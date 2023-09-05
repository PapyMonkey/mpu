import discord

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
