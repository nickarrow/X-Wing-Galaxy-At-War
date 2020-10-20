import discord
from discord.ext import commands

import asyncio

import main
from cogs import sheets
import random

import re


class Scoring(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.factions = sheets.Sheet.get_factions()
        self.planets = sheets.Sheet.get_planets()

    @commands.command()
    @commands.guild_only()
    async def submit(self, ctx: commands.Context, player1: str, player1points: int, vs: str, player2: str, player2points: int):

        self.client.get_command(
            "submit").help = f"""Use: "{main.getPre(self.client, ctx)[2]}submit <@player1> <player1points> vs <@player2> <player2points>" to submit your game."""

        try:
            player1 = ctx.guild.get_member(int("".join(re.split("[^0-9]", player1))))
            player2 = ctx.guild.get_member(int("".join(re.split("[^0-9]", player2))))
            if not player1 or not player2:
                raise ValueError
        except ValueError:
            raise ValueError(
                f"Wrong Form. Mention both players: {main.getPre(self.client, ctx)[2]}submit <@player1> <player1points> vs <@player2> <player2points>")

        if vs not in ("vs", "v.", "|", "vs.", "versus"):
            raise ValueError(
                f"Wrong Form. Use: {main.getPre(self.client, ctx)[2]}submit <@player1> <player1points> vs <@player2> <player2points>")

        if player1.id == player2.id:
            raise ValueError(f'Duh. You have to ping different Users.')

        if ctx.message.author not in (player1, player2):
            raise ValueError(
                "You can only submit your own games."
            )

        if player1points <= -1 or player2points <= -1:
            raise ValueError(f"Players can't have negative scores.")

        if player1points < player2points:
            player1, player1points, player2, player2points = player2, player2points, player1, player1points

        winner, loser = None, None

        for role in self.factions:
            if role in (roles.name.replace(" ", "").lower() for roles in player1.roles):
                winner = {
                    "name": player1.name,
                    "faction": role,
                    "points": player1points
                }
            if role in (roles.name.replace(" ", "").lower() for roles in player2.roles):
                loser = {
                    "name": player2.name,
                    "faction": role,
                    "points": player2points
                }

        if winner is None or loser is None:
            raise ValueError("Both Players need a faction role.")

        message = await ctx.channel.send(embed=discord.Embed(
            title=f"Match: {winner['name']} {winner['points']} vs {loser['name']} {loser['points']}",
            description=f"{player2.mention} and {player1.mention}, please react with :white_check_mark: to confirm or with :x: to reset.",
            colour=discord.Colour.from_rgb(101, 104, 133)))

        await message.add_reaction("✅")
        await message.add_reaction("❌")

        players = [player1, player2]

        def check(r, u):
            if not r.message.id == message.id:
                return False
            if str(r) == "✅":
                if u.id in (player.id for player in players):
                    players.remove(u)
            elif str(r) == "❌":
                if u.id in (player.id for player in [player1, player2]):
                    return True

            if not players:
                return True
            return False

        r, u = await self.client.wait_for('reaction_add', check=check)

        if str(r) == "❌":
            await message.delete()
            raise InterruptedError(f"{u.mention} canceled the Submission.")

        ret = await sheets.Sheet.append(winner, loser)

        await message.delete()
        await ctx.message.delete()

        await ctx.send(embed=discord.Embed(title=f"Match {ret} - Battle of {random.choice(self.planets)}",
                                           description=f"**Winner: {(list((role for role in player1.roles if role.name.replace(' ', '').lower() in self.factions))[0]).mention}**\n"
                                                       f"**Standing: {winner['name']} {winner['points']} vs {loser['name']} {loser['points']}**",
                                           colour=discord.Colour.from_rgb(101, 104, 133)))

    @submit.error
    async def submit_handler(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send(
                f"**Submission Error**\n{str(error).split(': ')[-1]} Use: {main.getPre(self.client, ctx)[2]}submit <@player1> <player1points> vs <@player2> <player2points>",
                delete_after=30.0)
            await asyncio.sleep(30.0)
            await ctx.message.delete()

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"**Submission Error**\n{str(error).split(': ')[-1]} Use: {main.getPre(self.client, ctx)[2]}submit <@player1> <player1points> vs <@player2> <player2points>",
                delete_after=30.0)
            await asyncio.sleep(30.0)
            await ctx.message.delete()
        else:
            await ctx.send("**Submission Error**\n" + str(error).split(': ')[-1], delete_after=30.0)
            await asyncio.sleep(30.0)
            await ctx.message.delete()



def setup(client):
    client.add_cog(Scoring(client))
