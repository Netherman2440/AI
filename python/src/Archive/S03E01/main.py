
import asyncio
from openaiService import OpenAIService
from aidevs import Aidevs
import os

answers = {
    "2024-11-12_report-00-sektor_C4.txt": "Aleksander Ragowski, jednostka organiczna, fabryka, skan biometryczny, baza danych, dział kontroli, patrol, ruch oporu, nauczyciel, angielski, automatyzacja, reżim, krytyk, aktywista, programista, Java, ucieczka, szkolenie, zabezpieczenia, zagrożenie, reżim robotów",
    "2024-11-12_report-01-sektor_A1.txt": "alarm, ruch, zwierzyna, leśna, fałszywy, spokój, obszar, patrol, bezpieczeństwo, sektor, A1, monitoring, zwierzęta",
    "2024-11-12_report-02-sektor_A3.txt": "Patrol, Noc, Monitoring, Obwód, Bezpieczeństwo, Cisza, Obiekt, Peryferie, Aktywność, Brak, Wykrycie, Sektor A3, Zadania, Raport, Stabilność",
    "2024-11-12_report-03-sektor_A3.txt": "Patrol, Monitoring, Sektor, A3, Czujniki, Aktywność, Życie organiczne, Stan, Zakłócenia",
    "2024-11-12_report-04-sektor_B2.txt": "Patrol, Sektor, Anomalia, Odchylenie, Komunikacja, Kanał, Bezpieczeństwo, Zachodni, Teren, Norma",
    "2024-11-12_report-05-sektor_C1.txt": "Sektor C1, Aktywność, Brak, Patrol, Monitoring, Sensor, Dźwięk, Detektory, Ruch, Sygnały, Analiza, Raport, Bezpieczeństwo, Technologia",
    "2024-11-12_report-06-sektor_C2.txt": "Sektor, Północny zachód, Skanery temperatury, Skanery ruchu, Operacyjność, Stabilność, Brak wykrycia, Patrol, Bezpieczeństwo, Monitoring",
    "2024-11-12_report-07-sektor_C4.txt": "sektor C4, czujnik dźwięku, ultradźwięk, sygnał, nadajnik, krzaki, las, analiza, odciski palców, Barbara Zawadzka, baza urodzeń, dział śledczy, bezpieczeństwo, ruch oporu, frontend developer, JavaScript, Python, sztuczna inteligencja, sabotaż, koktajl Mołotowa, powiązania, kryjówka, bezpieczeństwo, obszar zabezpieczony",
    "2024-11-12_report-08-sektor_A1.txt": "",
    "2024-11-12_report-09-sektor_C2.txt": "",
}

openai = OpenAIService()

files = "reports: \n"
facts = "facts: \n"

def prepare_files():
    # Get the directory of the current file
    global files, facts
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct path to Resources folder
    resources_path = os.path.join(current_dir, "Resources")

    # Open the Resources folder
    if os.path.exists(resources_path):
        print(f"Resources folder found at: {resources_path}")
    else:
        print("Resources folder not found")

    for file in os.listdir(resources_path):
        if "report" in file:

            with open(os.path.join(resources_path, file), "r") as f:
                print("reports", file)
                files += f" {file} \n"
                files += f"{f.read()} \n\n"
        else:
            with open(os.path.join(resources_path, file), "r") as f:
                print("facts", file)
                facts += f" {file} \n"
                facts += f"{f.read()} \n\n"
                



async def generate_keywords(file):

    response = await openai.completion(
    messages=[
        {
            "role": "system",
            "content": f"""
            <context>
            Zapoznaj się z 10-cioma plikami TXT z raportami

            {files}

            oraz 5-cioma plikami TXT z faktami

            {facts}

             Dane te dotyczą wydarzeń związanych z bezpieczeństwem, które zdarzyły się w różnych sektorach wokół fabryki. 
            </context>
           
            <objective>
            Do podanego przez użytkownika pliku wygeneruj słowa kluczowe w formie mianownika (czyli np. “sportowiec”, a nie “sportowcem”, “sportowców” itp.)
            
            Metadane mają ułatwić wyszukiwanie raportów w bazie danych
            
            Przy generowaniu metadanych z reportu posiłkuj się całą posiadaną wiedzą (czyli także faktami) 

            Na przykład jeśli raport dotyczy Aleksandra Rogowskiego posiłkuj się faktami o Aleksandrze Rogowskim

            Jeśli użycie faktów jest niepotrzebne, to je zignoruj. (np. raport dotyczy ruchu w lesie, a nie konkretnych osób)

            ZAWSZE mów w jakim sektorze doszło do wydarzenia

            Generuj słowa kluczowe dotyczące danego raportu oraz faktów przydatnych w danym raporcie

            Słowa kluczowe muszą być w języku polskim

            Słowa kluczowe muszą być unikalne



            </objective>
            """
        },
        {
            "role": "user",
            "content": file
        }
    ]
    )

    return response

async def convert_answer(file: str):
    response = await openai.completion(
    messages=[
        {
            "role": "system",
            "content": f"""
            Przekształć wiadomość użytkownika do podanej formy:

            <example>
            - Jednostka
            - Aleksander Ragowski
            - Patrol
            </example>

            <output>
            "Jednostka, Aleksander Ragowski, Patrol"
            </output>
            """
        },
        {
            "role": "user",
            "content": file
        }
    ]
    )

    return response
    
async def generate_answer():

    prepare_files()

    response = await generate_keywords(" 2024-11-12_report-07-sektor_C4.txt")

    print(response.choices[0].message.content)

    converted = await convert_answer(response.choices[0].message.content)

    print(converted.choices[0].message.content)

async def verify_answer():

    aidevs = Aidevs()

    result = await aidevs.verify("dokumenty", answers)

    print(result)


asyncio.run(verify_answer())

