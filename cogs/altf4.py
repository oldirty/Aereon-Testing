import discord
from discord.ext import commands

class Altf4(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['altf4','f4'])
  async def AltF4(self, ctx):
     embed = discord.Embed(title="AltF4 Airlines", url="https://google.com", description= "Corporate Ranks", color=0xff0000)
     embed.set_author(name=ctx.author.display_name, url="https://google.com", icon_url=ctx.author.avatar_url)
     embed.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
     embed.add_field(name="Owner", value="Victor Vonsweetz", inline=True)
     embed.add_field(name="Board of Directors", value="Elias Sicario\n Ava Arienti", inline=False)
     embed.add_field(name="Chief Executive Officer", value="Jordy Jetson", inline=False)
     embed.add_field(name="Chief Financial Officer", value="Window Payne", inline=False)
     embed.add_field(name="Chief Administrative Officer", value="N/A", inline=False)
     embed.add_field(name="Chief Human Resource Officer", value="N/A", inline=False)
     embed.set_footer(text="Aeron Flight Bot v1.0")
     await ctx.send(embed=embed)

def setup(client):
      client.add_cog(Altf4(client))