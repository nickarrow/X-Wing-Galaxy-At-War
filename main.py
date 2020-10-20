import discord
from discord.ext import commands, tasks
import logging

from datetime import datetime
import json

import secret
import cogs.help

logging.basicConfig(level=logging.INFO)


def getPre(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("!")(bot, message)

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!", "! ")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix, prefix + " ")(bot, message)


client = commands.Bot(command_prefix=getPre, case_insensitive=True, help_command=cogs.help.HelpCommand(),
                      description="This bot allows for players to submit match results within Discord by "
                                  "using the !submit command. The results are then confirmed by the players "
                                  "of the match. After a match result is submitted, players use reactions "
                                  ":white_check_mark: to confirm results, or :x: to reset the submission.")


@client.event
async def on_ready():
    print('---------------------------')
    print(datetime.now())
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('---------------------------')

    game = discord.Game("Galaxy at War")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command(aliases=["setP", "p"])
@commands.has_guild_permissions(manage_guild=True)
async def setPrefix(ctx, *, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f'Prefix set to "{prefix}"')

        with open("prefixes.json", "w") as w:
            json.dump(prefixes, w, indent=4)


async def is_team_member(ctx):
    return list(member for member in (await ctx.bot.application_info()).team.members if not member.id == ctx.message.author.id)


@client.command()
@commands.check(is_team_member)
async def reloadCog(ctx, cog: str):
    client.reload_extension(f"cog.{cog}")
    print(f"Reloading cog {cog}")
    await ctx.send(f"Reloaded cog {cog}", delete_after=3.0)



initial_extensions = (
    "cogs.scoring",
    "cogs.general",
)
for extension in initial_extensions:
    client.load_extension(extension)

client.run(secret.token)
