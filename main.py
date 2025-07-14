import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='mw_', intents = intents)

def load_channel_id(requested_channel_id):
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      return ids_data [0][requested_channel_id]
  except FileNotFoundError:
    print('server_ids.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from server_ids.json')

@bot.event
async def on_ready():
  print(f'{bot.user.name} is online!')
  x = load_channel_id("new_mem_ch")
  print(x)

@bot.event
async def on_member_join(member):
  new_mem_channel_id = load_channel_id("new_mem_ch")
  new_mem = bot.get_channel(new_mem_channel_id)
  if new_mem:
    await new_mem.send(f"{member.mention}, welcome to the LT Workshop!")
  else:
    print(f'Something is wrong! {new_mem_channel_id} is not found!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)