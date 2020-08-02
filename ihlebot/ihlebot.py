import discord
import time

# Used for DNS lookup
import socket
# Used for regexp
import re
# Used for ping
import os
from random import randint
import random
# General stuff for discord
import asyncio
import aiohttp
import urllib.request, json

# For ASCII art
from pyfiglet import Figlet
import pyfiglet

# Discord stuff
import datetime
import requests
from discord.utils import get
from redbot.core import commands

client = discord.Client()


class Ihlebot(commands.Cog):
    """ Command definitions"""

    def user_is_me(ctx):
        return ctx.message.author.id == "240799236113956864"

    @commands.command(pass_context=True)
    async def pizza(self, ctx):
        """Pizza!"""
        pizza_list = [
            'https://media1.giphy.com/media/iThaM3NlpjH0Y/200w.gif',
            'https://media1.giphy.com/media/POmeDOmoTg9CU/200w.gif',
            'https://i.imgur.com/BrXB1VU.gifv',
            'https://media0.giphy.com/media/3o7aDdeZzsZyx4qkqk/200w.gif',
            'https://media0.giphy.com/media/sTUWqCKtxd01W/200w.gif',
            'https://media0.giphy.com/media/YfLdTsfMIfHX2/200w.gif',
            'https://media0.giphy.com/media/AeWntMyxGFXXi/200w.gif',
            'https://media0.giphy.com/media/10kxE34bJPaUO4/giphy.gif',
            'https://media0.giphy.com/media/RRRSdQ6tuUXBu/200w.gif'
        ]

        rng = random.randint(0, len(pizza_list))
        await self.bot.say(pizza_list[rng])

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await self.bot.say('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(
                name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await self.bot.say(embed=data)


    @commands.command(pass_context=True)
    async def ping(self, ctx, ip):
        """Check if Server is online"""

        # Check for valid IP else do DNS lookup
        valid_ip = re.compile("([0-9]{1,3}\.){3}[0-9]{1,3}")
        valid_hostname = re.compile(".*\.[a-zA-Z]{2,}")
        valid = False

        if valid_ip.match(ip):
            valid = True
        elif valid_hostname.match(ip):
            valid = True
            try:
                await self.bot.say('Doing DNS lookup...')
                ip = socket.gethostbyname(ip)
            except socket.gaierror:
                return await self.bot.say('Whoops! That Address cant be resolved!')

        if valid == True:
            start = time.time()
            response = os.system("sudo ping -c 1 -w3 " + ip)
            duration = time.time() - start
            duration = round(duration * 1000, 0)
            if response == 0:
                await self.bot.say(ip + ' is up and responding in ' +
                                   str(duration) + 'ms.')
            else:
                await self.bot.say(ip + ' is not reachable.')
        else:
            await self.bot.say(ip + ' is not a valid IP or Domain.')

    @commands.command(pass_context=True)
    async def pr0(self, ctx):
        """Outputs a random image from pr0gramm.com (sfw)"""

        # Generate random number, check if header responds with 200 (OK)
        # If not generate new number
        # Hardcoded img src from webpage in line 63
        # Extract path to image from webpage
        # Clean up
        user = ctx.message.author
        color = self.getColor(user)

        with urllib.request.urlopen(
                "https://pr0gramm.com/api/items/get") as url:
            data = json.loads(url.read().decode())

        items = data["items"]
        item = random.choice(items)["image"]
        upvotes = random.choice(items)["up"]
        downvotes = random.choice(items)["down"]
        uploader = random.choice(items)["user"]
        embed = discord.Embed(
            description='Uploaded by **{}**'.format(uploader), color=color)
        embed.add_field(
            name="Score",
            value="{0} :arrow_up: {1} :arrow_down:".format(upvotes, downvotes))

        await self.bot.say(embed=embed)
        await self.bot.say("https://img.pr0gramm.com/{}".format(item))

    @commands.command(pass_context=True, aliases=["cf"])
    async def coinflip(self, ctx, *, param=None):
        """Coinflip, defaults to Kopf/Zahl if no choices are given"""

        if param is None:
            rng = randint(1, 10)
            if rng <= 5:
                return await self.bot.say("Kopf gewinnt!")
            else:
                return await self.bot.say("Zahl gewinnt!")
        else:
            choices = []
            for word in param.split(' '):
                choices.append(word)
            length = len(choices)
            rng = randint(0,length-1)
            return await self.bot.say("**{}** hat gewonnen!".format(choices[rng]))

    def getColor(self, user):
        try:
            color = user.colour
        except:
            color = discord.Embed.Empty
        return color

    @commands.command(pass_context=True)
    async def ascii(self, ctx, *, param):
        """Print String to ascii art: <font> <text>"""
        f = Figlet()
        fonts = f.getFonts()
        attr = param.split(' ', 1)[0]
        if attr.lower() == "help":
            def chunks(s, n):
                """Produce `n`-character chunks from `s`."""
                for start in range(0, len(s), n):
                    yield s[start:start + n]
            fonts_string = ""
            fonts_chunks = []
            for font in fonts:
                fonts_string += "{},".format(font)
            for chunk in chunks(fonts_string, 900):
                fonts_chunks.append(chunk)
            embed = discord.Embed(
                description="Usage: !ascii <fontname> <text>\nFont defaults to slant.\nAvailable fonts:")
            for chunk in fonts_chunks:
                embed.add_field(name="-", value="``{}``".format(chunk))
            return await self.bot.say(embed=embed)
        else:
            if attr.lower() in fonts:
                f = Figlet(font=attr.lower())
                try:
                    text = param.split(' ', 1)[1]
                except IndexError:
                    text = 'Empty'
            else:
                f = Figlet(font='slant')
                text = param
            asciistring = f.renderText(text)
            try:
                return await self.bot.say("```{}```".format(asciistring))
            except discord.errors.HTTPException:
                return await self.bot.say("Message too long")

    @commands.command(pass_context=True)
    @commands.check(user_is_me)
    async def emojiurl(self, ctx):
        server = ctx.message.server
        emojis = []
        for ej in server.emojis:
            emojis.append(ej)
            await self.bot.say(ej.url)

    @commands.command(pass_context=True)
    async def w(self, ctx, s1, s2=None, s3=None, s4=None):
        """
        Erzähle zwei Wahrheiten und eine Lüge! Die anderen müssen raten, welche Aussage gelogen ist.
        Beispiel: !w "Ich war noch niemals in New York" "Ich mag Gurken" "Ich studiere Informatik"

        :param s1: A truth
        :param s2: Another truth, maybe a lie
        :param s3: Another truth
        :return:
        """
        if s4 or not s3 or not s2:
            return await self.bot.say("Denke dran nur 3 Antworten zu geben und diese mit \"\" abzutrennen.")
        reply = await self.bot.say(":one: {}\n:two: {}\n:three: {}".format(s1, s2, s3))
        emojis = ['1\N{combining enclosing keycap}', '2\N{combining enclosing keycap}', '3\N{combining enclosing keycap}']
        for emoji in emojis:
            await self.bot.add_reaction(reply, emoji)

    @commands.command(pass_context=True, aliases=["Mensa"])
    async def mensa(self, ctx, subcommand=None):

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
                embed.add_field(name=field_name, value=values[0], inline=inline)
                for v in values[1:]:
                    embed.add_field(name=zero_width_space, value=v, inline=inline)
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
            url_mensa = "https://www.my-stuwe.de/wp-json/mealplans/v1/canteens/{}?lang=de".format(id)
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
                        menu_cur_day.append(["*{} - {}€*".format(menuLine, price)])
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
        mensa_id = "621" # Tuebingen Morgenstelle
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
            if subcommand.lower() == "nextweek" or subcommand.lower() == "nw":
                cal_week = int(cal_week) + 1

                today = next_weekday(today, 0)
                weekday = 0
                week_start = today
                week_end = week_start + datetime.timedelta(days=4)
            elif subcommand.lower() == "heute":
                heute_flag = True
            elif subcommand.lower() == "nt":
                mensa_id = "665"  # Nuertingen
            elif subcommand.lower() == "ntheute": # This is ugly
                mensa_id = "665"  # Nuertingen
                heute_flag = True
            else:
                return await self.bot.say("""```
        Mensa:
            help         Diese Nachricht
            <leer>       Speiseplan der aktuellen Woche
            nextweek     Speiseplan der nächsten Woche
            heute        Speiseplan von heute
            nt           Speiseplan in Nürtingen

            z.B. !mensa oder !mensa nextweek
            Alternativ auch Abkürzungen wie "h" oder "nw"
        ```""")

        data = get_data(mensa_id)
        if subcommand and "nt" not in subcommand.lower() or not subcommand:
            data_caf = get_data(caf_id)
        else:
            data_caf = None

        # No data from studierenwerk
        if not data:
            emoji_woah = get(self.bot.get_all_emojis(), name="woah")
            emoji_bad = get(self.bot.get_all_emojis(), name="eelsbadman")
            reply = await self.bot.say("Keine Daten vom Studierenwerk bekommen {}".format(emoji_bad))
            return await self.bot.add_reaction(reply, emoji_woah)

        # Needed later
        wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
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
                needed_days.append(today + datetime.timedelta(days=days_till_end_of_week))

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
                menu_cur_day_caf = build_menu(data_caf[caf_id]["menus"], caf=True)
                # Flatten list
                menu_cur_day_caf = [item for sublist in menu_cur_day_caf for item in sublist]
                # Append to menu
                menu_cur_day.append(menu_cur_day_caf)
            # Flatten list
            menu_cur_day = [item for sublist in menu_cur_day for item in sublist]
            if menu_cur_day == []:
                menu_cur_day = "Keine Daten vorhanden"
                embed.add_field(name="> **{}**".format(wochentage[cur_weekday]), value=menu_cur_day)
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
        await self.bot.say(embed=embed)



    # @commands.command(pass_context=True)
    # @commands.has_role("Administrator")
    # async def allrole(self, ctx, group=None):
    #     server = ctx.message.server
    #     role = discord.utils.get(server.roles, name=group.lower())
    #     members = server.members
    #     for member in members:
    #         try:
    #             await self.bot.add_roles(member, role)
    #         except AttributeError:
    #             await self.bot.say("Fehler")

# @commands.command(pass_context=True)
    # @commands.has_role("Administrator")
    # async def createroles(self, ctx):
    #     """Create roles to each channel that begins with "übungsgruppe- and set permissions"""
    #     server = ctx.message.server
    #     author = ctx.message.author
    #     all_channels = server.channels
    #     all_roles = []
    #     group_channels = []
    #     # Collect already available roles
    #     for role in server.roles:
    #         all_roles.append(role.name)
    #     # Collect needed channel names
    #     for channel in all_channels:
    #         if "übungsgruppe-" in channel.name:
    #             if channel.name not in group_channels:
    #                 group_channels.append(channel.name)
    #
    #     # Needed permissions
    #     everyone_perms = discord.PermissionOverwrite(read_messages=False)
    #     overwrite = discord.PermissionOverwrite()
    #     overwrite.read_messages = True
    #     overwrite.send_message = True
    #     overwrite.manage_messages = True
    #     overwrite.embed_links = True
    #     overwrite.attach_files = True
    #     overwrite.read_message_history = True
    #     # Create a role for each channel
    #     for group_channel in group_channels:
    #         if group_channel not in all_roles:
    #             await self.bot.create_role(author.server, name=group_channel)
    #             await self.bot.say("Role {} created".format(group_channel))
    #
    #     role_bots = discord.utils.get(server.roles, name="Bots")
    #
    #     # Grant permissions to role
    #     for channel in all_channels:
    #         if "übungsgruppe-" in channel.name:
    #             role = discord.utils.get(server.roles, name=channel.name)
    #             # Deny permission to everyone
    #             await self.bot.edit_channel_permissions(channel, server.default_role, everyone_perms)
    #             # Grant permission to role
    #             await self.bot.edit_channel_permissions(channel, role, overwrite)
    #             await self.bot.edit_channel_permissions(channel, role_bots, overwrite)
    #             await self.bot.say("Granted permissions for role {} to channel {}".format(role, channel))
    #             await asyncio.sleep(1.5)

    # @commands.command(pass_context=True)
    # async def gruppe(self, ctx, join_group=None):
    #
    #     server = ctx.message.server
    #
    #
    #     async def send_help(destination):
    #         group_channels = []
    #         all_channels = server.channels
    #         for channel in all_channels:
    #             if "übungsgruppe-" in channel.name:
    #                 if channel.name not in group_channels:
    #                     group_channels.append(channel.name.replace("übungsgruppe-", ""))
    #         sorted_groups = sorted(group_channels)
    #         embed = discord.Embed(
    #             description="**Verfügbare Übungsgruppen**")
    #         embed.add_field(name="Gruppen", value="\n".join(sorted_groups))
    #
    #         await self.bot.send_message(destination, "Gruppe nicht gefunden oder angegeben. Verfügbare Gruppen sind:")
    #         embed.set_footer(text='Bot by Fabi')
    #         return await self.bot.send_message(destination, embed=embed)
    #
    #     # Harcoded channel ID :(
    #     if ctx.message.channel.id != "437291813276090408":
    #         await send_help(ctx.message.author)
    #         await self.bot.send_message(ctx.message.author, "Bitte nutze den Channel #gruppenzuweisung dazu!")
    #     else:
    #         if join_group is None:
    #             return await send_help(ctx.message.channel)
    #         join_group = join_group.lower()
    #         join_group = "übungsgruppe-{}".format(join_group)
    #         author = ctx.message.author
    #         if "übungsgruppe-" in join_group:
    #             if join_group in [y.name.lower() for y in author.roles]:
    #                 await self.bot.say("{}, du bist bereits in der Gruppe {}".format(author.mention, join_group))
    #             else:
    #                 try:
    #                     role = discord.utils.get(server.roles, name=join_group)
    #                     await self.bot.add_roles(author, role)
    #                     await self.bot.say("{}, du wurdest zu {} hinzugefügt".format(author.mention, join_group))
    #                 except AttributeError:
    #                     await send_help(ctx.message.channel)
    #         else:
    #             await send_help(ctx.message.channel)

    # @commands.command(pass_context=True)
    # async def gruppeverlassen(self, ctx, leave_group=None):
    #     server = ctx.message.server
    #     author = ctx.message.author
    #     all_roles = author.roles
    #     role_names = []
    #     for role_name in all_roles:
    #         if not "everyone" in role_name.name:
    #             role_names.append(role_name.name.replace("übungsgruppe-", ""))
    #
    #     async def send_help(destination):
    #         embed = discord.Embed(description="**Zugeordnete Übungsgruppen**")
    #         embed.add_field(name="Gruppen", value="\n".join(role_names))
    #         await self.bot.send_message(destination, "Gruppe nicht gefunden oder zugeordnet. Zugeordnete Gruppen sind:")
    #         embed.set_footer(text='Bot by Fabi')
    #         return await self.bot.send_message(destination, embed=embed)
    #
    #     # Harcoded channel ID :(
    #     if ctx.message.channel.id != "437291813276090408":
    #         await send_help(ctx.message.author)
    #         await self.bot.send_message(ctx.message.author, "Bitte nutze den Channel #gruppenzuweisung dazu!")
    #     else:
    #         if leave_group is None:
    #             return await send_help(ctx.message.channel)
    #         leave_group = leave_group.lower()
    #         leave_group_full = "übungsgruppe-{}".format(leave_group)
    #         try:
    #             role = discord.utils.get(server.roles, name=leave_group_full)
    #             if leave_group not in role_names:
    #                 await self.bot.say("{} du bist nicht in der Gruppe {}".format(author.mention, leave_group_full))
    #             else:
    #                 await self.bot.remove_roles(author, role)
    #                 await self.bot.say("{} du wurdest aus der Gruppe {} entfernt".format(author.mention, leave_group_full))
    #         except AttributeError:
    #             await send_help(ctx.message.channel)
    #
    # @commands.command(pass_context=True)
    # async def gruppeninfo(self, ctx, group=None):
    #     server = ctx.message.server
    #     color = self.getColor(ctx.message.author)
    #     channel = ctx.message.channel
    #     group_info = None
    #
    #     # redundant part, fix this
    #     async def send_help():
    #         group_channels = []
    #         all_channels = server.channels
    #         for channel in all_channels:
    #             if "übungsgruppe-" in channel.name:
    #                 if channel.name not in group_channels:
    #                     group_channels.append(channel.name.replace("übungsgruppe-", ""))
    #         sorted_groups = sorted(group_channels)
    #         embed = discord.Embed(
    #             description="**Verfügbare Übungsgruppen**")
    #         embed.add_field(name="Gruppen", value="\n".join(sorted_groups))
    #
    #         return await self.bot.say(embed=embed)
    #
    #     if group is not None:
    #         group_info = "übungsgruppe-{}".format(group)
    #
    #     if "übungsgruppe-" in channel.name and group is None:
    #         group_info = channel.name
    #     elif group is None:
    #         return await send_help()
    #     group_info = group_info.lower()
    #     role = discord.utils.get(server.roles, name=group_info)
    #
    #     member_list = []
    #     members = server.members
    #     for member in members:
    #         # Check if member has role
    #         roles_member = member.roles
    #         if role in roles_member:
    #             if member.nick:
    #                 member_list.append(member.nick)
    #             else:
    #                 member_list.append(member.name)
    #     embed = discord.Embed(description="**Zugeordnete Mitglieder**", color=color)
    #     if member_list:
    #         embed.add_field(name=group_info, value="\n".join(member_list))
    #     else:
    #         embed.add_field(name=group_info, value="Niemand")
    #     return await self.bot.say(embed=embed)

def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
