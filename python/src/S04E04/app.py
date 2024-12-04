
import asyncio
from aidevs import Aidevs

aidevs = Aidevs()

response = asyncio.run(aidevs.verify('webhook', 'https://azyl-51279.ag3nts.org'))

print(response)
