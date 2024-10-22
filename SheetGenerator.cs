using NAudio.Midi;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;

public class SheetGenerator
{
    public void MidFile()
    {
        var midiFile = new MidiFile("test.mid", false); // Wczytaj plik MIDI
        Console.WriteLine($"Number of tracks: {midiFile.Tracks}");

        // Lista, która będzie zawierać wszystkie dane o MIDI
        var midiData = new List<Dictionary<string, object>>();

        foreach (var track in midiFile.Events)
        {
            Console.WriteLine($"Track: {track}");

            foreach (var midiEvent in track)
            {
                var eventData = new Dictionary<string, object>();

                // Sprawdzamy typ zdarzenia MIDI i zapisujemy odpowiednie dane
                if (midiEvent is NoteOnEvent noteOn)
                {
                    eventData["EventType"] = "NoteOn";
                    eventData["NoteNumber"] = noteOn.NoteNumber;
                    eventData["Velocity"] = noteOn.Velocity;
                    eventData["AbsoluteTime"] = noteOn.AbsoluteTime;
                }
                /*else if (midiEvent is NoteOffEvent noteOff)
                {
                    eventData["EventType"] = "NoteOff";
                    eventData["NoteNumber"] = noteOff.NoteNumber;
                    eventData["AbsoluteTime"] = noteOff.AbsoluteTime;
                }*/
                else if (midiEvent is ControlChangeEvent controlChange)
                {
                    eventData["EventType"] = "ControlChange";
                    eventData["Controller"] = controlChange.Controller;
                    eventData["ControllerValue"] = controlChange.ControllerValue;
                    eventData["AbsoluteTime"] = controlChange.AbsoluteTime;
                }
                else if (midiEvent is TempoEvent tempoEvent)
                {
                    eventData["EventType"] = "Tempo";
                    eventData["MicrosecondsPerQuarterNote"] = tempoEvent.MicrosecondsPerQuarterNote;
                    eventData["BPM"] = tempoEvent.Tempo;
                    eventData["AbsoluteTime"] = tempoEvent.AbsoluteTime;
                }
                else if (midiEvent is TextEvent textEvent)
                {
                    eventData["EventType"] = "Text";
                    eventData["Text"] = textEvent.Text;
                    eventData["AbsoluteTime"] = textEvent.AbsoluteTime;
                }
                else
                {
                    eventData["EventType"] = midiEvent.GetType().Name;
                    eventData["AbsoluteTime"] = midiEvent.AbsoluteTime;
                }

                // Dodajemy każde zdarzenie do listy
                midiData.Add(eventData);
            }
        }

        // Serializacja listy zdarzeń MIDI do formatu JSON
        var json = JsonConvert.SerializeObject(midiData, Formatting.Indented);
        Console.WriteLine(json);

        // Zapisujemy JSON do pliku
        System.IO.File.WriteAllText("midiData.json", json);

        MidiConverter midiConverter = new MidiConverter();
        midiConverter.JsonToMidi("midiData.json", "newMidi.mid");
    }
}
