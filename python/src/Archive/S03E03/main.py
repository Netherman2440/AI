import asyncio
from openaiService import OpenAIService
from aidevs import Aidevs

aidevs = Aidevs()
openaiService = OpenAIService()

base_url = 'https://centrala.ag3nts.org/apidb'
question = 'które aktywne datacenter (DC_ID) są zarządzane przez pracowników, którzy są na urlopie (is_active=0)'

tables = ['users', 'datacenters', 'connections', 'correct_order']
structure = 'show create table NAZWA'

query ='SELECT dc_id FROM datacenters d JOIN users u ON d.manager = u.id WHERE d.is_active = 1 AND u.is_active = 0'

result = asyncio.run(aidevs.api(query))

answer = ["4278", "9294"]

response = asyncio.run(aidevs.verify("database", answer))

print(response)

