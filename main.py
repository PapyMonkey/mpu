import discord 

from utils.loader.config_loader import ConfigLoader
from utils.loader.extension_loader import ExtensionLoader
from utils.database import DBManager
from utils.subclass.bot import CustomBot

# intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

aConfig = ConfigLoader()

bot = CustomBot(
    command_prefix = aConfig.get_prefix(),
    intents = discord.Intents.default()
)
bot.database = DBManager()
bot.config = aConfig

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Game("https://github.com/PapyMonkey/mpu")
    )
    print(f'{bot.user} has been successfully connected to Discord.')

if (__name__ == '__main__'):
    aExtLoader = ExtensionLoader(bot)
    aExtLoader.load_extensions()

bot.run(bot.config.get_access_token())
