#    DiscBot - A Framework for Discord bots
#    Copyright (C) 2021 Nils Vogels (WebSpider)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
# noinspection PyPackageRequirements
from discord.ext.commands import Bot, when_mentioned_or
# noinspection PyPackageRequirements
from discord import Intents, Game, Status, __version__ as discversion
from config import settings

DEBUG = settings.get('DEBUG', False)

print("Intializing...")
if DEBUG:
    print('DEBUG: Debug enabled')


def get_prefix(bot, message):
    """
    Callable to determine the needed prefix for the bot to act on

    :param bot: The Discord Bot to interact with
    :param message: The Discord Message we are referring to
    :return: relevant prefixes
    """

    prefixes = ['.', '.  ']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # No mentions in a guild
        return ['.', '. ']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return when_mentioned_or(*prefixes)(bot, message)


description = '''I am a framework'''

botintents = Intents.default()
botintents.reactions = True
botintents.messages = True
botintents.members = True

print("Data read. Starting Discord connection")

bot = Bot(command_prefix=get_prefix, description=description, intents=botintents)

# This is a list of extensions to call. Defauls to an extension that can dynamically include other extensions it finds
initial_extensions = ['extensions.extensionloader']

if __name__ == '__main__':
    sys.path.append('.')
    sys.path.append('..')
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_connect():
    print('Connected to Discord, getting personality info')


@bot.event
async def on_ready():
    print('\n\nReporting for duty as {} ({}) with version {}'.format(bot.user.name, bot.user.id, discversion))
    await bot.change_presence(status=Status.idle, activity=Game(name='Frameworking'))
    print(f'Successfully logged in and booted...!')

bot.run(settings["bot_token"])
