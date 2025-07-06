import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='mw_', intents = intents)

@bot.event
async def on_ready():
  print(f'{bot.user.name} is online!')

@bot.event
async def on_member_join(member):
  welcome_ch_id = 1381353794859827211
  welcome_ch = bot.get_channel(welcome_ch_id)
  if welcome_ch:
    await welcome_ch.send(f"{member.mention}, welcome to the LT Workshop!")
  else:
    print(f'Something is wrong! {welcome_ch_id} is not found!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)