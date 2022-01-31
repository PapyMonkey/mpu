from config import config
import os
import nextcord 
from nextcord.ext import commands

client = commands.Bot(command_prefix = config["prefix"])

@client.event
async def	on_ready():
    await client.change_presence(status=nextcord.Status.do_not_disturb)
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
