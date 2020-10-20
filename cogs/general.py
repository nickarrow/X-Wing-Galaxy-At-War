import asyncio

import discord
from discord.ext import commands

import main



async def is_team_member(ctx):
    return list(member for member in (await ctx.bot.application_info()).team.members if not member.id == ctx.message.author.id)


class General(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command(hidden=True)
    @commands.check(is_team_member)
    async def clear(self, ctx, amount=5):
        if amount <= 0:
            raise ValueError(f'**Why are you trying to delete "{amount}" messages? What is wrong with you? Please use your fucking brain ONCE in your entire fucking life ok?**')
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(content=f'You have deleted {amount} messages!', delete_after=3.0)

    @clear.error
    async def clear_handler(self, ctx, error):
        await ctx.message.delete()
        await ctx.send(str(error).split(': ')[-1], delete_after=30.0)


def setup(client):
    client.add_cog(General(client))
