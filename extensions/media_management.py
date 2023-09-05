import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
from services import radarr
from utils.view import dropdown

class MediaCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.radarr_client = radarr.RadarrClient()

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
            description = index,  # TODO : remove in the end
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
        "Commands for managing Plex Media Server with Arr's APIs."
    )
    radarr = media.create_subgroup(
        "movie",
        "Radarr (movies) commands"
    )

    @radarr.command(name="search")
    @discord.option("search", description="Enter the movie you are looking for")
    async def movie_search(
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

    @radarr.command(name="add")
    @discord.option("search", description="Enter the movie you are looking for")
    async def movie_add(
            self,
            ctx: discord.ApplicationContext,
            search: str):
        """Search a movie and add it to the Plex Media Server."""
        paginator = self.__create_pages_search(search)
        await paginator.respond(
            ctx.interaction,
            ephemeral=False
        )
        view = dropdown.DropdownMovieView(
            self.dropdown_options_list,
            self.embed_list
        )
        await ctx.respond(
            "Choose the movie you want to add to the Plex library :",
            view = view
        )
        await view.wait()
        match view.value:
            case True:
                self.radarr_client.add_movie(self.radarr_client.search_array[view.choice])

def setup(bot):
    bot.add_cog(MediaCmds(bot))
