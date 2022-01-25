import	os

import	discord 
from	dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

token_private = "MzY5NTY3ODY1MDMzOTgxOTUy.WeUI5Q.JiSa9mzwFXS_YXWBGG1dHtW0dTc"

client = discord.Client()

@client.event
async def	on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def	on_message(msg):
	if msg.author == client.user:
		return

	if msg.content == "Channel":
		await msg.channel.send(f"{msg.channel}")
		print(f'Channel : {msg.channel}.')

	if msg.content == "Ping":
		await msg.channel.send("Pong")

	if msg.content == "Voice status":
		await msg.channel.send(VoiceClient.is_connected())

@client.event
async def	on_group_join(chan, usr):
	print("coucou")
	print("%s has connected to %s.", usr.name, chan.name)

client.run(token_private)