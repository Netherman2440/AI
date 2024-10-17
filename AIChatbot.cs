using Newtonsoft.Json.Linq;
using System.Net.Http;
using System.Text;

namespace AI;
public class AIChatbot
{
    private readonly HttpClient httpClient = new HttpClient();

    public string systemPrompt = "You are a helpful assistant";
    private readonly string ApiKey;

    public AIChatbot()
    {
        DotNetEnv.Env.Load();

        ApiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("OPENAI_API_KEY is not set in the .env file.");
    }

    public async void ChatGPT()
    {
        while (true)
        {
            Console.WriteLine("Podaj swoje pytanie: (exit - wyjdz)");
            string userInput = Console.ReadLine();

            if (userInput == "exit")
            {
                break;
            }

           var response = await AskGPTSync(systemPrompt, userInput);
           Console.WriteLine(response);
        }
    }
    public async Task<string> AskGPTSync(string user, string system = "" ,string model = "gpt-4o")
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
            result = await httpClient.PostAsync("https://api.openai.com/v1/chat/completions", content);
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