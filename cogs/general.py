import asyncio

import discord
from discord.ext import commands

import main



async def is_team_member(ctx):
    return list(member for member in (await ctx.bot.application_info()).team.members if member.id == ctx.message.author.id)


class General(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    @commands.check(is_team_member)
    async def clear(self, ctx, amount=5):
        if amount <= 0:
            raise ValueError(f'''You can't delete {amount} messages.''')
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(content=f'You have deleted {amount} messages!', delete_after=3.0)

    @clear.error
    async def clear_handler(self, ctx, error):
        await ctx.message.delete()
        await ctx.send(str(error).split(': ')[-1], delete_after=30.0)


def setup(client):
    client.add_cog(General(client))
