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
        await ctx.send(pizza_list[rng])

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await ctx.send('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(
                name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await ctx.send(embed=data)


    @commands.command(pass_context=True)
    async def pinghost(self, ctx, ip):
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
                await ctx.send('Doing DNS lookup...')
                ip = socket.gethostbyname(ip)
            except socket.gaierror:
                return await ctx.send('Whoops! That Address cant be resolved!')

        if valid == True:
            start = time.time()
            response = os.system("sudo ping -c 1 -w3 " + ip)
            duration = time.time() - start
            duration = round(duration * 1000, 0)
            if response == 0:
                await ctx.send(ip + ' is up and responding in ' +
                                   str(duration) + 'ms.')
            else:
                await ctx.send(ip + ' is not reachable.')
        else:
            await ctx.send(ip + ' is not a valid IP or Domain.')

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

        await ctx.send(embed=embed)
        await ctx.send("https://img.pr0gramm.com/{}".format(item))

    @commands.command(pass_context=True, aliases=["cf"])
    async def coinflip(self, ctx, *, param=None):
        """Coinflip, defaults to Kopf/Zahl if no choices are given"""

        if param is None:
            rng = randint(1, 10)
            if rng <= 5:
                return await ctx.send("Kopf gewinnt!")
            else:
                return await ctx.send("Zahl gewinnt!")
        else:
            choices = []
            for word in param.split(' '):
                choices.append(word)
            length = len(choices)
            rng = randint(0,length-1)
            return await ctx.send("**{}** hat gewonnen!".format(choices[rng]))

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
            return await ctx.send(embed=embed)
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
                return await ctx.send("```{}```".format(asciistring))
            except discord.errors.HTTPException:
                return await ctx.send("Message too long")

    @commands.command(pass_context=True)
    @commands.check(user_is_me)
    async def emojiurl(self, ctx):
        server = ctx.message.server
        emojis = []
        for ej in server.emojis:
            emojis.append(ej)
            await ctx.send(ej.url)

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
            return await ctx.send("Denke dran nur 3 Antworten zu geben und diese mit \"\" abzutrennen.")
        reply = await ctx.send(":one: {}\n:two: {}\n:three: {}".format(s1, s2, s3))
        emojis = ['1\N{combining enclosing keycap}', '2\N{combining enclosing keycap}', '3\N{combining enclosing keycap}']
        for emoji in emojis:
            await ctx.send(reply, emoji)

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

    @commands.check(user_is_me)
    @commands.command(pass_context=True)
    async def send(self, ctx, channelId, message):
        """Sends a message to the specified channel identified by its ID"""
        channel = client.get_channel(channelId)
        if channel:
            try:
                await channel.send(message)
            except:
                await ctx.send("Cannot send a message to this channel!")
        else:
            await ctx.send("Channel not found")

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
