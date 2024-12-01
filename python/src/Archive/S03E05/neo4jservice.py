import dotenv
from neo4j import GraphDatabase
import os
from openaiService import OpenAIService

dotenv.load_dotenv()

class Neo4jService:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = 'neo4j'
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self.verify_connection()

    def verify_connection(self):
        try:
            self.driver.verify_connectivity()
            print("Connected to Neo4j successfully!")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise


    def create_connection(self, from_node_id: int, to_node_id: int, relationship_type: str, properties: dict = {}):
        #TODO: Better node searching
        cypher = f"""
        MATCH (a), (b)
        WHERE a.user_id = "{from_node_id}" AND b.user_id = "{to_node_id}"   
        CREATE (a)-[r:{relationship_type}]->(b)
        SET r = $properties
        RETURN r
        """
        return self.query(cypher, parameters={"properties": properties})

    async def add_node(self, label: str, properties: dict, create_embedding: bool = True):
        if create_embedding:
            if 'embedding' not in properties:
                text = properties.get('username', '') or properties.get('title', '') or ''
                properties['embedding'] = await self.create_embedding(text)

        cypher = f"""
        CREATE (n:{label}) 
        SET n = $properties
        RETURN id(n) AS id, n
        """
        return self.query(cypher, parameters={"properties": properties})

    def get_all_nodes(self):
        cypher = """
        MATCH (n) 
        RETURN n
        """
        return self.query(cypher)

    def delete_all_nodes(self):
        cypher = """
        MATCH (n)
        DETACH DELETE n
        """
        return self.query(cypher)

    async def create_embedding(self, text: str):
        openai = OpenAIService()
        return await openai.create_embedding(text)
    
    def query(self, cypher:str, parameters: dict = {}):
        return self.driver.execute_query(cypher, parameters, database_= self.database)
    
    def close(self):
        self.driver.close()
        print("Connection closed")

