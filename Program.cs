using AI;

Console.WriteLine("Hello, World!");

AIChatbot chatbot = new AIChatbot();
while (true)
{
    Console.WriteLine("Podaj swoje pytanie: ");
    string userInput = Console.ReadLine();
    Console.WriteLine(chatbot.AskGPTSync("You are a helpful assistant", userInput));
}

