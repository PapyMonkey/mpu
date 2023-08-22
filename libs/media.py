# import discord
# from discord.ext import commands

from pyarr import RadarrAPI

class search_radarr():

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(search_radarr(bot))
