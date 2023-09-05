import discord
from utils.view.button import ConfirmationButtons

class DropdownMovieSelect(discord.ui.Select):
    def __init__(
        self,
        options_list: list,
        embed_list: list
        ) -> None:
        super().__init__(
            placeholder = "Select the movie...",
            min_values = 1,
            max_values = 1,
            options = options_list,
            row = 2
        )
        self.embed_list = embed_list 

    async def callback(
        self,
        interaction: discord.Interaction
        ) -> None:
        index = int(self.values[0])
        self.view.choice = index
        view = ConfirmationButtons()
        await interaction.response.edit_message(
            content = "Are you sure you want to add this movie ?",
            embed = self.embed_list[index],
            view = view,
        )
        await view.wait()
        # TODO : Change the way we handle logs here
        match view.value:
            case True:
                print("Confirmed...")
                self.view.value = True
                self.view.stop()
            case False:
                print("Cancelled...")
                self.view.value = False
                self.view.stop()
            case None | _:
                print("Timed out...")
                self.view.stop()

class DropdownMovieView(discord.ui.View):
    def __init__(
        self,
        options_list: list,
        embed_list: list
        ) -> None:
        super().__init__()
        self.add_item(DropdownMovieSelect(options_list, embed_list))
        self.value = None
        self.choice = 0
