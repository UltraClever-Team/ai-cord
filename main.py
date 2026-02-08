import discord
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from better_profanity import profanity

load_dotenv()
knowledge = open("knowledge.txt", "r").read()
token = os.getenv('DISCORD_TOKEN')
client = genai.Client()
chat = client.chats.create(model="gemini-3-flash-preview", config=types.GenerateContentConfig(system_instruction=f"{knowledge}"))

def ask(prompt):
    response = chat.send_message(prompt)
    return response.text

bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'{bot.user} working!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        if profanity.contains_profanity(message.content):
            await message.channel.send("I'm sorry, but I can't respond to messages with inappropriate language.")
            return
        else:
            prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
            reply = ask(prompt)
            if profanity.contains_profanity(reply):
                await message.channel.send("I'm sorry, but I can't provide a response due to inappropriate content.")
                return
            else:
                await message.channel.send(reply)

bot.run(token)