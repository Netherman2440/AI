import asyncio
from aidevs import Aidevs
from openaiService import OpenAIService

aidevs = Aidevs()
openaiService = OpenAIService()


query_index = 0
query_count = 50


people_queries = []
places_queries = []

is_people_query = False

start_query = 'FROMBORK'


async def verify_query(query: str):
    response = await aidevs.verify("loop",query, False)
    print(response)
    

async def Query(query: str):

    global is_people_query
    if is_people_query:
        await people_query(query)
    else:
        await places_query(query)
        

async def people_query(query: str):
    print(f'people_query: {query}')
    global query_index
    query_index += 1
    
    if query == 'BARBARA' or query == 'GLITCH':
        return

    people_result = await aidevs.people(query)
    people_result = people_result.json()


    print(people_result['message'])

    if 'no data found for' in people_result['message']:
        return

    next_queries = await next_Queries(people_result['message'])

    for query in next_queries:
        global query_count
        if query == 'LUBLIN':
            continue
        if query_index <  query_count and query not in places_queries:
            global is_people_query
            is_people_query = False
            places_queries.append(query)
            await Query(query)
    

async def places_query(query: str):
    print(f'places_query: {query}')
    global query_index

    query_index += 1


    if query == 'LUBLIN':
        return

    places_result = await aidevs.places(query)
    places_result = places_result.json()
    
    print(places_result['message'])

    if 'no data found for' in places_result['message']:
        return
    
    next_queries = await next_Queries(places_result['message'])
    

    for new_query in next_queries:
        global query_count
        
        if new_query == 'BARBARA':
            print(f'\033[92mBARABARA WAS IN {query}\033[0m')
            continue
        if query_index < query_count and new_query not in people_queries:
            global is_people_query
            is_people_query = True
            people_queries.append(new_query)
            await Query(new_query)


async def next_Queries(message: str):
    words = message.split()
    normalized_words = []

    for word in words:
        
        if word == 'RAFAŁ':
            normalized_words.append('RAFAL')
        else:
            normalized_words.append(word)
        

    return normalized_words

def prepare_query(query: str):
    words = query.split()
    if len(words) > 1:
        print(f"Message contains more than one word: {query}, parsed to {words[0]}")
    return words[0]

def save_results_to_files():
    # Usuwamy duplikaty używając set()
    unique_people = set(people_queries)
    unique_places = set(places_queries)
    
    # Zapisujemy wyniki do plików
    with open('people.txt', 'a+', encoding='utf-8') as f:
        # Najpierw wczytujemy istniejące dane
        f.seek(0)
        existing_people = set(f.read().splitlines())
        # Dodajemy tylko nowe, nieunikalne wpisy
        new_people = unique_people - existing_people
        if new_people:
            # Wracamy na koniec pliku
            f.seek(0, 2)
            for person in new_people:
                f.write(f"{person}\n")
    
    with open('places.txt', 'a+', encoding='utf-8') as f:
        # Najpierw wczytujemy istniejące dane
        f.seek(0)
        existing_places = set(f.read().splitlines())
        # Dodajemy tylko nowe, nieunikalne wpisy
        new_places = unique_places - existing_places
        if new_places:
            # Wracamy na koniec pliku
            f.seek(0, 2)
            for place in new_places:
                f.write(f"{place}\n")
if __name__ == '__main__':
    #asyncio.run(Query(start_query))
    print(people_queries)
    print(places_queries)
    #save_results_to_files()
    asyncio.run(verify_query('ELBLAG'))


