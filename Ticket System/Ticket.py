#   Ticket System von MK_Pascal#0505
#   Hier ist ein kleines Ticket System Was ein guten einstieg für euch bietet.
#
#
#
import os
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import random
import os
import asyncio
from datetime import datetime
from ezcord import times
import aiosqlite

# Hier Brauchst du einen Order mit den namen "Data" damit die Datenbank weiß wo sie erstellt werden muss.
db = "Data/Ticket.db"

set_image = "https://cdn.discordapp.com/attachments/1085176967730581681/1087780407837204570/MK_greenTurquoise.gif"
set_thumbnail = ""
Mod_role = 1234567  # änder hier dir ID für die moderator rolle
Log_Channel = 1234567
category_id = 1234567


class Ticket(commands.Cog):
    ticket = SlashCommandGroup("ticket", description="Ticket system")

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def add_views(self) -> None:
        self.bot.add_view(TutorialView(self.bot))
        self.bot.add_view(main(self.bot))

    @commands.Cog.listener("on_ready")
    async def create_table(self) -> None:
        async with aiosqlite.connect(db) as conn:
            await conn.execute(
                '''
                    CREATE TABLE IF NOT EXISTS ticket (
                        guild_id INTEGER PRIMARY KEY,
                        ticket_count INTEGER DEFAULT 0
                    )
                '''
            )
            await conn.commit()

        if not os.path.exists("Log"):
            os.mkdir("Log")

    # Hier kannst du dein guild eintragen ohne den send command zu Benutzen.
    @ticket.command(name="guild", description="Füge dein server wieder hinzu")
    @discord.default_permissions(administrator=True)
    async def _guild(self, ctx: discord.ApplicationContext) -> None:
        async with aiosqlite.connect(db) as conn:
            await conn.execute('INSERT OR REPLACE INTO ticket(guild_id) VALUES(?)', (ctx.guild.id,))
            await conn.commit()

        await ctx.respond("Guild wurde eingetragen", ephemeral=True)

    @ticket.command(name="send", description="Ticket System")
    @discord.default_permissions(administrator=True)
    async def _send(self, ctx: discord.ApplicationContext) -> None:
        async with aiosqlite.connect(db) as conn:
            await conn.execute('INSERT OR REPLACE INTO ticket(guild_id) VALUES(?)', (ctx.guild.id,))
            await conn.commit()

        ticket_create = discord.Embed(
            title="Support kontaktieren",
            description="Drücke den Button, um ein neues Ticket zu erstellen.\n"
                        "\n"
                        "⚠️**Wichtig** Bitte erstelle nur ein Ticket wenn du ein ernstes problem hast[!](https://my-cool-app.com)",
            color=0x3BA45C
        )
        ticket_create.set_thumbnail(url=set_thumbnail)
        ticket_create.set_image(url=set_image)
        ticket_create.set_footer(text="Made by MK_Pascal#0505")

        erfolgreich = discord.Embed(
            title="Ticket System erfolgreich aufgesetzt!",
            color=0x2ECC70
        )
        erfolgreich.set_image(url=set_image)
        erfolgreich.set_footer(text="Made by MK_Pascal#0505")

        await ctx.respond(embed=erfolgreich, ephemeral=True)
        await ctx.channel.send(embed=ticket_create, view=TutorialView(self.bot))


def setup(bot: discord.Bot) -> None:
    bot.add_cog(Ticket(bot))


class Logger:
    def __init__(self, channel: discord.TextChannel) -> None:
        self.channel = channel

    async def create_log_file(self) -> None:
        with open(f"Log/{self.channel.name}.txt", "w", encoding="utf-8") as f:
            f.write(f'Ticket "{self.channel.name}"\n\n')
            f.write(f"{'-' * 40}\n")
            messages = await self.channel.history(limit=69420).flatten()
            for i in reversed(messages):

                f.write(
                    f"[{i.created_at}] {i.author} ({i.author.id}): {i.content}\n")
            f.write(f"{'-' * 40}\n\n")
            if len(messages) >= 69420:
                f.write(
                    f"Es wurden mehr als 69420 Nachrichten in diesen Channel eingesendet. Aus Speicher-Gründen wurden "
                    f"nur die letzten 69420 Nachrichten geloggt.")
            else:
                f.write(f"Es wurden Nachrichten: {len(messages)} geschrieben")

    async def send_log_file(self, channel: discord.TextChannel) -> None:
        await channel.send(files=[discord.File(f"Log/{self.channel.name}.txt", filename=f"{self.channel.name}.txt")])
        os.remove(f"Log/{self.channel.name}.txt")


class TutorialView(discord.ui.View):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        super().__init__(timeout=None)

        # hier kannst du einstellen wie lange es Dauern soll bis Man ein neues Ticket erstellen kann.
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, 120, commands.BucketType.user)

    @discord.ui.button(label="Ticket erstellen", style=discord.ButtonStyle.green, emoji="📩", custom_id="ticket", row=1)
    async def button_callback1(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()

        async with aiosqlite.connect(db) as conn:
            async with conn.execute('SELECT guild_id FROM ticket WHERE guild_id = ?', (interaction.guild.id,)) as cursor:
                wert = await cursor.fetchone()

        if wert is None:
            if interaction.guild.owner == interaction.user:
                embed = discord.Embed(
                    description="Ticket's können nicht erstellt werden🤔\nFühre bitte erneut den Ticket Command aus",
                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    description="Ich weiß nicht wo ich dein Ticket erstellen soll🤔\nFrag bitte den Server owner ob er es aktiviert",
                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:

            if retry:

                zeit = times.dc_timestamp(int(retry), style='R')
                liste = [f"Immer sachte mit den jungen Pferden! **{zeit}** kannst du es nochmal versuchen.",
                         f"Oh! probier es **{zeit}** nochmal.",
                         f"Immer eins nach den anderen. **{zeit}** kannst du erneut versuchen."]
                word = random.choice(liste)
                timeup = discord.Embed(
                    title="Cooldown", description=f"{word}", color=discord.Color.red())

                return await interaction.response.send_message(embed=timeup, ephemeral=True)
            else:
                cat = self.bot.get_channel(category_id)
                interaction.message.author = interaction.user

                async with aiosqlite.connect(db) as conn:
                    async with conn.execute('SELECT channel_count FROM ticket WHERE guild_id = ?', (interaction.guild.id,)) as cursor:
                        channel_count = await cursor.fetchone()[0]

                overwrites = {
                    # Mit der get_role funktion kannst du in der oben eingetragenen rolle festlegen wer das Ticket sehen darf.
                    # in den py-cord docs kannst du auch nochmal nach schauen was es für Permissions gibt.
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.guild.get_role(Mod_role): discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True)
                }

                ticket_channel = await interaction.guild.create_text_channel(
                    f'🎫・ticket-{channel_count}',
                    topic=f'Ticket von {interaction.user.name}'
                    f'\n\ninfo'
                    f'\nTicket-nummer: {channel_count}'
                    f'\nkunden-ID: {interaction.user.id}'
                    f'\nMade by MK_Pascal#0505',
                    category=cat,
                    overwrites=overwrites
                )

                ticket_create = discord.Embed(
                    title="Ticket Erstellt!",
                    description=f"{interaction.user.mention}, Hier findest du dein ticket:\n{ticket_channel.mention}",
                    color=0x3BA45C
                )
                ticket_create.set_footer(text="Made by MK_Pascal#0505")

                await interaction.response.send_message(embed=ticket_create, ephemeral=True)

                ticket_channel_em = discord.Embed(
                    title=f"Willkommen zu deinen Ticket {interaction.user.name}",
                    description="**Um zu beginnen, bitte befolge diese Schritte**"
                                "\nNenne uns dein Anliegen und habe ein bisschen Geduld."
                                f"\nIn der Zwischenzeit kannst du auch die Regeln durchlesen."
                                f"\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
                                f"\nUnsere <@&{Mod_role}> werden sich so schnell wie möglich um dein anliegen drum kümmern.",
                    color=0x3BA45C
                )
                ticket_channel_em.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/1077917507568013332/1078263684012458055/ticket.gif")
                ticket_channel_em.set_image(url=set_image)
                ticket_channel_em.set_footer(text="Made by MK_Pascal#0505")
                await ticket_channel.send(embed=ticket_channel_em, view=main(self.bot))

                async with aiosqlite.connect(db) as conn:
                    await conn.execute('UPDATE ticket SET channel_count = ? WHERE guild_id = ?', (channel_count + 1, interaction.guild.id))
                    await conn.commit()


class main(discord.ui.View):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="schließen", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close", row=1)
    async def button_callback2(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        for child in self.children:
            child.disabled = True

        modrole = interaction.guild.get_role(Mod_role)

        if modrole in interaction.user.roles:
            close = discord.Embed(
                title="Ticket wurde geschlossen",
                description=f"{interaction.user.mention} hat dein Ticket geschlossen. Dieser Channel wird num in wenigen Sekunden gelöscht",
                color=0xBF3537
            )
            close.set_footer(text="Made by MK_Pascal#0505")
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(embed=close)

            # Hier änderst du die channel wo dann die Logs gesendet werden
            logchannel = interaction.guild.get_channel(Log_Channel)
            logger = Logger(interaction.channel)
            await logger.create_log_file()

            embed2 = discord.Embed(
                title=f"Chat erfolgreich exportiert",
                description=f"Closed by {interaction.user.mention} 🔒\n```{interaction.channel.name}```",
                color=0x23a696,
                timestamp=datetime.now()
            )
            embed2.set_footer(text="Made by MK_Pascal#0505")
            embed2.set_image(url=set_image)

            await logchannel.send(embed=embed2)
            await logger.send_log_file(logchannel)
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            liste = [f"Nur {modrole.mention} können dieses Ticket schließen",
                     f"Da hast du wohl eine sonder Funktion von den {modrole.mention} entdeckt",
                     f"Wenn die Zeit dazu gekommen ist, werden die {modrole.mention} sich schon drum kümmern"]
            wort = random.choice(liste)
            teamrolle = discord.Embed(
                description=f"{wort}",
                color=discord.Color.red()
            )
            teamrolle.set_footer(text="Made by MK_Pascal#0505")

            await interaction.response.send_message(embed=teamrolle, ephemeral=True)

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green, emoji="✅", custom_id="Bearbeiten", row=1)
    async def button_callback3(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        button.disabled = True
        modrole = interaction.guild.get_role(Mod_role)

        if modrole in interaction.user.roles:

            Bearbeiten = discord.Embed(
                title="Ticket angenommen",
                description=f"{interaction.user.mention} kümmert sich um dein Ticket",
                color=0x3BA45C
            )
            Bearbeiten.set_footer(text="Made by MK_Pascal#0505")

            await interaction.response.edit_message(view=self)
            await interaction.followup.send(embed=Bearbeiten)
        else:
            liste = [f"Nur {modrole.mention} können dieses Ticket schlissen",
                     f"Da hast du wohl eine sonder funktion von den {modrole.mention} entdeckt"]
            wort = random.choice(liste)
            teamrolle = discord.Embed(
                description=f"{wort}",
                color=discord.Color.red()
            )
            teamrolle.set_footer(text="Made by MK_Pascal#0505")

            await interaction.response.send_message(embed=teamrolle, ephemeral=True)

    @discord.ui.button(label="Regel", style=discord.ButtonStyle.blurple, emoji="🔖", custom_id="Regel", row=1)
    async def button_callback4(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        infos = discord.Embed(
            title="Ticket Regel!",
            description=f"\n1・Alle Nachrichten in diesem Ticket werden aufgezeichnet und können für spätere Zwecke wieder abgerufen werden."
                        f"\n2・Nur das Server-Team darf diese Chats einsehen"
                        f"\n3・Das Team darf keinerlei Details weitergeben. Sollte es doch geschehen, kann dies mit einem Serverausschluss bestraft werden.",
            color=0x5865F2
        )
        infos.set_footer(text="Made by MK_Pascal#0505")

        await interaction.response.send_message(embed=infos, ephemeral=True)
