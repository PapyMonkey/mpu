from src.config import config
import os
import discord 
from discord.ext import commands

client = commands.Bot(command_prefix = config["prefix"])

@client.event
async def	on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("https://github.com/PapyMonkey/mpu"))
    print("\n*-------------------------------------------------------*")
    print("|\t\t\t\t\t\t\t|")
    print(f"| {client.user} has been successfully connected to Discord ! |")
    print("|\t\t\t\t\t\t\t|")
    print("*-------------------------------------------------------*\n")

initial_extensions = []

for filename in os.listdir('src/cogs'):
    if (filename.endswith('.py')):
        initial_extensions.append("cogs." + filename[:-3])

if (__name__ == '__main__'):
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(config["access_token"])
