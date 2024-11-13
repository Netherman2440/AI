import os
import dotenv
from openai import OpenAI
import base64

map_0 = "D:\Ignacy\Code\AI\Resources\map_0.jpg"
map_1 = "D:\Ignacy\Code\AI\Resources\map_1.jpg"
map_2 = "D:\Ignacy\Code\AI\Resources\map_2.jpg"
map_3 = "D:\Ignacy\Code\AI\Resources\map_3.jpg"


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image(map_3)
dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{
    "role": "system",
    "content": "You are a expert in image processing and you are given a map of the city. Carefully analyze all the image before answering."
  },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "This is a map of the city in Poland. Your task is to print ALL names of places and streets mentioned in the image. Then find the name of the city."},
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])


answer_0 = 'Boczna\n- Twardowskiego\n- Dworska \nSłomiana\n- - Szwedzka \n'
answer_1 = 'Cmentarna\n- Parkowa\n- 534\n- Cmentarz ewangelicko-augsburski\n trasa 534 - ?\n'
answer_2 = 'Kalinkowa\n- Brzeźna\n- Chełmińska\n- Chopina\n- ???\n'
answer_3 = 'Kalinowska\n2. Konstantego Ildefonsa Gałczyńskiego\n3. Stroma\n4. Władysława Reymonta\n ??\n'


response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{
    "role": "user",
    "content": f'''
    You are given 4 lines of street names. 
    Your task is to write ALL names of the POLISH cities mentioned that has those streets
    
    Answer:
    {answer_0}
    {answer_1}
    {answer_2}
    {answer_3}

3 of them ARE FROM ONE CITY. NAME THIS CITY.
    '''
  },
  ]
)

print(response.choices[0])
