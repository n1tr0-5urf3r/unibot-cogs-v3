from redbot.core import commands
import datetime
import requests
import re
from discord.utils import get
import discord

client = discord.Client()


class Unibot(commands.Cog):

    @commands.command(pass_context=True, aliases=["Mensa"])
    async def mensa(self, ctx, *, subcommand=None):

        return await ctx.send("\n \n⚠️ ⚠️ ⚠️\n 🇩🇪 Präfix `!` ist veraltet! Bitte nutze ab sofort Slash commands mit Präfix `/` \n \n 🇬🇧 Prefix `!` is deprecated! Please use the slash command with prefix `/` from now on.")


        def embed_list_lines(embed,
                             lines,
                             field_name,
                             max_characters=1024,
                             inline=False):
            zero_width_space = u'\u200b'
            value = "\n".join(lines)
            if len(value) > 1024:
                value = ""
                values = []
                for line in lines:
                    if len(value) + len(line) > 1024:
                        values.append(value)
                        value = ""
                    value += line + "\n"
                if value:
                    values.append(value)
                embed.add_field(name=field_name,
                                value=values[0], inline=inline)
                for v in values[1:]:
                    embed.add_field(name=zero_width_space,
                                    value=v, inline=inline)
            else:
                embed.add_field(name=field_name, value=value, inline=inline)
            return embed

        def next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return d + datetime.timedelta(days_ahead)

        def get_data(id):
            # Get data
            url_mensa = "https://www.my-stuwe.de/wp-json/mealplans/v1/canteens/{}?lang=de".format(
                id)
            r = requests.get(url_mensa)
            r.encoding = 'utf-8-sig'
            data = r.json()
            return data

        def build_menu(data, caf=False):
            menu = []
            menu_cur_day = []
            for id in data:
                # If meal matches today
                if str(day.date()) in id["menuDate"]:
                    # Collect meal for this day
                    if caf:
                        menuLine = "Cafeteria"
                    else:
                        menuLine = id["menuLine"]
                    if "Dessert" not in menuLine and "Beilagen" not in menuLine and "Salat" not in menuLine:
                        price = id["studentPrice"]
                        # Append newline to last entry
                        if id["menu"]:
                            id["menu"][-1] = id["menu"][-1] + "\n"
                        for food in id["menu"]:
                            if caf:
                                if re.match("^Pommes frites$", food):
                                    continue
                            food = "-{}".format(food)
                            menu.append(food)
                        if not menu:
                            continue
                        # menu is fully available, build string
                        menu_cur_day.append(
                            ["*{} - {}€*".format(menuLine, price)])
                        menu_cur_day.append(menu)
                        # Reset menu
                        menu = []
            return menu_cur_day

        # Get time stuff
        today = datetime.datetime.now()
        cal_week = today.strftime("%W")
        weekday = datetime.datetime.today().weekday()
        week_start = today - datetime.timedelta(days=weekday)
        week_end = today + datetime.timedelta(days=4 - weekday)
        heute_flag = False

        color = discord.Colour.magenta()
        mensa_id = "621"  # Tuebingen Morgenstelle
        caf_id = "724"
        emoji_map = {"[S]": "[ :pig2: ]",
                     "[R]": "[ :cow2: ]",
                     "[S/R]": "[ :pig2: / :cow2: ]",
                     "[F]": "[ :fish: ]",
                     "[G]": "[ :rooster: ]",
                     "[V]": "[ :seedling: ]",
                     "[L]": "[ :sheep: ]",
                     "[W]": "[ :deer: ]",
                     "[vegan]": "[ <:vegan:643514903029743618> ]",
                     "Tagesmenü -": ":spaghetti: Tagesmenü -",
                     "Tagesmenü 2 -": ":spaghetti: Tagesmenü 2 -",
                     "Tagesmenü vegetarisch -": ":seedling: Tagesmenü vegetarisch -",
                     "mensaVital": ":apple: mensaVital",
                     "Cafeteria": ":coffee: Cafeteria",
                     "Angebot des Tages": ":dollar: Angebot des Tages"}

        if subcommand:
            subcommands = subcommand.split(" ")
            subcommands = [s.lower() for s in subcommands]
            if "nw" in subcommands or "nextweek" in subcommands:
                cal_week = int(cal_week) + 1
                today = next_weekday(today, 0)
                weekday = 0
                week_start = today
                week_end = week_start + datetime.timedelta(days=4)
            elif "heute" in subcommands:
                heute_flag = True
            if "sh" in subcommands or "shedhalle" in subcommands:
                # Mensa shedhalle
                mensa_id = "611"
            elif "nt" in subcommands or "nuertingen" in subcommands:
                # Nuertingen
                mensa_id = "665"
            if "help" in subcommands or "h" in subcommands:
                return await ctx.send(
        """```Mensa:
    help                Diese Nachricht
    <leer>|sh|nt        Speiseplan der aktuellen Woche Morgenstelle | Shedhalle | Nürtingen
        ╠═ heute         Heutiger Speiseplan
        ╚═ nextweek      Speiseplan der nächsten Woche

    z.B. !mensa oder !mensa nextweek oder !mensa sh heute
    Alternativ auch Abkürzungen wie "h" oder "nw"```""")

        data = get_data(mensa_id)
        if subcommand and "nt" not in subcommand.lower() or not subcommand:
            data_caf = get_data(caf_id)
        else:
            data_caf = None

        # No data from Studierendenwerk
        if not data:
            reply = await ctx.send("Keine Daten vom Studierendenwerk bekommen {}".format(":persevere:"))
            return await reply.add_reaction("😵")

        # Needed later
        wochentage = ["Montag", "Dienstag", "Mittwoch",
                      "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        needed_days = []

        # Show next week on weekends
        if weekday > 4:
            # could also use next_weekday() here
            today = next_weekday(today, 0)
            weekday = 0
            week_start = today
            week_end = week_start + datetime.timedelta(days=4)

        # Get Weekdays from today till friday
        if (heute_flag):
            if weekday > 4:
                today = next_weekday(today, 0)
            needed_days.append(today)
        else:
            for day in range(weekday, 5):
                days_till_end_of_week = 4 - day
                needed_days.append(
                    today + datetime.timedelta(days=days_till_end_of_week))

        needed_days.reverse()
        canteen = data[mensa_id]["canteen"]
        if (heute_flag):
            embed = discord.Embed(
                description="{}, am {}".format(canteen, today.strftime("%d.%m.")), color=color)
        else:
            embed = discord.Embed(
                description="{}, KW {} vom {} bis {}".format(canteen, cal_week, week_start.strftime("%d.%m."),
                                                             week_end.strftime("%d.%m.")), color=color)
        for day in needed_days:
            cur_weekday = day.weekday()
            # Go through all meals (6/day)
            menu_cur_day = build_menu(data[mensa_id]["menus"])
            if data_caf:
                # Collect data for cafeteria
                menu_cur_day_caf = build_menu(
                    data_caf[caf_id]["menus"], caf=True)
                # Flatten list
                menu_cur_day_caf = [
                    item for sublist in menu_cur_day_caf for item in sublist]
                # Append to menu
                menu_cur_day.append(menu_cur_day_caf)
            # Flatten list
            menu_cur_day = [
                item for sublist in menu_cur_day for item in sublist]
            if menu_cur_day == []:
                menu_cur_day = "Keine Daten vorhanden"
                embed.add_field(
                    name="> **{}**".format(wochentage[cur_weekday]), value=menu_cur_day)
            else:
                # Do emoji mapping here
                for k, v in emoji_map.items():
                    menu_cur_day = [w.replace(k, v) for w in menu_cur_day]
                # build embed here
                embed = embed_list_lines(
                    embed, menu_cur_day, "> **{}**".format(wochentage[cur_weekday]), inline=True)
        embed.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg/220px-Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg.png')
        embed.set_footer(text='Bot by Fabi / N1tR0#0914')
        await ctx.send(embed=embed)
