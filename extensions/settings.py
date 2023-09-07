import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def	_is_valid_id(self, id):
        return True if (id.isnumeric() and len(id) == 18) else False

    settings = SlashCommandGroup(
        "settings",
        "Commands for managing bot and server settings"
    )

    temporary_channels = settings.create_subgroup(
        "tmpchannel",
        "Temporary channels module settings"
    )

    # NOTE : temporary function, need to be upgraded to something more automated later
    @settings.command(name="add_guild")
    async def setup_add_guild(
        self,
        ctx: discord.ApplicationContext,
        search: str):
        if (self._is_valid_id(search)):
            print(self.bot.database.guild_insert(search))

    @temporary_channels.command(name="list_guilds")
    async def list_guilds(self, ctx: discord.ApplicationContext):
        await ctx.send(self.bot.database.list_all_guilds())

    @temporary_channels.command(name="list_parent_chan")
    async def list_parent_chan(self, ctx: discord.ApplicationContext):
        await ctx.send(self.bot.database.list_parent_channels_for_guild(ctx.guild_id))

    # TODO : Add dropdown menu to define parent channel from server generated list
    # HACK : Return an error if setup failed (database error or idk)
    @temporary_channels.command(name="define_chan_creator")
    async def setup_add_parent(
        self,
        ctx:discord.ApplicationContext,
        vocal_id:str
        ) -> None:
        if (self._is_valid_id(vocal_id)):
            insert_result = self.bot.database.parent_chan_insert(ctx.guild_id, vocal_id)
            if (insert_result):
                await ctx.respond(
                    f'Successfully defined {vocal_id} as a channel creator.',
                    ephemeral = True
                )
            else:
                # HACK: maybe change the way we display the error
                await ctx.respond(
                    f'Definition of {vocal_id} as a channel creator failed.',
                    ephemeral = True
                )

    @temporary_channels.command(name="clean_temporary_channel_db")
    async def clean_temporary_channel_db(
        self,
        ctx:discord.ApplicationContext
        ) -> None:
        if self.bot.database.temporary_channel_clean():
            await ctx.respond(
                f'Successfully clean TemporaryChannels DB.',
                ephemeral = True
            )
        else:
            # HACK: maybe change the way we display the error
            await ctx.respond(
                f'Cleanup of TemporaryChannels DB failed.',
                ephemeral = True
            )

    @temporary_channels.command(name="define_template")
    async def define_template(
        self,
        ctx:discord.ApplicationContext,
        vocal_id:str,
        template:str
        ) -> None:
        if (self._is_valid_id(vocal_id)):
            insert_result = self.bot.database.template_update(template, vocal_id)
            if (insert_result):
                await ctx.respond(
                    f'Successfully defined {vocal_id} as a channel creator.',
                    ephemeral = True
                )
            else:
                # HACK: maybe change the way we display the error
                await ctx.respond(
                    f'Definition of {vocal_id} as a channel creator failed.',
                    ephemeral = True
                )

def setup(bot):
    bot.add_cog(Settings(bot))
