
import os
import dotenv
import openai

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

adam = "D:/Ignacy/Code/AI/Resources/przesluchania/adam.m4a"
agnieszka = "D:/Ignacy/Code/AI/Resources/przesluchania/agnieszka.m4a"
adrian = "D:/Ignacy/Code/AI/Resources/przesluchania/ardian.m4a"
michal = "D:/Ignacy/Code/AI/Resources/przesluchania/michal.m4a"
monika = "D:/Ignacy/Code/AI/Resources/przesluchania/monika.m4a"
rafal = "D:/Ignacy/Code/AI/Resources/przesluchania/rafal.m4a"



client = openai.OpenAI(api_key=api_key)

audio_file= open(rafal, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
with open("transcription.txt", "a", encoding="utf-8") as f:
    f.write(transcription.text + "\n")
print(transcription.text)
