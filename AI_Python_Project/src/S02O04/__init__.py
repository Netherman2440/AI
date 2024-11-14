import os
from aidevs import Aidevs
from openaiService import OpenAIService
import asyncio
import re
import json

aidevs = Aidevs()
openai = OpenAIService()

async def convert_files():
    folder_path = "Resources/pliki_z_fabryki/"
    output_path = "Resources/output/"
    output_file = os.path.join(output_path, "all_responses.txt")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    # Clear output file before processing new files
    open(output_file, "w", encoding="utf-8").write("...")
    for file in os.listdir(folder_path):
        print(file)
        if file in open(output_file, "r", encoding="utf-8").read():
            print("File already processed")
            continue
        
        if file.endswith(".jpg") or file.endswith(".png"):
            #photo convert to text
            response = await openai.photo_to_text(folder_path + file)
            print(response)
            # Using 'with' statement for proper file handling
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== {file} ===\n")
                f.write(response)
                f.write("...")
        elif file.endswith(".mp3") or file.endswith(".wav"):
            #audio transcription
            response = await openai.audio_transcription(folder_path + file)
            print(response)
            # Using 'with' statement for proper file handling
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== {file} ===\n")
                f.write(response)
                f.write("...")
        else:
            print(file)
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== {file} ===\n")
                f.write(open(folder_path + file, "r", encoding="utf-8").read())
                f.write("...")
            #.txt file
        
def getfilesdesc():
    file_path = "Resources/output/all_responses.txt"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content by file sections
    sections = content.split("...")
    files_data = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Znajdź nazwę pliku między === ===
        filename_match = re.search(r'=== (.*?) ===', section)
        if filename_match:
            filename = filename_match.group(1)
            # Usuń linię z nazwą pliku i pobierz resztę jako opis
            description = re.sub(r'=== .*? ===\n?', '', section).strip()
            files_data.append({
                "nazwa pliku": filename,
                "opis": description
            })

    return files_data
    
async def categorize_files():
    files_data = getfilesdesc()
    print(len(files_data))

    categories = {"people": [], "hardware": []}
    for file_data in files_data:

        response = await openai.completion(
            messages=[
                {"role": "system", "content": '''
                <objective>
                Your task is to categorize the text into two categories:
                
                If fragment is about people, answer: people
                If fragment is about hardware, answer: hardware
                If fragment isnt about people or hardware for example about software, answer: other
                </objective>
   
                <example>
                user:
                'opis pliku: This is a text about people.'
                
                assistant:
                people
                 
                </example>
                '''},
                {"role": "user", "content": file_data['opis']}
            ]
        )
        print(file_data['nazwa pliku'], response.choices[0].message.content)
        if response.choices[0].message.content == "other":
            continue
        categories[response.choices[0].message.content].append(file_data['nazwa pliku'])

    print("Categories:")
    print(categories)

    message = json.dumps(categories)
    print(message)
    response = await aidevs.verify("kategorie", message, False)
    print(response)

async def send_final_answer():
    message ={"people": ["2024-11-12_report-00-sektor_C4.txt", "2024-11-12_report-07-sektor_C4.txt", "2024-11-12_report-10-sektor-C1.mp3"], "hardware": [ "2024-11-12_report-13.png", "2024-11-12_report-15.png", "2024-11-12_report-17.png"]}

    response = await aidevs.verify("kategorie", message)
    print(response)

if __name__ == "__main__":
    asyncio.run(send_final_answer())
    #categorize files

'''
             <objective>
             Your task is to categorize the text into two categories:
             
             If fragment is about people, put it in "people" category.
             If fragment is about hardware, put it in "hardware" category.
             you must categorize all fragments, even if you are not sure about it.
             </objective>
             <rules>
             You must categorize all fragments, even if you are not sure about it.
             You can speak freely before giving final answer. 
             you can loudly think before giving final answer.
             </rules>
             <output>
             Output should be in JSON format:

             {
                "people": ["plik1.txt", "plik2.mp3", "plikN.png"],
                "hardware": ["plik4.txt", "plik5.png", "plik6.mp3"],
             }
             </output>

             <example>
             === plik1.txt ===
             This is a text about people.'''