using System.Xml;
using Newtonsoft.Json;

public class XMLConverter
{
    public void XMLToMidi(string inputXmlPath, string outputMidiPath)
    {
          string xmlFilePath = "test.musicxml";
        XmlDocument xmlDocument = new XmlDocument();
        xmlDocument.Load(xmlFilePath);

        string jsonText = JsonConvert.SerializeXmlNode(xmlDocument);

        Console.WriteLine(jsonText);  // Wyświetla JSON w konsoli

        
    }   
}