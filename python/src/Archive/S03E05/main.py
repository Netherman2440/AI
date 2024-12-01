import asyncio
import json
from aidevs import Aidevs
from neo4jservice import Neo4jService


async def load_data():
    query = "select * from users"
    response = await aidevs.api(query)
    print(json.dumps(response.json()["reply"]))
    with open('users.txt', 'w') as f:
        f.write(json.dumps(response.json()["reply"]))

neo4j = Neo4jService()
aidevs = Aidevs()

async def load_users():
    with open('users.txt', 'r') as f:
        users = json.load(f)
        for user in users:
            await neo4j.add_node('USER', user, False)
            print(user)

def load_connections():
    with open('connections.txt', 'r') as f:
        connections = json.load(f)
        for connection in connections:
            neo4j.create_connection(connection['user1_id'], connection['user2_id'], 'KNOWS')
           

def transform_users_file():
    # Wczytaj dane
    with open('users.txt', 'r') as f:
        users = json.load(f)
    
    # Transformuj dane
    transformed_users = []
    for user in users:
        transformed_user = user.copy()
        transformed_user['user_id'] = transformed_user.pop('id')
        transformed_users.append(transformed_user)
    
    # Zapisz przetransformowane dane z powrotem do pliku
    with open('users.txt', 'w') as f:
        json.dump(transformed_users, f)
    
    print("Users data transformed successfully")
def path():
    cypher = '''
    MATCH (start:USER {username: 'Rafał'}),
      (end:USER {username: 'Barbara'}),
      path = shortestPath((start)-[:KNOWS*]-(end))
RETURN [node in nodes(path) | node.username] as names,
       length(path) as pathLength
'''
    result = neo4j.query(cypher)
    return result

async def verify():
    ans = "Rafał, Azazel, Aleksander, Barbara"
    return await aidevs.verify('connections', ans)

async def main():
    
    #load_connections()
    #result = neo4j.create_connection(1, 2, 'KNOWS')
    #print(result)

    response = await verify()
    print(response)
    

if __name__ == "__main__":
    asyncio.run(main())
