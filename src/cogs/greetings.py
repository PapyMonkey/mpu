import discord
from discord.ext import commands

class greetings(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def	hello(ctx):
		await ctx.send("Hi !")

def setup(client):
	client.add_cog(greetings(client))