import asyncio
import json
from openaiService import OpenAIService
from aidevs import Aidevs

aidevs = Aidevs()
openai = OpenAIService()

query = 'START'
response = asyncio.run(aidevs.api(query))
print(response.json())

response = asyncio.run(openai.completion(
    messages=[
        {
            "role": "system",
            "content": """
 description: >
 1. Analyze user message and return 4 images urls that are there.

  output_format:
  {
    image_urls: ["url1", "url2", "url3", "url4"]
  }

   instructions: |
    Replace "URL of the analyzed image" with the URL of each respective image.
    REPLY ONLY IN A RAW, FORMATTED JSON FORMAT WITHOUT ADDITIONAL SPACES,  LINE BREAKS OR ''' signs
"""
        },
        {
            "role": "user",
            "content": f"{response.json()['message']}"
        }

    ]
))

print(response.choices[0].message.content)

json_response = json.loads(response.choices[0].message.content)
print(json_response)

for image_url in json_response['image_urls']:
    response = asyncio.run(openai.vision(
        file_path_or_url=image_url,
        prompt="""
         Analyze a photo and perform the following tasks:
    0.  - REPLY ONLY IN A RAW, FORMATTED JSON FORMAT WITHOUT ADDITIONAL SPACES,  LINE BREAKS OR ''' signs
  1. Identify if the image depicts a woman.

  3. If the image does not depict a woman but appears to be a normal photo, respond with 'not related'.

output_format:

  {
    "image_url": "URL",
    "operation": "REPAIR, DARKEN, BRIGHTEN, or 'not related'"
  }

  
  example of good answer:
{"image_url":"https://centrala.ag3nts.org/dane/barbara/IMG_1410.PNG","operation":"REPAIR"}

  example of bad answer:
 ```json
  {"image_url":"https://centrala.ag3nts.org/dane/barbara/IMG_1410.PNG","operation":"REPAIR"}
  ```

instructions: |
  - Replace "URL" with the url of each respective image.
  - For "operation", select one of the following based on the analysis:
      - REPAIR if the image is damaged,
      - DARKEN if the image is overly bright,
      - BRIGHTEN if the image is too dark,
      - "not related" if the image does not depict a woman and appears normal.


"""

    ))
    response_json = json.loads(response)
    print(response_json)
    url = image_url.replace("https://centrala.ag3nts.org/dane/barbara/", "")
    message = f"{response_json['operation']} {url}"
    print(message)
    response = asyncio.run(aidevs.api(message))
    print(response.json()['message'])

    AI_response = asyncio.run(openai.completion(
        messages=[
            {"role": "system",
            "content": """
                If user message contains whole url of image, return it. If there is just image name add at start:
                https://centrala.ag3nts.org/dane/barbara/

                structure of output:
                {
                    "message": "https://centrala.ag3nts.org/dane/barbara/image_name.PNG"
                }
            """
            },
            {
                "role": "user",
                "content": f"{response.json()['message']}"
            }
        ]
    ))
    #AI_response_json = json.loads(AI_response.choices[0].message.content)
    print(AI_response.choices[0].message.content)

    response = asyncio.run(aidevs.api(AI_response.choices[0].message.content))
    print(response.json()['message'])

