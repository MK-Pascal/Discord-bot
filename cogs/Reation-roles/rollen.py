import discord
from discord.ext import commands
from discord.commands import slash_command

role1 = 1234567
role2 = 1234567
role3 = 1234567

class Rollen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TutorialView(self.bot))

    @slash_command(description="Ping Benachrichtigungen")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        erfolgreich = discord.Embed(
            title="🫑 Benachrichtigungen erfolgreich gesendet",
            color=0x2ECC70
        )
        pings = discord.Embed(
            title="📢 Benachrichtigungen",
            description="**Wenn du bei News Benachrichtig werden willst**"
                        "\n**Suche dir eine Rolle aus**"
                        "\n"
                        "\n📢 Ping bei Server änderung"
                        "\n🔔 Ping bei neuen Videos"
                        "\n🍪 Ping bei Neuen Timo news",
            color=0x3BA45C
        )
        await ctx.respond(embed=erfolgreich, ephemeral=True)
        await ctx.channel.send(embed=pings, view=TutorialView(self.bot))

def setup(bot):
    bot.add_cog(Rollen(bot))

class TutorialView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
    @discord.ui.button(
        label="Ankündingung",
        style=discord.ButtonStyle.green,
        emoji="📢", custom_id="loudspeaker",
        row=1
    )
    async def button_callback1(self, button, interaction):
        user = interaction.user
        role = interaction.guild.get_role(role1)

        rolegetaway = discord.Embed(
            description=f"**Deine {role.mention} Rolle wurde entfernt!**",
            color=0x2ECC70
        )
        getrole = discord.Embed(
            description=f"**Du hast nun die {role.mention} Rolle!**",
            color=0x2ECC70
        )
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(embed=rolegetaway, ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(embed=getrole, ephemeral=True)

    @discord.ui.button(
        label="Videos",
        style=discord.ButtonStyle.green,
        emoji="🔔", custom_id="bell",
        row=1
    )
    async def button_callback2(self, button, interaction):
        user = interaction.user
        role = interaction.guild.get_role(role2)

        rolegetaway = discord.Embed(
            description=f"**Deine {role.mention} Rolle wurde entfernt!**",
            color=0x2ECC70
        )
        getrole = discord.Embed(
            description=f"**Du hast nun die {role.mention} Rolle!**",
            color=0x2ECC70
        )
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(embed=rolegetaway, ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(embed=getrole, ephemeral=True)

    @discord.ui.button(
        label="Keks",
        style=discord.ButtonStyle.green,
        emoji="🍪", custom_id="Keks",
        row=1
    )
    async def button_callback3(self, button, interaction):
        user = interaction.user
        role = interaction.guild.get_role(role3)

        rolegetaway = discord.Embed(
            description=f"**Deine {role.mention} Rolle wurde entfernt!**",
            color=0x2ECC70
        )
        getrole = discord.Embed(
            description=f"**Du hast nun die {role.mention} Rolle!**",
            color=0x2ECC70
        )
        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(embed=rolegetaway, ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.response.send_message(embed=getrole, ephemeral=True)
