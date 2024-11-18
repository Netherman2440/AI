from aidevs import Aidevs
from openaiService import OpenAIService
import os

ai = Aidevs()
openai = OpenAIService()

async def main():
    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to article.md
    article_path = os.path.join(script_dir, 'article.md')
    
    with open(article_path, 'r', encoding='utf-8') as file:
        article = file.read()
    
    response = await openai.completion([{
        "role": "user", 
        "content": f"Your task is to find all links in the article: {article}. Return only links, with descrpitions. Convert them into .md format."
    }])
    print(response.choices[0].message.content)

async def interpret_link(link: str, shrt_desc: str):

    response = await openai.completion([{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Whats in that image? Here's it's description: {shrt_desc}",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": link
                            },
                        },
                    ],
                },
    ])
    print(response.choices[0].message.content)
    # Save response to a text file
    with open('interpretation_result.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n\nLink: {link}\nDescription: {shrt_desc}\nInterpretation:\n")
        f.write(response.choices[0].message.content)

def parse_links_file(file_path: str) -> list[tuple[str, str]]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_path)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    links_with_descriptions = []
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('- ['): 
            continue
            
        # Extract description and link using regex or string manipulation
        description_start = line.find('[') + 1
        description_end = line.find(']')
        link_start = line.find('(') + 1
        link_end = line.find(')')
        
        if all(x != -1 for x in [description_start, description_end, link_start, link_end]):
            description = line[description_start:description_end]
            link = line[link_start:link_end]
            links_with_descriptions.append((link, description))
    
    return links_with_descriptions

# Przykład użycia:
async def interpret_links():
    links = parse_links_file('links.md')
    for link, description in links:
        print(f"Link: {link}")
        print(f"Opis: {description}\n")
        await interpret_link(link, description)
        

async def transcribe_audio(link: str, article: str):
    response = await openai.audio_transcription(link)
    print(response)
    response = await openai.completion([{
        "role": "user",
        "content": f"Interprete this audio: {response} as a part of the article: {article}"
    }])
    print(response.choices[0].message.content)

if __name__ == "__main__":
    import asyncio

    script_dir = os.path.dirname(os.path.abspath(__file__))
    article_path = os.path.join(script_dir, 'article.md')
    
    with open(article_path, 'r', encoding='utf-8') as file:
        article = file.read()
    
    asyncio.run(transcribe_audio("D:/Ignacy/Code/AI/Resources/rafal_dyktafon.mp3", article)) 