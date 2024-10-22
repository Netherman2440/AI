using System;
using System.IO;
using NAudio.Wave;

namespace AI
{
    internal class AudioReader
    {
        public void Read()
        {
            Console.WriteLine("Press 'r' to start recording, and 's' to stop.");

            using (var waveIn = new WaveInEvent())
            {
                // Ustawienie formatu audio (44.1 kHz, 16-bit, 1 kanał - mono)
                waveIn.WaveFormat = new WaveFormat(44100, 16, 1);

                // Zapis dźwięku do pliku WAV
                using (var writer = new WaveFileWriter("recordedAudio.wav", waveIn.WaveFormat))
                {
                    // Obsługa zdarzenia zapisu danych audio
                    waveIn.DataAvailable += (sender, e) =>
                    {
                        writer.Write(e.Buffer, 0, e.BytesRecorded);
                    };

                    // Rozpoczęcie nagrywania po naciśnięciu 'r'
                    ConsoleKey key;
                    do
                    {
                        key = Console.ReadKey().Key;
                        if (key == ConsoleKey.R)
                        {
                            Console.WriteLine("\nRecording started...");
                            waveIn.StartRecording();
                        }
                        // Zatrzymanie nagrywania po naciśnięciu 's'
                        if (key == ConsoleKey.S)
                        {
                            Console.WriteLine("\nRecording stopped.");
                            waveIn.StopRecording();
                        }
                    } while (key != ConsoleKey.S);
                }
            }

            Console.WriteLine("Audio saved as 'recordedAudio.wav'.");
        }
    }
}
