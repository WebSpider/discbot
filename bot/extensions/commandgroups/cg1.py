from discord.abc import PrivateChannel
from discord.ext.commands import Cog, command
from bot.config import settings
from helpers import

DEBUG = settings.get('DEBUG', False)

# A workflow is a list of arrays. Each array has at least a "step" key, to identify the step
cg1_workflow = [
    {
        "step": "title1",
        "choices": {
            "1": "Choice 1",
            "2": "Choice 2"
        },
        "replies": {
            "1": "Emoji 1",
            "2": "Emoji 2"
        },
        "message": "Hello"
    },
    {
        "step": "title2",
        "choices": {
            "1": "Choice 1",
            "2": "Choice 2"
        },
        "replies": {
            "1": "Emoji 1",
            "2": "Emoji 2"
        },
        "message": "Goodbye"
    }
]


class CommandGroup1(Cog, name="Command Group One"):
    def __init(self, this_bot):
        self.bot = this_bot
        self._last_member = None

    @command(name='example1', brief='Example One')
    async def handle_cmd_example1(self, ctx):
        await _cmd_example1(ctx)

    @Cog.listener()
    async def on_reaction_add(self, reaction, react_user):
        print('{} added reaction {} to message {}'.format(react_user.display_name, reaction.emoji, reaction.message.id))
        await handle_reaction(reaction, react_user, self.bot.user, self.bot)

async def _cmd_example1(ctx):
    # Do some stuff like send an initial hello message here
    await ctx.send(content="Example")

async def handle_reaction(reaction, user, botuser, bot):
    """
    Generic reaction handler for this Cog

    :param reaction: Discord Reaction that triggered this handler
    :param user: User that authored the Discord Reaction
    :param botuser: User this bot is
    :param bot: This bot
    :return: Action taken as a result of this action
    """
    if DEBUG:
        print("DEBUG: I am now handling reaction {} for user {} ({})".format(str(reaction), user, user.id))

    if reaction.message.author != bot.user:
        # Only act on my own messages
        if DEBUG:
            print("DEBUG: The message reacted to wasnt mine, but {}. I am done here.".format(reaction.message.author))
            return True

    if user.id == botuser.id:
        # Never act if I reacted myself
        if DEBUG:
            print("DEBUG: I addded this reaction. Skipping further steps")
        return True
    else:

        if DEBUG:
            print("DEBUG: USER {} reacted to {} from {} with {}".format(user, reaction.message.id,
                                                                        reaction.message.author, reaction))

        channel = bot.get_channel(reaction.message.channel.id)
        if isinstance(channel, PrivateChannel):
            is_dm = True
        else:
            is_dm = False

        selection = convert_from_emoji(str(reaction))
        if is_dm:
            if DEBUG:
                print('DEBUG: This is a DM')

            if not selection:
                if DEBUG:
                    print("DEBUG: Reaction {} on message {} makes nosense to me. Removing".format(reaction,
                                                                                                  reaction.message.id))
                return await user.send(content="Well, that's not a valid choice. Try again.")

            return await process_actions_from_reaction(reaction, selection, dm=True)


        else:
            if DEBUG:
                print('DEBUG: This is not a DM')

            usermsg = get_usermsg(user.id)
            if DEBUG:
                print('DEBUG: Userdetail: {}'.format(usermsg))
                print('DEBUG: Message reacted on {}'.format(reaction.message.id))

            if usermsg == reaction.message.id:
                if DEBUG:
                    print('DEBUG: User {} is reacting to my last message, validating reaction and proceeding'.format(user))
                if not selection:
                    if DEBUG:
                        print("DEBUG: Reaction {} on message {} makes nosense to me. Removing".format(reaction,
                                                                                                  reaction.message.id))
                    return await reaction.remove(user)

                await reaction.message.clear_reactions()

                return await process_actions_from_reaction(reaction, selection, dm=True)

        channel = bot.get_channel(reaction.message.channel.id)
        if isinstance(channel, PrivateChannel):
            pass

        else:
            await reaction.remove(user)
            return await channel.send(content="Well thanks {}, but that's not your command.\n"
                                              "Please type `.help` get some help on issuing commands".format(user.mention))

def setup(bot):
    bot.add_cog(CommandGroup1(bot))