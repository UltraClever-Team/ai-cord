import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

token = os.getenv('DISCORD_TOKEN')

# Incomplete