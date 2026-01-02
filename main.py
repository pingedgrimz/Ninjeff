import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1455675638852751486)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands {e}')

    # Events
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('Hello'):
            await message.channel.send(f'Hi there {message.author}')

        if message.content.startswith('G'):
            await message.channel.send(f'Good Gamers {message.author}')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1455675638852751486)

# /cmds
@client.tree.command(name="about", description="Get the bot information.", guild=GUILD_ID)
async def say(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About Ninjeff",
        description="Ninjeff is a Discord bot that belongs to the Jeff community. It was completely coded by pingedgrimz.",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

# /tournament
class TournamentEntry(discord.ui.View):
    MAX_ENTERIES = 16
    entries = []
    @discord.ui.button(label="Enter Tournament", style=discord.ButtonStyle.green)
    async def enter_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.entries:
            return await interaction.response.send_message("You already entered in the tournament.", ephemeral=True)
        if len(self.entries) >= self.MAX_ENTERIES:
            return await interaction.response.send_message("The roster for the tournament is complete.", ephemeral=True)
        self.entries.append(interaction.user.id)
        await interaction.channel.send(f"{interaction.user.mention} has submitted the initial tournament roster; kindly wait until further instructions are provided.")
        if len(self.entries) >= self.MAX_ENTERIES:
            button.disabled = True
            await interaction.response.send_message("You have been entered!", ephemeral=True)
class TournamentButton(discord.ui.View):
    REQUIRED_ROLE_ID = 1455677149330538627
    @discord.ui.button(label="Confirm Host", style=discord.ButtonStyle.blurple)
    async def announce_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.REQUIRED_ROLE_ID not in [role.id for role in interaction.user.roles]:
            return await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
        role_mention = f"<@&1456460027547091045>"
        embed1 = discord.Embed(color=discord.Color.blue())
        embed1.set_image(url="https://cdn.discordapp.com/attachments/1455998327714742486/1455998635836969053/Jeff_community_tournaments_banner..png?ex=69581565&is=6956c3e5&hm=1eb765f584062420913b14fe8e0c363c9b2d8f6dd4089f88a5eac73ec0abfce6")
        embed2 = discord.Embed(title="Tournament Announcement", description="Currently, no tournaments has been declared.", color=discord.Color.blue())
        embed2.add_field(name="Max players:", value="```16 players```", inline=True)
        embed2.add_field(name="Winning prize", value="```1,000 V-Bucks```", inline=True)
        await interaction.channel.send(role_mention)
        await interaction.channel.send(embeds=[embed1, embed2], view=TournamentEntry())
        await interaction.response.send_message("Tournament has been hosted", ephemeral=True)
@client.tree.command(name="host", description="Launch a tournament.", guild=GUILD_ID)
async def host(interaction: discord.Interaction):
    await interaction.response.send_message("Click the botton below to launch the tournament:", view=TournamentButton(), ephemeral=True)

# /status
@client.tree.command(name="status", description="Get the current status of the bot.", guild=GUILD_ID)
async def say(interaction: discord.Interaction):
    embed=discord.Embed(title="Bot Status")
    embed.add_field(name="🧠 Memory Usage", value="81.80 MB", inline=True)
    embed.add_field(name="⚙️ CPU Usage", value="51.6%", inline=True)
    embed.add_field(name="⏱️ Uptime", value="00:14:03", inline=True)
    embed.add_field(name="🐍 Python Version", value="3.12.7", inline=True)
    embed.add_field(name="📦 discord.py Version", value="2.6.4", inline=True)
    embed.add_field(name="🖥️ OS", value="Windows", inline=True)
    await interaction.response.send_message(embed=embed)

# /links
@client.tree.command(name="links", description="Get useful links for Jeff community.", guild=GUILD_ID)
async def say(interaction: discord.Interaction):
    embed = discord.Embed(title="Useful Links", color=discord.Color.blue())
    embed.set_image(url="https://cdn.discordapp.com/attachments/1454284468515766454/1454744511061295188/OFJ_MERCH_banner_1650x600.png?ex=695233e7&is=6950e267&hm=7ad6a1a1a07703dcb037df1a1500fc35c0df4c57b976365093a8533fa464b59d&")
    embed.add_field(
        name="Merch",
        value="[OFJ Merch](https://ofj.creator-spring.com/?_ga=2.121664520.2032860827.1766889703-571559999.1766889495&_gl=1*1qae5x1*_gcl_au*MTk2MjkyMjIzLjE3NjY4ODk3MDMuNTA1MjkzOTczLjE3NjY5MDQzOTguMTc2NjkwNTY5MQ..*_ga*NTcxNTU5OTk5LjE3NjY4ODk0OTU.*_ga_G3GKJFR6Z9*czE3NjY5MDQyNjQkbzIkZzEkdDE3NjY5MDY3ODkkajQ2JGwwJGgyODg0MTM0MTc)",
        inline=True
    )
    await interaction.response.send_message(embed=embed)