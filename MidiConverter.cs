using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;
using NAudio.Midi;

public class MidiConverter
{
    public void JsonToMidi(string inputJsonPath, string outputMidiPath)
    {
        // Wczytaj dane JSON
        var jsonData = File.ReadAllText(inputJsonPath);
        var midiEvents = JsonConvert.DeserializeObject<List<Dictionary<string, object>>>(jsonData);

        // Utwórz nowy plik MIDI
        var midiEventCollection = new MidiEventCollection(1, 480); // Format MIDI i ticki na takt

        // Dodaj ścieżkę do pliku MIDI
        var trackEvents = new List<MidiEvent>();

        foreach (var midiEvent in midiEvents)
        {
            int absoluteTime = Convert.ToInt32(midiEvent["AbsoluteTime"]);

            switch (midiEvent["EventType"].ToString())
            {
                case "NoteOn":
                    int noteNumber = Convert.ToInt32(midiEvent["NoteNumber"]);
                    int velocity = Convert.ToInt32(midiEvent["Velocity"]);
                    trackEvents.Add(new NoteOnEvent(absoluteTime, 1, noteNumber, velocity, 0));
                    break;

                case "ControlChange":
                    int controller = Convert.ToInt32(midiEvent["Controller"]);
                    int controllerValue = Convert.ToInt32(midiEvent["ControllerValue"]);
                    trackEvents.Add(new ControlChangeEvent(absoluteTime, 1, (MidiController)controller, controllerValue));
                    break;

                case "Tempo":
                    int tempo = Convert.ToInt32(midiEvent["BPM"]);
                    trackEvents.Add(new TempoEvent(tempo, absoluteTime));
                    break;

                case "Text":
                    string text = midiEvent["Text"].ToString();
                    trackEvents.Add(new TextEvent(text, MetaEventType.TextEvent, absoluteTime));
                    break;

                case "TimeSignatureEvent":
                    // Dodaj sygnaturę metrum - tutaj zakładamy wartości domyślne (np. 4/4)
                    trackEvents.Add(new TimeSignatureEvent(absoluteTime, 4, 2, 24, 8));
                    break;

                case "KeySignatureEvent":
                    // Dodaj sygnaturę tonacji - zakładamy tonację C-dur (0) i 0 tryb (durowy)
                    trackEvents.Add(new KeySignatureEvent(absoluteTime, 0, 0));
                    break;

                case "MetaEvent":
                    // Dodajemy zakończenie tracka
                    trackEvents.Add(new MetaEvent(MetaEventType.EndTrack, 0, absoluteTime));
                    break;
                /*case "PatchChangeEvent":
                    int patchNumber = Convert.ToInt32(midiEvent["Instrument"]);
                    trackEvents.Add(new PatchChangeEvent(absoluteTime, 1, patchNumber));
                    break;*/
                /*case "RawMetaEvent":
                    byte[] rawData = (byte[])midiEvent["RawMetaEvent"];
                    trackEvents.Add(new RawMetaEvent(MetaEventType.TrackSequenceNumber, absoluteTime, rawData));
                    break;*/
                
                default:
                    Console.WriteLine($"Unrecognized event type: {midiEvent["EventType"]}");
                    break;
            }
        }

        // Dodaj track do kolekcji eventów MIDI
        midiEventCollection.AddTrack(trackEvents);

        // Zapisz plik MIDI
        MidiFile.Export(outputMidiPath, midiEventCollection);
    }
}


