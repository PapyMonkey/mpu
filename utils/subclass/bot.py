from discord.ext import commands

from utils.database import DBManager
from utils.loader.config_loader import ConfigLoader

class CustomBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database: DBManager
        self.config: ConfigLoader
