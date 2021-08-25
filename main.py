#Module Imports
import discord
import os
import requests
import json
import math
import time
from discord.ext.commands import MissingPermissions
from replit import db
from keep_alive import keep_alive
from discord.ext import commands
#-----------------------------------------------------------------------------
#--------------------------------INTENT SETUP---------------------------------
#-----------------------------------------------------------------------------
intents = discord.Intents.default()
intents.members = True
#-----------------------------------------------------------------------------
#-------------------------Print DB / REMOVE USER FROM DB----------------------
#-----------------------------------------------------------------------------
#print(db.keys())
#del db["Key"]
#-----------------------------------------------------------------------------
#------------------------------COMMAND PREFIX---------------------------------
#-----------------------------------------------------------------------------
client = commands.Bot(command_prefix="!", intents=intents)
#-----------------------------------------------------------------------------
#-------------------------------BOT CONSOLE LOG-------------------------------
#-----------------------------------------------------------------------------
@client.event
async def on_ready():
    print("Aeron Flight Bot v1.0")
    #print(os.getenv("REPLIT_DB_URL"))
#-----------------------------------------------------------------------------
#-------------------------------COG SETUP-------------------------------------
#-----------------------------------------------------------------------------
initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)
#----------------------------------------------------------------------------
#-----------------------------------JOIN/LEAVEMESSAGES-----------------------
#----------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    channel = client.get_channel(875893971350609953)
    await channel.send(
        "Welcome to AltF4 Airlines discord! When ready head down to ACAP for a interview! Good luck!")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(875893971350609953)
    await channel.send("Hah, later nerd!")
#----------------------------------------------------------------------------
#-----------------------------------STATS COMMAND----------------------------
#----------------------------------------------------------------------------
@client.command()
async def stats(ctx,user: discord.User=None ):
    if not user:
      userid = ctx.author.id
      userat = ctx.author
    else:
      userid = user.id
      userat = user.name

    await open_profile(ctx.author)
    user = json.loads(str(db[str(userid)]))

    try:
      em = discord.Embed(title=f"{userat}'s stats", url="https://google.com", color =0x96DDFF)
      em.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
      em.add_field(name="Balance Owed", value=user["wallet"], inline=False)
      em.add_field(name="Life Time Passengers", value=user["try"], inline=False)
      em.add_field(name="Life Time Ticket Value ", value=user["bank"], inline=False)
      em.set_footer(text="Aeron Flight Bot v1.0")
    except:
      em = discord.Embed(title=f"{userat}")
      em.add_field(name="debug", value=user)
    await ctx.send(embed=em)
#----------------------------------------------------------------------------
#----------------------------------FLIGHT COMMAND----------------------------
#----------------------------------------------------------------------------
@client.command()
async def flight(ctx):
    await open_profile(ctx.author)
      
    try:
        user = json.loads(str(db[str(ctx.author.id)]))
    except:
        print("Unexpected value in #add: {}".format(db[str(ctx.author.id)]))
    balance = user["wallet"]
    tbal = user["bank"]
    Passanger = user["try"]
    psngr = int()
    arguments = ctx.message.content.split(' ')

    if 'vip' in ctx.message.content:
     for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)    
        except:
            pass
        vipt = 4000
        earnings = psngr * vipt
        tearn = psngr * vipt

    elif 'sked' in ctx.message.content:
      for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)
        except:
            pass
        skedt = 1500    
        earnings = psngr * skedt
        tearn = psngr * skedt

    elif 'bloon' in ctx.message.content:
      for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)
        except:
            pass
        balloon = 2500
        earnings = psngr * balloon
        tearn = psngr * balloon

    elif 'sky' in ctx.message.content:
      for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)
        except:
            pass
        sky = 2500
        earnings = psngr * sky
        tearn = psngr * sky

    elif 'scuba' in ctx.message.content:
      for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)
        except:
            pass
        scuba = 3500
        earnings = psngr * scuba
        tearn = psngr * scuba

    elif 'pudo' in ctx.message.content:
      for arg in arguments:
        try:
            int(arg)
            psngr = int(arg)
        except:
            pass
        pudo = 2500
        earnings = psngr * pudo
        tearn = psngr * pudo
              
    else:
     await ctx.send('You have entered a invalid flight type')
     return        

    fm = discord.Embed(title=f"Ticket Collected {ctx.author.name}", url="https://google.com", color=0x96DDFF)
    fm.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
    fm.add_field(name="Passengers", value= "{}".format(psngr, inline=False))
    fm.add_field(name="Ticket Value", value= "{}".format(earnings), inline=False)
    fm.set_footer(text="Aeron Flight Bot v1.0")
    #fm.add_field(name="Balance Owed", value= user["wallet"] + earnings, inline=False) - NOT NEEDED???
    ##fm.add_field(name="Life Time Passangers", value= user["try"] + psngr)## - DONT NEED
    await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))
    
    user["bank"] = tearn + tbal
    user["try"] = Passanger + psngr
    user["wallet"] = balance + earnings
    db[str(ctx.author.id)] = json.dumps(user)
#----------------------------------------------------------------------------
#-----------------------------------REMOVE COMMAND---------------------------
#----------------------------------------------------------------------------
@client.command()
@commands.has_role("Management")
async def remove(ctx, user: discord.User=None):   

    Userid = user.id # same as previous
    UserAt = user.name
    await open_profile (ctx.author)
  
    try:
        user = json.loads(str(db[str(Userid)]))
    except:
        print("Unexpected value in #add: {}".format(db[str(Userid)]))
    balance = user["wallet"]
    earnings = int()
    arguments = ctx.message.content.split(' ')
      
    for arg in arguments:
        try:
            int(arg)
            earnings = int(arg)
        except:
            pass
        
    if earnings < 0:
      await ctx.send('Please Use a Postive Number.')
      return          
       
    if earnings > 0:
      earning = earnings * -1
      fm = discord.Embed(title=f"{UserAt}'s' Invoice Created",color=0x96DDFF)
      fm.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
      fm.add_field(name="Payment Recieved", value= "{}".format(earning))
      fm.add_field(name="Remaining Balance", value= user["wallet"] + earning, inline=False)
      fm.set_footer(text="Aeron Flight Bot v1.0")
      ##fm.add_field(name="Life Time Passangers", value= user["try"] + psngr)##
      await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))
    
    user["wallet"] = balance + earning
    
@remove.error
async def clear_error(ctx, error,user: discord.User=None):
 if isinstance(error, commands.errors.UserNotFound):
    
    
    await open_profile(ctx.author)
    try:
      user = json.loads(str(db[str(ctx.author.id)]))
    except:
        print("Unexpected value in #add: {}".format(db[str(ctx.author.id)]))
    balance = user["wallet"]
    earnings = int()
    arguments = ctx.message.content.split(' ')

    for arg in arguments:
        try:
            int(arg)
            earnings = int(arg)
        except:
            pass

    if earnings < 0:
      await ctx.send('Please Use a Postive Number.')
      return

    if earnings > 0:
      earning = earnings * -1
      fm = discord.Embed(title=f"{ctx.author.name}'s Invoice Created",color=0x96DDFF)
      fm.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
      fm.add_field(name="Payment Recieved", value= "{}".format(earning))
      fm.add_field(name="Remaining Balance", value= user["wallet"] + earning, inline=False)
      fm.set_footer(text="Aeron Flight Bot v1.0")
      ##fm.add_field(name="Life Time Passangers", value= user["try"] + psngr)##
      await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))
   
    else:
      ctx.send("!remove @Person Amount") 
   
   
    user["wallet"] = balance + earning
    db[str(ctx.author.id)] = json.dumps(user)
 #----------------------------------------------------------------------------
#----------------------------------CREATE USER PROFLE------------------------
#----------------------------------------------------------------------------
async def open_profile(user):
    users = await get_profile_data()
    
    if str(user.id) in users:
      js = json.loads(str(db[str(user.id)]))
      for field in ["wallet", "bank", "try", "lttv"]:
        try:
          tmp = js[field]
          db[user.id] = json.dumps(js)
        except:
          js[field] = 0
          db[user.id] = json.dumps(js)
      return js
    else:
      print("Registering user {}".format(user.id))
      js = {"Registered": True, "wallet": 0, "bank": 0, "try": 0} #added try to this and line 89/95
      db[user.id] = json.dumps(js)
      return js
#----------------------------------------------------------------------------
#----------------------------Variable that holds DB INFO---------------------
#----------------------------------------------------------------------------
async def get_profile_data():
    return db.keys()
#----------------------------------------------------------------------------
#--------------------------------KEEP ALIVE----------------------------------
#----------------------------------------------------------------------------
keep_alive()
#----------------------------------------------------------------------------
#--------------------------------CLIENT RUN----------------------------------
#----------------------------------------------------------------------------
client.run(os.environ['envtoken'])
#----------------------------------------------------------------------------
#-------------------------------TEMPLATES------------------------------------
#----------------------------------------------------------------------------
#                 @command.has_any_role(ENTER ROLE ID)
#
#
#
#
#this is fucking stupid
#