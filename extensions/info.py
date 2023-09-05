from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @bot.event
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandNotFound):
    #         await ctx.send(f'Command not found. Use `{bot.command_prefix}help` to see available commands.')

    @commands.command()
    async def ping(self, ctx):
        """Measures the bot's latency."""
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)} ms')

def setup(bot):
    bot.add_cog(Info(bot))
