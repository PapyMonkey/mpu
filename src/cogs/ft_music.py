import discord
from discord.ext import commands

class music(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(pass_context=True)
	async def join(self, ctx):
		if (ctx.author.voice):
			channel = ctx.message.author.voice.channel
			await channel.connect()
		else:
			await ctx.send("Tu dois de trouver dans un salon vocal pour pouvoir executer cette commande.")


	@commands.command(pass_context=True)
	async def leave(self, ctx):
		if (ctx.voice_client):
			await ctx.guild.voice_client.disconnect()
			await ctx.send("J'ai quitte le salon vocal.")
		else:
			await ctx.send("Je ne me trouve pas dans un salon vocal !")

def setup(client):
	client.add_cog(music(client))