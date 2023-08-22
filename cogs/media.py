import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from media import radarr

class MediaCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.radarr_client = radarr.RadarrClient()


    class ConfirmationView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
        async def confirm_callback(
            self,
            button: discord.ui.Button,
            interaction: discord.Interaction
        ) -> None:
            await interaction.response.send_message("Confirming...", ephemeral=True)
            self.value = True
            self.stop()

        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji='⛔')
        async def cancel_callback(
            self,
            button: discord.ui.Button,
            interaction: discord.Interaction
        ) -> None:
            await interaction.response.send_message("Canceling...", ephemeral=True)
            self.value = False
            self.stop()

    class DropdownSelectMovie(discord.ui.Select):
        """
        A custom dropdown menu component for selecting a movie.

        This class extends the `Select` component provided by the `discord.ext.commands` module.
        It creates a dropdown menu specifically designed for selecting a single movie.
        Attributes:
            options_list (list): A list of options to populate the dropdown menu with.

        Methods:
            callback(interaction): An asynchronous callback method triggered when an option is selected.
                It is called with the selected `interaction` object.
        """

        def __init__(
            self,
            instance_parent,
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
            self.instance_parent = instance_parent
            self.embed_list = embed_list 

        async def callback(
            self,
            interaction: discord.Interaction
            ) -> None:
            index = int(self.values[0])
            await interaction.response.send_message(
                content = "Are you sure you want add this movie ?",
                embed = self.embed_list[index],
                ephemeral = True,
                view = self.instance_parent.ConfirmationView()
            )
        
    # --------------------------------------------------------------------------
    # Methods

    def __create_dropdown_option_obj(
            self,
            index: str,
            movie_obj: radarr.MovieObj
        ) -> discord.SelectOption:
        """Define an option (label/description/number) for the dropdown menu."""
        return discord.SelectOption(
            label = movie_obj.title,
            description = index, # TODO : remove in the end
            value = index,
            emoji = None,
            default = False
        )

    # TODO: Change this definition by using the dedicated method to convert dict into embed
    def __create_embed_obj(
            self,
            movie_obj: radarr.MovieObj
        ) -> discord.Embed:
        return discord.Embed(
            title = str(movie_obj.title),
            color = 0x00ff00,
            description = str(movie_obj.synopsis),
            fields = [
                discord.EmbedField(
                    name = 'Movie length',
                    value = str(movie_obj.runtime),
                    inline = True
                ),
                discord.EmbedField(
                    name = 'Status',
                    value = str(movie_obj.status).capitalize(),
                    inline = True
                ),
                discord.EmbedField(
                    name = 'Release date',
                    value = str(movie_obj.date_released),
                    inline = True
                ),
                discord.EmbedField(
                    name = 'Available on Plex ?',
                    value = str(movie_obj.has_file).capitalize(),
                    inline = True
                ),
                discord.EmbedField(
                    name = 'Genre.s',
                    value = str(movie_obj.genres),
                    inline = True
                ),
                discord.EmbedField(
                    name = 'Link.s',
                    value = self.__init_urls(movie_obj),
                    inline = False
                ),
            ],
        )

    def __init_urls(
            self,
            movie_obj: radarr.MovieObj
        ) -> str:
        """Define all available links based on json provided by Radarr api."""

        # Filters all 'movie_obj' ending in '_url'
        attributes_to_link = [attr for attr in dir(movie_obj) if attr.endswith("_url")]

        links = []
        for attr_name in attributes_to_link:
            attr_value = getattr(movie_obj, attr_name)
            if attr_value:
                link_name = attr_name.replace("_url", "").capitalize()
                links.append(f"- [{link_name}]({attr_value})")
        return "\n".join(links)

    def __create_page_obj(
            self,
            movie_obj: radarr.MovieObj,
            embed_obj: discord.Embed
        ):
        page = embed_obj
        page.set_thumbnail(url = movie_obj.poster_image)
        return page

    def __create_pages_search(
            self,
            search: str
        ) -> pages.Paginator:
        self.radarr_client.def_array_movies(search)

        # Add embed/pages/options to some empty lists
        self.embed_list = []
        self.movie_pages_list = []
        self.dropdown_options_list = []
        for index, movie in enumerate(self.radarr_client.movies_list):
            self.embed_list.append(self.__create_embed_obj(movie))
            self.movie_pages_list.append(self.__create_page_obj(movie, self.embed_list[index]))
            self.dropdown_options_list.append(self.__create_dropdown_option_obj(str(index), movie))

        return pages.Paginator(
            pages=self.movie_pages_list,
            disable_on_timeout=False
        )

    # --------------------------------------------------------------------------
    # Commands

    media = SlashCommandGroup(
        "media",
        "Commands for managing Plex Media Server with Radarr/Sonarr APIs."
    )

    @media.command(name="search_movie")
    async def search_movie(
            self,
            ctx: discord.ApplicationContext,
            search: str):
        """Search a movie on IMDB/TMDB with Radarr API calls."""
        paginator = self.__create_pages_search(search)

        # Send datas to the channel/thread
        await paginator.respond(
            ctx.interaction,
            ephemeral=False
        )

    @media.command(name="add_movie")
    async def add_movie(
            self,
            ctx: discord.ApplicationContext,
            search: str):
        paginator = self.__create_pages_search(search)
        await paginator.respond(
            ctx.interaction,
            ephemeral=False
        )
        await ctx.respond(
            "Choose the movie you want to add to the Plex library :",
            view = discord.ui.View(self.DropdownSelectMovie(
                self,
                self.dropdown_options_list,
                self.embed_list
            ))
        )

    @media.command(name="test_radarr_json")
    async def radarr_test(
            self,
            ctx: discord.ApplicationContext,
            search: str):
        import json
        json_array = self.radarr_client.search_movie(search)
        print(json.dumps(json_array[0], indent=4))

def setup(bot):
    bot.add_cog(MediaCmds(bot))
