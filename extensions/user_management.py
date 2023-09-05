import discord
from discord.ext import commands

class Man_threads(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def thread_create(self, ctx):
        thread = await ctx.channel.create_thread(
            name="Toto les potos",
            auto_archive_duration=60,
            type=discord.ChannelType.private_thread
        )
        await thread.edit(invitable=False)
        await thread.add_user(ctx.author)
        await thread.send("Coucou les potos")

    @commands.command()
    async def clear_threads(self, ctx):
        """Clear all threads (public and private) from this channel."""
        threads_list = ctx.channel.threads
        print(threads_list)
        for thread in threads_list:
            print(thread)
            print(type(thread))
            await thread.delete()

def setup(bot):
    bot.add_cog(Man_threads(bot))
