import json
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import requests
from requests.auth import HTTPBasicAuth

from chatBot import ChatBot

# Załaduj token z pliku .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Tworzymy nową klasę bota dziedziczącą po discord.Client
class MyBot(discord.Client):
    def __init__(self):
        # Inicjalizacja z intencjami
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        # Utworzenie drzewa komend
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Rejestracja komend dla wszystkich serwerów
        await self.tree.sync()

client = MyBot()
ai_chatbot = ChatBot()
# Przykładowa komenda slash


@client.tree.command(name="system", description="Ustaw system prompt dla chatbota")
@app_commands.describe(
    prompt="Nowy system prompt dla chatbota"
)
async def system_command(interaction: discord.Interaction, prompt: str):
    try:
        await interaction.response.defer()
        
        # Aktualizuj system prompt dla globalnego chatbota
        ai_chatbot.system_prompt = prompt
        
        await interaction.followup.send(f"System prompt został zaktualizowany. Nowy prompt:\n```{prompt}```")
        
    except Exception as e:
        await interaction.followup.send(f"Wystąpił błąd: {str(e)}")



async def get_channel_history(channel, limit, skip_first_command=True):
    messages = []
    
    async for msg in channel.history(limit=limit + 1):
        if skip_first_command:
            skip_first_command = False
            continue
        messages.append(f"{msg.author.name}: {msg.content}")
    if not messages:
        return "Nie znaleziono żadnych wiadomości."
    return messages

@client.event
async def on_message(message):
    # Ignoruj wiadomości od samego bota
    if message.author == client.user:
        return

    # Sprawdź czy bot został wspomniany (pingowany)
    if client.user.mentioned_in(message) and not message.mention_everyone:
        # Możesz dostosować odpowiedź bota
        response = await ai_chatbot.ask(message.content)
        print(f"User: {message.content}\nAI: {response}")
        await message.reply(response)

# Możesz zachować również stare eventy
@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')
    print(f'Bot jest gotowy do użycia!')

client.run(TOKEN)