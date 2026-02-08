# import discord
# from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

token = os.getenv('DISCORD_TOKEN')

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)