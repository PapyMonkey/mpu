from discord.ext import commands

class greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello to the user."""
        await ctx.send("Hi !")

def setup(bot):
    bot.add_cog(greetings(bot))
