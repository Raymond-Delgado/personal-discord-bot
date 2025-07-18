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

def load_channel_id(requested_server_id, requested_channel_id):
  s_index = 0
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      for index in ids_data:
        if requested_server_id == index["server_id"]:
          s_index = index
      return(s_index, ids_data [s_index][requested_channel_id])
  except FileNotFoundError:
    print('server_ids.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from server_ids.json')

def load_message(server_index ,message_type):
  s_index = server_index
  requested_message = ''
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      if message_type == "welcome":
        requested_message = ids_data[s_index]["welecome_message"]
        return requested_message
  except FileNotFoundError:
    print('server_ids.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from server_ids.json')

@bot.event
async def on_ready():
    
    print(f'{bot.user.name} is online!')
    for guild in bot.guilds:
      print(f'Guild ID: {guild.id}')
    print(bot.guilds[0])
    first_server_id = bot.guilds[0]
    x = load_channel_id(first_server_id,"new_mem_ch")
    print(f'New member channel: {x}')
    

@bot.event
async def on_member_join(member):
  print(member.guild)
  server_index, new_mem_channel_id = load_channel_id(member.guild, "new_mem_ch")
  print(server_index)
  new_mem = bot.get_channel(new_mem_channel_id)
  if new_mem:
    welcome_message = load_message(server_index, 'welcome')
    await new_mem.send(f'{member.mention}{welcome_message}')
  else:
    print(f'Something is wrong! {new_mem_channel_id} is not found!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)