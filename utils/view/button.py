import discord
from abc import abstractmethod

# HACK: Refactor this to button classes and a custom view class
class ConfirmationButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(
        label='Confirm',
        style=discord.ButtonStyle.green,
        emoji='✅'
    )
    async def confirm_callback(
        self,
        button: discord.ui.Button,
        interaction: discord.Interaction
    ) -> None:
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        # await interaction.response.send_message("Confirming...", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(
        label='Cancel',
        style=discord.ButtonStyle.red,
        emoji='⛔'
    )
    async def cancel_callback(
        self,
        button: discord.ui.Button,
        interaction: discord.Interaction
    ) -> None:
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        # await interaction.response.send_message("Canceling...", ephemeral=True)
        self.value = False
        self.stop()

class TmpChanBaseButton(discord.ui.Button):
    @staticmethod
    async def send_error(interaction:discord.Interaction) -> None:
        await interaction.response.send_message(
            f"Error: you can not use this command as you are not an admninistrator of this temporary channel",
            ephemeral=True,
            delete_after=15
        )

    @staticmethod
    async def send_success(interaction:discord.Interaction) -> None:
        await interaction.response.send_message(
            f"✅ Action successfully executed !",
            ephemeral=True,
            delete_after=15
        )

    async def callback(
        self,
        interaction:discord.Interaction
        ) -> None:
        """
        This function will be called any time a user clicks on this button.

        Parameters
        ----------
        interaction: :class:`discord.Interaction`
            The interaction object that was created when a user clicks on a button.
        """
        aUser = interaction.user
        if (interaction.channel.permissions_for(aUser).administrator):
            await self.button_action(interaction)
            await self.send_success(interaction)
        else:
            await self.send_error(interaction)

    @abstractmethod
    async def button_action(
        self,
        interaction:discord.Interaction
        ) -> None:
        pass


class ButtonLimitNumberUserChannel(TmpChanBaseButton):
    def __init__(self):
        super().__init__(
            label='Limit to the current number of users',
            style=discord.ButtonStyle.blurple,
            emoji='🔒'
        )

    async def button_action(
        self,
        interaction:discord.Interaction
        ) -> None:
        aNumberUsersInChan = len(interaction.channel.members)
        await interaction.channel.edit(user_limit=aNumberUsersInChan)

class ButtonRestrictUsersChannel(TmpChanBaseButton):
    def __init__(self):
        super().__init__(
            label='Restrict access to current users',
            style=discord.ButtonStyle.blurple,
            emoji='🔒'
        )

    async def button_action(
        self,
        interaction:discord.Interaction
        ) -> None:
        aRoleEveryone = discord.utils.get(interaction.guild.roles, name="@everyone")
        await interaction.channel.set_permissions(aRoleEveryone, connect = False)
        for aUserIter in interaction.channel.members:
            await interaction.channel.set_permissions(aUserIter, connect = True)
