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

bot = discord.Bot()

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

@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx):
    await ctx.respond(f"Pong! The latency is {round(bot.latency * 1000)}ms.")

@bot.slash_command(name="is-bad", description="Check if a message contains bad language")
async def is_bad(ctx, message: str):
    if profanity.contains_profanity(message):
        await ctx.respond("Yes, the message contains bad language.")
    else:
        await ctx.respond("No, the message is clean.")

@bot.slash_command(name="setting", description="Ask the bot a question")
async def setting(ctx):
    await ctx.respond("Please set any specific settings you want for the bot in `setting.json` file! (WIP) ")


bot.run(token)