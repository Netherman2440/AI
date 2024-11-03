using Newtonsoft.Json.Linq;
using System.Net.Http;
using System.Reflection.Metadata;
using System.Runtime.InteropServices;
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

    public async Task ChatGPT(string model = "gpt-4o")
    {
        //todo: add history

        JArray messages = new(){
             new JObject { ["role"] = "system", ["content"] = systemPrompt }
        };

        httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", ApiKey);

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"System message: {systemPrompt}");

        while (true)
        {
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine("Podaj swoje pytanie: (exit - wyjdz)");
            Console.ResetColor();

            string userInput = Console.ReadLine();

            if (userInput == "exit")
            {
                break;
            }

            var userMessage = new JObject { ["role"] = "user", ["content"] = userInput };

            messages.Add(userMessage);

            var response = await Chat(messages, model, true);

            Console.ForegroundColor = ConsoleColor.Blue;
            Console.WriteLine(response);
            Console.ResetColor();

            var assistantMessage = new JObject { ["role"] = "assistant", ["content"] = response };

            messages.Add(assistantMessage);

        }

        messages.Clear();
    }
    public async Task<string> Chat(string user, string system = "You are a helpful assistant.", string model = "gpt-4o")
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

        var messages = new JArray
         {
             new JObject { ["role"] = "system", ["content"] = system },
             new JObject { ["role"] = "user", ["content"] = user }
         };

        return await Chat(messages);
    }

    private async Task<string> Chat(JArray messages, string model = "gpt-4", bool isAuthorisated = false)
    {
        var data = new JObject
        {
            ["model"] = model,
            ["messages"] = new JArray(messages) // Przekazujemy całą historię wiadomości
        };

        var content = new StringContent(data.ToString(), Encoding.UTF8, "application/json");


        if (!isAuthorisated)
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
            string resultContent = await result.Content.ReadAsStringAsync();
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