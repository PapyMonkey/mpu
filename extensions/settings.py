from config import config
from dataIO import dataIO
from utils import utils
import inspect
import os
import discord
from discord.ext import commands

# BUG : Not working

class settings(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def setup_add_parent(self, ctx):
		func_name = inspect.getframeinfo(inspect.currentframe()).function
		msg = ctx.message.content.replace(config["prefix"] + func_name + ' ', '')
		if (utils._is_valid_id(msg)):
			filepath = utils._db_pathfile(ctx.guild)
			if (dataIO.is_valid_json(filepath)):
				db = dataIO._read_json(filepath)
			else:
				db = {"server_name": str(ctx.guild.name)}
			try:
				db["parent_channels"] += msg
			except KeyError:
				db["parent_channels"] = msg
			dataIO._save_json(filepath, db)
		else:
			await ctx.send("Given ID is not valid. No parent channel has been added to the database.")

	@commands.command()
	async def setup_name_template(self, ctx):
		func_name = inspect.getframeinfo(inspect.currentframe()).function
		msg = ctx.message.content.replace(config["prefix"] + func_name + ' ', '').split(' ', 1)
		print(msg)
		print(msg[0])
		print(msg[1])
		parent_channel_id = msg[0]
		name_template = msg[1]
		if (utils._is_valid_id(msg[0])):
			filepath = utils._db_pathfile(ctx.guild)
			'''
			if (dataIO.is_valid_json(filepath)):
				db = dataIO._read_json(filepath)
			else:
				db = {'parent_channels': {str(parent_channel_id): {'name_template': ''}}, 'server_name': str(ctx.guild.name)}
			# db["parent_channels"][str(msg[0])] = utils.x_to_dico(db["parent_channels"][msg[0]])
			'''
			db = {'parent_channels': {msg[0]: {'name_template': msg[1]}}, 'server_name': str(ctx.guild.name)}
			dataIO._save_json(filepath, db)
		else:
			await ctx.send("Given ID is not valid. No parent channel has been added to the database.")

def setup(client):
	client.add_cog(settings(client))
