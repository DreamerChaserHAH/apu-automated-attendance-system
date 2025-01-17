import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aa

load_dotenv()

discord_token = os.environ['DISCORD_TOKEN']
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='attendance')
async def attendance(ctx, arg):
    aa.attendance(arg)
    await ctx.send('attendance updated')

bot.run(token=discord_token)