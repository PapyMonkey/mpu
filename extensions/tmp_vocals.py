import discord
from discord.ext import commands
import utils.view.button as btn

class TmpVocals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class TmpVocalsView(discord.ui.View):
        def __init__(self):
            super().__init__(
                timeout=None
            )
            self.add_item(btn.ButtonRestrictUsersChannel())
            self.add_item(btn.ButtonLimitNumberUserChannel())
    async def _tmp_vocal_create(
        self,
        member,
        after,
        iParentChan
        ):
        if after.channel != None and after.channel.id == iParentChan:
            aTemplateName = self.bot.database.get_name_template(iParentChan)
            aChanName = aTemplateName if aTemplateName != None else 'Room : ' + member.display_name 
            aNewTmpChanName = await member.guild.create_voice_channel(aChanName, category=member.voice.channel.category)
            self.bot.database.temporary_chan_insert(iParentChan, aNewTmpChanName.id)
            await member.move_to(aNewTmpChanName)
            await aNewTmpChanName.set_permissions(member, view_channel=True, manage_channels=True, manage_permissions=True, create_instant_invite=True, connect=True, speak=True, stream=True, use_voice_activation=True, priority_speaker=True, mute_members=True, deafen_members=True, move_members=True)
            await aNewTmpChanName.send("**Channel settings** :", view=self.TmpVocalsView())

    async def _tmp_vocal_remove(
        self,
        before,
        iChildChannelsList
        ):
        if (before.channel != None and before.channel.id in iChildChannelsList):
            for id in iChildChannelsList:
                channel = self.bot.get_channel(id)
                if not channel.members:
                    await channel.delete()
                    self.bot.database.temporary_chan_remove(channel.id)
    
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member:discord.Member,
        before:discord.VoiceState,
        after:discord.VoiceState
        ) -> None:
        try:
            aParentChannelsList = self.bot.database.get_parent_channels_for_guild(member.guild.id)
            for iParentChan in aParentChannelsList:
                await self._tmp_vocal_create(member, after, iParentChan)
                iChildChannelsList = self.bot.database.get_child_channels_for_parent(iParentChan)
                await self._tmp_vocal_remove(before, iChildChannelsList)
        except Exception as E:
            print(f"Error in on_voice_state_update (from TmpVocals): {E}")

def setup(bot):
	bot.add_cog(TmpVocals(bot))
