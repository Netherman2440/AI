import asyncio
from aidevs import Aidevs

aidevs = Aidevs()

photos = ['IMG_1410_FXER.PNG', 'IMG_1410_FXER.PNG', 'IMG_1410_FXER.PNG']




response = asyncio.run(aidevs.api("Barbara ma czarne włosy, okulary i tatuaż na lewym ramieniu."))
print(response.json()['message'])
