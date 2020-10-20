import discord
from discord.ext import commands

import gspread


class Sheet:
    @staticmethod
    async def append(winner: dict,
                     loser: dict) -> int:

        gs = gspread.service_account(filename="cogs/oval-sunset-293015-f7567c7bebce.json")
        spreadsheet = gs.open_by_url(
            "https://docs.google.com/spreadsheets/d/1V4fwxLfwOODZPGYx3es27VK7MyPheJSMBs7G4LhzbtM/")
        worksheet = spreadsheet.worksheet("Bot Data v1")

        col_values = worksheet.col_values("1")
        col_values.pop(0)
        col_values.append(0)
        game_id = int(
            max(int(value) for value in
                (col_values_none for col_values_none in col_values if col_values_none != ''))) + 1

        worksheet.append_row(values=(game_id,
                                     winner["name"],
                                     winner["faction"],
                                     winner["points"],
                                     loser["name"],
                                     loser["faction"],
                                     loser["points"]),
                             table_range="A1")

        col10_values = worksheet.col_values("10")
        col10_values.pop(0)
        col10_values.pop(0)

        for user in (winner, loser):
            if user["name"] not in col10_values:
                worksheet.update_acell(f"J{len(col10_values) + 3}", user["name"])
                col10_values.append(user["name"])

        return game_id

    @staticmethod
    async def change(game_id: int,
                     winner: dict,
                     loser: dict) -> int:

        gs = gspread.service_account(filename="cogs/oval-sunset-293015-f7567c7bebce.json")
        spreadsheet = gs.open_by_url(
            "https://docs.google.com/spreadsheets/d/1V4fwxLfwOODZPGYx3es27VK7MyPheJSMBs7G4LhzbtM/")
        worksheet = spreadsheet.worksheet("Bot Data v1")

        column_a = worksheet.col_values("1")

        # if not str(game_id) in (str(entry) for entry in column_a):
        #     raise ValueError
        #
        # row = 1
        # for entry in column_a:
        #     if not str(entry) == str(game_id):
        #         row += 1
        #     else:
        #         break

        row = list(str(entry) for entry in column_a).index(str(game_id))

        row = worksheet.range(f"B{row}:G{row}")
        row[0].value = winner["name"]
        row[1].value = winner["faction"]
        row[2].value = winner["points"]
        row[3].value = loser["name"]
        row[4].value = loser["faction"]
        row[5].value = loser["points"]

        worksheet.update_cells(cell_list=row)

        return game_id

    @staticmethod
    def get_factions() -> list:
        gs = gspread.service_account(filename="cogs/oval-sunset-293015-f7567c7bebce.json")
        spreadsheet = gs.open_by_url(
            "https://docs.google.com/spreadsheets/d/1V4fwxLfwOODZPGYx3es27VK7MyPheJSMBs7G4LhzbtM/")
        worksheet = spreadsheet.worksheet("Bot Data v1")

        factions = worksheet.col_values("17")
        factions.pop(0)
        factions = list((faction.replace(" ", "").lower() for faction in factions))


        return factions

    @staticmethod
    def get_planets() -> list:
        gs = gspread.service_account(filename="cogs/oval-sunset-293015-f7567c7bebce.json")
        spreadsheet = gs.open_by_url(
            "https://docs.google.com/spreadsheets/d/1V4fwxLfwOODZPGYx3es27VK7MyPheJSMBs7G4LhzbtM/")
        worksheet = spreadsheet.worksheet("Bot Data v1")

        planets = worksheet.col_values("18")
        planets.pop(0)


        return planets
