import discord
from discord.ext import commands

class tmp_channels(commands.Cog):

	def __init__(self, client):
		self.client = client

	tmp_chan_list = []
	tmp_chan_template = "Salon "
	lst_vowels = "AaEeIiOoUuYy"

	# Methode qui permet de creer des salons temporaires en se connectant dans un salon de base bien defini.
	# A l'avenir, l'utilisateur pourra modifier l'ID de ce salon.
	# @client.event
	@commands.Cog.listener()
	async def	on_voice_state_update(self, member, before, after):
		base_voice = self.client.get_channel(698880918835822644)
		# Check si, apres voice_state_update, l'utilisateur se trouve encore dans un salon
		# ET si c'est le salon pere.
		if (after.channel and member.voice.channel == base_voice):
			# Definit le nom du channel temporaire en fonction de celui de l'utilisateur.
			tmp_member_name = member.nick if member.nick else member.name
			tmp_chan_name_prefix = "de "
			for x in self.lst_vowels :
				if (x == tmp_member_name[0]):
					tmp_chan_name_prefix = "d'"
					break
			tmp_chan_name = self.tmp_chan_template + tmp_chan_name_prefix + tmp_member_name
			tmp_chan_id = await member.guild.create_voice_channel(tmp_chan_name, category = member.voice.channel.category)
			self.tmp_chan_list.append(tmp_chan_id.id)
			print(self.tmp_chan_list)
			await member.move_to(tmp_chan_id)
			await tmp_chan_id.set_permissions(member,	view_channel = True,
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
		elif (before.channel.id in self.tmp_chan_list and (not after.channel or before.channel.id != after.channel.id)):
			for id in self.tmp_chan_list:
				channel = self.client.get_channel(id)
				if (not channel.members):
					await channel.delete()
					self.tmp_chan_list.remove(id)
					break

def setup(client):
	client.add_cog(tmp_channels(client))