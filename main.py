# module Imports
import discord
import os, requests, json
import math, time, datetime
from discord.ext.commands import MissingPermissions
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("Aeron Flight Bot v1.0")


if __name__ == "__main__":
    client.add_cog(Altf4(client))

    @client.event
    async def on_member_join(member):
        channel = client.get_channel(865731272919744535)
        await channel.send(
            "Welcome to AltF4 Airlines discord! When ready head down to ACAP for a interview! Good luck!"
        )

    @client.event
    async def on_member_remove(member):
        channel = client.get_channel(865731272919744535)
        await channel.send("Hah, later nerd!")

    keep_alive()
    client.run(os.environ["envtoken"])
