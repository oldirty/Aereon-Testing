import discord
from discord.ext import commands

class Sheets(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['guides'])
  async def Sheets(self, ctx):
     embed = discord.Embed(title="AltF4 Airlines", url="https://google.com", description= "Official Guides of AltF4 Airlines", color=0xff0000)
     embed.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
     embed.add_field(name="Management Guidelines", value="https://docs.google.com/document/d/1P4dc_BIS7l80hnjvP_is5b3JWweIa7anCwRDOYcM5rs/edit?usp=sharing", inline=True)
     embed.add_field(name="Pilot Guidelines", value="https://docs.google.com/document/d/1XtwHNapJO7wc11GYHtaA__7-l8Gxverv-8_QE56DPVs/edit?usp=sharing", inline=False)
     embed.add_field(name="Flight Instructor S.O.P.", value="https://docs.google.com/document/d/186tJ5sNobWcC3r9VN8WwMQB_UAtd3mk3WQ3W57JqEEg/edit?usp=sharing", inline=False)
     embed.add_field(name="ACAP Directory", value="https://docs.google.com/spreadsheets/d/1R4h9B3Npeq2T5QBQnaoCtKH8WLKoR-0YPYZv8S2dgN4/edit?usp=sharing", inline=False)
     embed.set_footer(text="Aeron Flight Bot v1.0")
     await ctx.send(embed=embed)

def setup(client):
      client.add_cog(Sheets(client))