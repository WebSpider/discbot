from discord import Embed, Color
from datetime import datetime
from external import git_version


def reformat(title, descr, msg, bot, field_hdr=None, color=Color.default()):
    embed = Embed(title=title, description=descr, color=color, timestamp=datetime.utcnow())
    embed.add_field(name=field_hdr, value=msg)
    embed = add_footer(embed=embed, bot=bot)
    return embed


def notimplemented(bot):
    embed = Embed(title="Not implemented",
                  description="This function is not yet implemented", timestamp=datetime.utcnow())
    embed = add_footer(embed=embed, bot=bot)
    return embed


def add_footer(embed, bot):
    botname = bot.display_name
    git_hash = git_version()
    embed.set_footer(text='{} ({}) - '.format(botname, git_hash))
    return embed
