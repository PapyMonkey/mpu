import	discord 
from discord.ext import commands

token_private = "MzY5NTY3ODY1MDMzOTgxOTUy.WeUI5Q.JiSa9mzwFXS_YXWBGG1dHtW0dTc"

client = commands.Bot(command_prefix = '!')
tmp_chan_list = []
tmp_chan_template = "Salon "
lst_vowels = "AaEeIiOoUuYy"

@client.event
async def	on_ready():
	print("\n---------------------------------------------------------\n")
	print(f'{client.user} has been successfully connected to Discord!')
	print("\n---------------------------------------------------------\n")

@client.command()
async def	hello(ctx):
	await ctx.send("Coucou !")

@client.command(pass_context = True)
async def	join(ctx):
	if (ctx.author.voice):
		channel = ctx.message.author.voice.channel
		await channel.connect()
	else:
		await ctx.send("Tu dois de trouver dans un salon vocal pour pouvoir executer cette commande.")

@client.command(pass_context = True)
async def	leave(ctx):
	if (ctx.voice_client):
		await ctx.guild.voice_client.disconnect()
		await ctx.send("J'ai quitte le salon vocal.")
	else:
		await ctx.send("Je ne me trouve pas dans un salon vocal !")

# Methode qui permet de creer des salons temporaires en se connectant dans un salon de base bien defini.
# A l'avenir, l'utilisateur pourra modifier l'ID de ce salon.
@client.event
async def	on_voice_state_update(member, before, after):
	base_voice = client.get_channel(698880918835822644)
	# Check si, apres voice_state_update, l'utilisateur se trouve encore dans un salon
	# ET si c'est le salon pere.
	if (after.channel and member.voice.channel == base_voice):
		# Definit le nom du channel temporaire en fonction de celui de l'utilisateur.
		tmp_member_name = member.nick if member.nick else member.name
		tmp_chan_name_prefix = "de "
		for x in lst_vowels :
			if (x == tmp_member_name[0]):
				tmp_chan_name_prefix = "d'"
				break
		tmp_chan_name = tmp_chan_template + tmp_chan_name_prefix + tmp_member_name
		tmp_chan_id = await member.guild.create_voice_channel(tmp_chan_name, category = member.voice.channel.category)
		tmp_chan_list.append(tmp_chan_id)
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
	elif (before.channel in tmp_chan_list and before.channel != after.channel):
		for i in tmp_chan_list:
			if (not i.members):
				await i.delete()
				tmp_chan_list.remove(i)
				break

@client.command()
async def	voice_check(ctx):
	base_voice = client.get_channel(935450508372635678)
	members = base_voice.members
	print(members)

client.run(token_private)