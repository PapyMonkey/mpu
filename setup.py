from config import config
import discord 
from discord.ext import commands
import os

from libs.views import MyView

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix = config["prefix"],
    intents = intents
)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Game("https://github.com/PapyMonkey/mpu")
    )
    print(f'{bot.user} has been successfully connected to Discord.')

# @bot.slash_command()
# @bot.slash_command(
#     guild_ids=[470340987064025089],
#     description="Juste un petit coucou!"
# )
# async def hello(ctx):
#     await ctx.respond("Hello!")

initial_extensions = []

for filename in os.listdir('cogs'):
    if (filename.endswith('.py')):
        initial_extensions.append("cogs." + filename[:-3])

if (__name__ == '__main__'):
    for extension in initial_extensions:
        bot.load_extensions(extension)

@bot.command()
async def button(ctx):
    await ctx.send("This is a button!", view=MyView()) # Send a message with our View class that contains the button

bot.run(config["access_token"])
