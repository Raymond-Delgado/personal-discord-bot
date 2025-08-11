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

bot = commands.Bot(command_prefix='tc_', intents = intents)

def load_bad_words_array():
  try:
    with open('bad_words.json', 'r') as read_file:
      bw_array = json.load(read_file)
      return bw_array
  except FileNotFoundError:
    print('bad_words.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from bad_words.json')


def load_guild_index(requested_guild_id):
  g_index = 0
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      for index in ids_data:
        if requested_guild_id == index["guild_id"]:
          g_index = index
      return g_index
  except FileNotFoundError:
    print('server_ids.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from server_ids.json')

def load_id(requested_guild_id, requested_id, requested_id_category):
  g_index = load_guild_index(requested_guild_id)
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      if requested_id_category == 'channel':
        return g_index, ids_data[g_index]["channels"][requested_id]
      elif requested_id_category == 'role':
        return ids_data[g_index]["roles"][requested_id]
  except FileNotFoundError:
    print('server_ids.json not found')
    return None
  except json.JSONDecodeError:
    print('Error decoding JSON from server_ids.json')

def load_message(requested_guild_id ,message_type):
  g_index = load_guild_index(requested_guild_id)
  requested_message = ''
  try:
    with open('server_ids.json', 'r') as read_file:
      ids_data = json.load(read_file)
      if message_type == "welcome":
        requested_message = ids_data[g_index]["messages"]["welecome_msg"]
        return requested_message
      elif message_type == 'bw_warning':
        requested_message = ids_data[g_index]["messages"]["bw_warning_msg"]
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
    first_guild_id = bot.guilds[0]
    print(load_guild_index(first_guild_id))
    x = load_id(first_guild_id,"new_member_ch","channel")
    y = load_id(first_guild_id, 'admin', 'role')
    print(f'New member channel: {x}')
    print(f'Admin role: {y}')
    

@bot.event
async def on_member_join(member):
  server_index, new_member_ch_id = load_id(member.guild, "new_member_ch", "channel")
  new_mem = bot.get_channel(new_member_ch_id)
  if new_mem:
    welcome_message = load_message(server_index, 'welcome')
    await new_mem.send(f'{member.mention}{welcome_message}')
  else:
    print(f'Something is wrong! {new_member_ch_id} is not found!')
  
@bot.event
async def on_message(message):
  guild = message.guild
  bad_words = load_bad_words_array()
  admin_role_id = load_id(message.guild, 'admin', 'role')
  admin_role = discord.utils.get(guild.roles, id = admin_role_id)
  if message.author == bot.user:
    return
  for word in bad_words:
    if word in message.content.lower():
      for member in guild.members:
        if admin_role in member.roles:
          try:
            if member.dm_channel is None:
              await member.create_dm()
            await member.dm_channel.send(f'A message from {message.author} was flagged and deleted \n- Message content: {message.content}\n- Message sent at: {message.created_at}')
          except discord.Forbidden:
            await message.channel.send(f'{member.mention}, I was unable to send you a DM. Please check your DM settings for your account')
            print(f'Could not send message to {member.name}. (DMs disabled or blocked)')
          except Exception as e:
            print(f'Error sending message to {member.name}: {e}')
      bw_warning_msg = load_message(message.guild, 'bw_warning')
      await message.delete()
      await message.channel.send(f'{message.author.mention}{bw_warning_msg}')
  await bot.process_commands(message)

@bot.command()
async def commands(ctx):
  await ctx.send(f'''
Hello {ctx.author.mention}!
Here is a list of the commands that you can use:
- tc_commands: Lists the commands that are available.
''')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)