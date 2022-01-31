import nextcord
from nextcord.ext import commands
import json

class tmp_channels(commands.Cog):

	def __init__(self, client):
		self.client = client

	def get_vowels(self):
		with open("rsc/settings.json", 'r') as fd:
			settings = json.load(fd)
		return settings["vowels_list"]

	def get_parent_chan_list(self, guild):
		with open("rsc/database.json", 'r') as fd:
			database = json.load(fd)
		return database[str(guild.id)]["parent_channels"]

	def get_child_chan_list(self, guild, parent_chan):
		with open("rsc/database.json", 'r') as fd:
			database = json.load(fd)
		return database[str(guild.id)]["parent_channels"][str(parent_chan)]["temporary_channels"]

	def get_template(self, guild, parent_chan):
		with open("rsc/database.json", 'r') as fd:
			database = json.load(fd)
		return database[str(guild.id)]["parent_channels"][str(parent_chan)]["name_template"]

	def put_child_chan_list(self, guild, parent_chan, child_chan):
		with open("rsc/database.json", 'r') as fd:
			database = json.load(fd)
		database[str(guild.id)]["parent_channels"][str(parent_chan)]["temporary_channels"].append(child_chan.id)
		with open("rsc/database.json", 'w') as fd:
			json.dump(database, fd, indent=4)

	def rm_child_chan_list(self, guild, parent_chan, child_chan):
		with open("rsc/database.json", 'r') as fd:
			database = json.load(fd)
		database[str(guild.id)]["parent_channels"][str(parent_chan)]["temporary_channels"].remove(child_chan.id)
		with open("rsc/database.json", 'w') as fd:
			json.dump(database, fd, indent=4)

	@commands.Cog.listener()
	async def	on_voice_state_update(self, member, before, after):
		try:
			for parent_chan in self.get_parent_chan_list(member.guild):
				if (after.channel and member.voice.channel == self.client.get_channel(int(parent_chan))):
					tmp_member_name = member.nick if member.nick else member.name
					tmp_chan_name_prefix = "de "
					for x in self.get_vowels():
						if (x == tmp_member_name[0]):
							tmp_chan_name_prefix = "d'"
							break
					tmp_chan_name = self.get_template(member.guild, parent_chan) + ' ' + tmp_chan_name_prefix + tmp_member_name
					new_tmp_chan = await member.guild.create_voice_channel(tmp_chan_name, category = member.voice.channel.category)
					self.put_child_chan_list(member.guild, parent_chan, new_tmp_chan)
					await member.move_to(new_tmp_chan)
					await new_tmp_chan.set_permissions(member,	view_channel = True,
																manage_channels = True,
																manage_permissions = True,
																create_instant_invite = True,
																connect = True,
																speak = True,
																stream = True,
																use_voice_activation = True,
																priority_speaker = True,
																mute_members = True,
																deafen_members = True,
																move_members = True)
					# break
				child_chan_list = self.get_child_chan_list(member.guild, parent_chan)
				if (before.channel.id in child_chan_list and (not after.channel or before.channel.id != after.channel.id)):
					for id in child_chan_list:
						channel = self.client.get_channel(id)
						if (not channel.members):
							await channel.delete()
							self.rm_child_chan_list(member.guild, parent_chan, channel)
							# break
					# break
		except:
			return

def setup(client):
	client.add_cog(tmp_channels(client))