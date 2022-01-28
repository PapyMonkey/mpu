import	discord 
from discord.ext import commands
import os

token_private = "MzY5NTY3ODY1MDMzOTgxOTUy.WeUI5Q.JiSa9mzwFXS_YXWBGG1dHtW0dTc"

client = commands.Bot(command_prefix = '!')

@client.event
async def	on_ready():
	# await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='Minecraft', url='https://www.twitch.tv/jackmanifoldtv'))
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

client.run(token_private)