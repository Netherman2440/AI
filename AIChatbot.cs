using Newtonsoft.Json.Linq;
using System.Net.Http;
using System.Text;

namespace AI;
public class AIChatbot
{
    private readonly HttpClient httpClient = new HttpClient();

    private readonly string ApiKey;

    public AIChatbot()
    {
        DotNetEnv.Env.Load();

        ApiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("OPENAI_API_KEY is not set in the .env file.");
    }
    public string AskGPTSync(string system, string user, string model = "gpt-4o")
    {
        var data = new JObject
        {
            ["model"] = model,
            ["messages"] = new JArray
         {
             new JObject { ["role"] = "system", ["content"] = system },
             new JObject { ["role"] = "user", ["content"] = user }
         }
        };

        DotNetEnv.Env.Load();

        var content = new StringContent(data.ToString(), Encoding.UTF8, "application/json");
        httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", ApiKey);

        HttpResponseMessage result;
        try
        {
            result = httpClient.PostAsync("https://api.openai.com/v1/chat/completions", content).GetAwaiter().GetResult();
        }
        catch (HttpRequestException e)
        {
            return "Error while sending request: " + e.Message;
        }

        if (result.IsSuccessStatusCode)
        {
            string resultContent = result.Content.ReadAsStringAsync().GetAwaiter().GetResult();
            var json = JObject.Parse(resultContent);
            string messageContent = json["choices"][0]["message"]["content"].ToString().Trim();
            return messageContent;
        }
        else
        {
            return "Nie udalo sie uzyskac odpowiedzi, sprawdz blad: " + result.ReasonPhrase;
        }
    }
}