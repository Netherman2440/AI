namespace AI;
public class Poligon
{
    private readonly string ApiKey;
    public Poligon()
    {
        DotNetEnv.Env.Load();

        ApiKey = Environment.GetEnvironmentVariable("DEVS_API_KEY") ?? throw new Exception("DEVS_API_KEY is not set in the .env file.");
    }
    public async Task ZeroTask()
    {
        PoligonHttp poligonHttp = new();
        string content = await poligonHttp.GET();
        Console.WriteLine(content);

        AIChatbot chatbot = new();

        chatbot.systemPrompt = "You are a c# expert";

        string userMessage = $"""
        Dla podanych dwóch ciągów znaków stwórz tablicę tych dwóch ciągów. 
        {content}
        Nie dodawaj żadnych dodatkowych komentarzy, zwróć tylko tablicę.  

        następnie utwórz odpowiedź w podanej formie:

        """;

        userMessage += @"{
   ""task"": ""POLIGON"",
    ""apikey"": """ + ApiKey +"\"" + @",
    ""answer"": TU WSTAW TABLICE
}";

        userMessage += "\n Nie dodawaj żadnych dodatkowych komentarzy, zwróć tylko obiekt json. Również nie dodawaj formuły kodu ```";

        Console.WriteLine(userMessage);

        var response =  await chatbot.AskGPTSync(userMessage);

        Console.WriteLine(response);

        var result = await poligonHttp.POST(response);

        Console.WriteLine(result);
    }
}