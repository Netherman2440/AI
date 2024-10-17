namespace AI;
public class PoligonHttp
{
    public async Task<string> GET(string uri = "https://poligon.aidevs.pl/dane.txt")
    {
        HttpClient httpClient = new HttpClient();

        var response = await httpClient.GetAsync(uri);    
        string content = await response.Content.ReadAsStringAsync();
        Console.WriteLine(content);
        return content;
    }

    public async Task<string> POST(string content, string uri = "https://poligon.aidevs.pl/verify")
    {
        using HttpClient httpClient = new HttpClient();

        var response = await httpClient.PostAsync(uri, new StringContent(content));
        
        string responseContent = await response.Content.ReadAsStringAsync();

        return responseContent;
    }

}
