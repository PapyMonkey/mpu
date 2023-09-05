import discord 
from discord.ext import commands
from utils.loader.config_loader import ConfigLoader
from utils.loader.extension_loader import ExtensionLoader

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

iConfig = ConfigLoader()
bot = commands.Bot(
    command_prefix = iConfig.get_prefix(),
    intents = intents
)

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

bot.run(iConfig.get_access_token())
