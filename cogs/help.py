import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["info", "Info"])
    async def Help(self, ctx):
        embed = discord.Embed(
            title="AltF4 Airlines",
            url="https://google.com",
            description="Commands To Use",
            color=0xFF0000,
        )
        embed.set_author(
            name=ctx.author.display_name,
            url="https://google.com",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_thumbnail(
            url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/"
        )
        # embed.add_field(name="!clockin", value="Clocks You In", inline=False)
        # embed.add_field(name="!clockout", value="Clocks You Out", inline=False)
        embed.add_field(
            name="!stats",
            value="Shows Your Overall stats and how much you owe the company",
            inline=True,
        )
        embed.add_field(name="!AltF4", value="Shows The Chain Of Command", inline=False)
        embed.add_field(
            name="!Sheets", value="Sheets To Our Guidelines etc.", inline=False
        )
        embed.add_field(
            name="!flight vip #",
            value="This is how you will log your flights the # is # of passengers",
            inline=False,
        )
        embed.add_field(
            name="!flight sked #",
            value="Same as above but for Schedule Flights",
            inline=False,
        )
        embed.add_field(
            name="!flight bloon #",
            value="Same as above but for Balloon Flights",
            inline=False,
        )
        embed.add_field(
            name="!flight sky #", value="Same as above but for Sky Diving", inline=False
        )
        embed.add_field(
            name="!flight scuba #",
            value="Same as above but for Scuba Diving",
            inline=False,
        )
        embed.add_field(
            name="!flight pudo #",
            value="Same as above but for Pickup/Dropoff",
            inline=False,
        )
        embed.set_footer(text="Aeron Flight Bot v1.0")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
