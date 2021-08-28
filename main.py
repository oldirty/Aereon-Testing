#module Imports
import discord
import os, requests, json
import math, time, datetime
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
#875893971350609953 - test server
@client.event
async def on_member_join(member):
    channel = client.get_channel(865731272919744535)
    await channel.send(
        "Welcome to AltF4 Airlines discord! When ready head down to ACAP for a interview! Good luck!")
#UPDATED CHANNEL TO ALTF4 Airlines welcome channel
@client.event
async def on_member_remove(member):
    channel = client.get_channel(865731272919744535)
    await channel.send("Hah, later nerd!")

#----------------------------------------------------------------------------
#----------------------------------DB FIDDLING-------------------------------
#----------------------------------------------------------------------------



#----------------------------------------------------------------------------
#-----------------------------------STATS COMMAND----------------------------
#----------------------------------------------------------------------------
@client.command(aliases=['s', 'Stats', 'STATS'])
async def stats(ctx, user: discord.User=None):
    
    if not user:
      userid = ctx.author.id
      userat = ctx.author
    else:
      userid = user.id
      userat = user.name

    await open_profile(ctx.author)
    try:
      user = json.loads(str(db[str(userid)]))
    except KeyError as e:
      fm = newEmbed(title=f"{user} is not registered!", fields={
        "Error": f"Unrecognized or unregistered user: {user}"
      })
      ctx.send(embed=fm)
      
    shift_time = user["total_hours_worked"]
    shift_time_hrs = int(shift_time // 3600)
    shift_time_mins = int((shift_time % 3600) // 60)
    shift_time_secs = int(shift_time % 60)
    shift_time_str = "{} Hours, {} Minutes, {} Seconds".format(shift_time_hrs, shift_time_mins, shift_time_secs)

      
    try:
      em = newEmbed(title=f"{userat}'s stats",
        fields={
          "Balance Owed": "${:,}".format(user["balance_owed"]),
          "Life Time Hours Worked": shift_time_str,
          "Life Time Flights:": user["total_flights"],
          "Lifetime Passengers": user["total_passengers"],
          "Lifetime Ticket Value": "${:,}".format(user["total_money_earned"]),
          "Pilot Join Date": user["join_date"],
          })
    
    except BaseException as e:
      em = discord.Embed(title=f"{userat}")
      em.add_field(name="debug", value=user)
      em.add_field(name="error", value=str(e))
    await ctx.send(embed=em)
#----------------------------------------------------------------------------
#----------------------------------Leader-Board----------------------------
#----------------------------------------------------------------------------
@client.command(aliases=['lb', 'LB'])
async def leaderboard(ctx, limit=10):
    users = await get_profile_data()
    leader_board = {}
    for user in users:
      u = json.loads(str(db[str(user)]))
      discord_user = await client.fetch_user(str(user))
    
  
      total_amount = u["total_money_earned"]
      leader_board[total_amount] = discord_user.name
    
    keys = sorted(leader_board.keys(),reverse=True)

    em = discord.Embed(title = f"Top {limit} Earners!" , description = "This is decided on the basis of Total Lifetime Ticket Value",color = discord.Color(0xfa43ee))
    keys = keys[:limit]
    for index, amt in enumerate(keys):
        em.add_field(name = f"{index + 1}. {leader_board[amt]}" , value = f"${amt:,}",  inline = False)

    await ctx.send(embed = em)
################################################################################################################################################################################
@client.command(aliases=['wh','WH'])
async def weeklyhours(ctx, limit=100):
    users = await get_profile_data()
    weekly_hours = {}
    for user in users:
      u = json.loads(str(db[str(user)]))
      discord_user = await client.fetch_user(str(user))
      shift_time = u["weekly_hours_worked"]
      shift_time_hrs = int(shift_time // 3600)
      shift_time_mins = int((shift_time % 3600) // 60)
      shift_time_secs = int(shift_time % 60)
      shift_time_str = "{} Hours, {} Minutes, {} Seconds".format(shift_time_hrs, shift_time_mins, shift_time_secs)
  
      total_amount = shift_time_str
      weekly_hours[total_amount] = discord_user.name
    
    keys = sorted(weekly_hours.keys(),reverse=True)

    em = discord.Embed(title = f"Weekly hours for employees!" , description = "Make sure to log these in excel before purging!!!",color = discord.Color(0xfa43ee))
    keys = keys[:limit]
    for index, amt in enumerate(keys):
        em.add_field(name = f"{index + 1}. {weekly_hours[amt]}", value = f"{amt}",  inline = False)

    await ctx.send(embed = em)  

@client.command()
#@commands.has_role("Management")
async def purge(ctx): 
  weeklyhours(ctx, limit=1000)
  users = await get_profile_data()

  for uid in users:
    user = json.loads(str(db[str(uid)]))
    user["weekly_hours_worked"] = 0
    db[uid] = json.dumps(user)
  await ctx.send("Weekly hours have been purged")
#=======================================================================================
#------------------------------Infintitys-register--------------------------------------
#=======================================================================================
@client.command(aliases=['Reg','register'])
async def Register(ctx):
    users = await get_profile_data()
    
    if str(ctx.author.id) in users:
     await ctx.send("You Are Already Registered")
    else:
       
      ts = datetime.datetime.now() # Gets Date from right now and set it to TS
      print("Registering user {}".format(ctx.author.id))
      js = {"Registered": True, "balance_owed": 0, "total_money_earned": 0, "total_passengers": 0, "join_date":ts.strftime('%x'), "cdin" : False , "total_flights" : 0, "shift_flights" : 0,"shift_passengers" : 0,"shift_wallet":0,"total_hours_worked":0, "clock_start":0, "clocked_in"  : False,"weekly_hours_worked": 0 } #added try to this and line 89/95
     # Sets join_date value to right nows date though ts.strtime("%x") when a new person
     # Creates a profile and Registers
      await ctx.send("You Are Now Registered")
      db[ctx.author.id] = json.dumps(js)
      return js
#=======================================================================================
#=======================================================================================
@client.command()
async def jd(ctx):
  await open_profile(ctx.author)
  try:
    user = json.loads(str(db[str(ctx.author.id)]))
  except KeyError as e:
    fm = newEmbed(title=f"{user} is not registered!", fields={
      "Error": f"Unrecognized or unregistered user: {user}"
    })
    ctx.send(embed=fm)
  user["join_date"] = "08/25/21"
  db[ctx.author.id] = json.dumps(user)
#----------------------------------------------------------------------------
#----------------------------------FLIGHT COMMAND----------------------------
#----------------------------------------------------------------------------
@client.command(aliases=['Flight','FLIGHT','fl', 'f'])
async def flight(ctx, destination=None, passengers=None):
    await open_profile(ctx.author) 
    try:
        user = json.loads(str(db[str(ctx.author.id)]))
    except:
        print("Unexpected value in #add: {}".format(db[str(ctx.author.id)]))
        
    tlp =  user["total_flights"] + (int(1)) 
    balance = user["balance_owed"]
    tbal = user["total_money_earned"]
    total_passengers = user["total_passengers"]

    destination = destination.lower()
    destinations = {
      "bloon": 2500,
      "sky": 2500,
      "scuba": 3500,
      "pudo": 2500,
      "sked": 1500,
      "vip": 4000,
    } 
    
    if destination is not None and passengers is not None:
      if destination in destinations.keys():
        try:
          earnings = int(passengers) * destinations[destination]
        except:
          await ctx.send(f"Invalid `passengers` value: {passengers}")
      else:
        await ctx.send(f"Invalid destination: {destination}")
    else:
      await ctx.send(f"Usage: `!flight <destination> <passengers>`")

    fm = newEmbed(title=f"Ticket Collected {ctx.author.name}",
      fields={ "Passengers": passengers, "Ticket Value": "${:,}".format (earnings)})
    await ctx.send(embed=fm)
    
    
    user["total_flights"] = tlp
    user["total_money_earned"] = earnings + tbal
    user["total_passengers"] = total_passengers + int(passengers)
    user["balance_owed"] = balance + earnings
    user["shift_wallet"] = user["shift_wallet"] + earnings
    user["shift_passengers"] = user["shift_passengers"] + int(passengers)
    user["shift_flights"] = user["shift_flights"] + 1
    db[str(ctx.author.id)] = json.dumps(user)
#=============================================================================================================================================================================================================================================
#@client.command()
#async def shstats (ctx, username: discord.User=None):
# print("Hello")

  


#===================================================================================================================================================================================================================
@client.command(aliases=['onduty', 'offduty', 'Onduty', 'Offduty', 'ofd', 'od'])
#@commands.has_role('Money Remover')
async def clock(ctx, username: discord.User=None):
  if username is not None:
    uid = username
  else:
    uid = ctx.author

  await open_profile(uid) 
  try:
        user = json.loads(str(db[str(uid.id)]))
  except:
        print("Unexpected value in #clock: {}".format(db[str(uid.id)]))

  timestamp = datetime.datetime.now()
  now = timestamp.strftime('%a, %b %d, %Y\n\n%I:%M:%S %p')
  # odirzy snippy time fun for python date format garbo '%a %b %d %H:%M:%S %Y
  if user["clocked_in"] is not None and user["clocked_in"] == True:
    user["clocked_in"] = False
    start_time = datetime.datetime.strptime(user["clock_start"], '%a, %b %d, %Y\n\n%I:%M:%S %p')
    end_time = datetime.datetime.now()
    shift_time = (end_time - start_time)
    shift_time_hrs = int(shift_time.total_seconds() // 3600)
    shift_time_mins = int((shift_time.total_seconds() % 3600) // 60)
    shift_time_secs = int(shift_time.total_seconds() % 60)
    shift_time_str = "{} Hours, {} Minutes, {} Seconds".format(shift_time_hrs, shift_time_mins, shift_time_secs)

    user["total_hours_worked"] = user["total_hours_worked"] + shift_time.total_seconds()
    user["weekly_hours_worked"] = user["weekly_hours_worked"] + shift_time.total_seconds()
    fm = newEmbed(title=f"{uid.name} has clocked out",
      fields={
        "Time on shift": shift_time_str,
        "Total Flights this shift": user["shift_flights"],
        "Passengers this shift": user["shift_passengers"],
        "Shift earnings": "${:,}".format(user["shift_wallet"])
      })
    await ctx.send(embed=fm)
  else: # clocked_in is false-y
    user["clocked_in"] = True
    user["clock_start"] = now
    fm = newEmbed(title=f"{uid.name} has clocked in",
      fields={"Start time": "{}".format(now)})
    await ctx.send(embed=fm)
 
  
  user["shift_flights"] = 0
  user["shift_wallet"] = 0
  user["shift_passengers"] = 0
  db[uid.id] = json.dumps(user)
#------------------------------------------------REMOVECOMMAND------------------------------
#-------------------------------------------------------------------------------------------
@client.command(aliases=['R','remove','Remove'])
#@commands.has_role("Management")
async def r(ctx, user: discord.User=None):   

    Userid = user.id # same as previous
    UserAt = user.name
    await open_profile (ctx.author)
  
    try:
        user = json.loads(str(db[str(Userid)]))
    except:
        print("Unexpected value in #r: {}".format(db[str(Userid)]))
    balance = user["balance_owed"]
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
      fm = newEmbed(title=f"{UserAt}'s Invoice Created",
        fields={ "Payment Recieved": "${:,}".format (earnings), "Remaining Balance": "${:,}".format (user["balance_owed"] + earning)})
      ##fm.add_field(name="Life Time Passangers", value= user["total_passengers"] + psngr)##
      await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))

    if earnings > 0: #PUSH TO LOG CHANNEL
      channel = client.get_channel(880002977753071626) 
      #This Tells it were to sent the message

      earning = earnings * -1
      fm = newEmbed(title=f"{UserAt}'s remove log",
        fields={ "Payment From": UserAt, "Payment Received": earning })
      await channel.send(embed=fm)  #("{} added to {}".format(earnings, balance))
    
    else:
      ctx.send("!remove @Person Amount") 
   
   
    user["balance_owed"] = balance + earning
    db[str(Userid)] = json.dumps(user)
#----------------------------------------------------------------------------
#----------------------------------CREATE USER PROFLE------------------------
#----------------------------------------------------------------------------
async def open_profile(user):
    users = await get_profile_data()
    
    if str(user.id) in users:
      js = json.loads(str(db[str(user.id)]))
      for field in ["balance_owed", "total_money_earned", "total_passengers", "total_flights", "join_date", "clock_start", "clocked_in", "total_hours_worked", "shift_wallet", "shift_passengers", "shift_flights", "weekly_hours_worked"]:
        try:
          tmp = js[field]
          db[user.id] = json.dumps(js)
        except:
          js[field] = 0
          db[user.id] = json.dumps(js)
      return js
    else:
      await user.send("You Need to Register")


def newEmbed(title=None, fields=None, **kwargs):
  fm = discord.Embed(title=f"{title}",color=0x96DDFF)
  fm.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
  for key in fields:
     fm.add_field(name=key, value=fields[key], inline=False)
  fm.set_footer(text="Aeron Flight Bot v1.0")
  return fm
#----------------------------------------------------------------------------
#----------------------------Variable that holds DB INFO---------------------
#----------------------------------------------------------------------------
async def set_role():
    return
  
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
#${:,.2f}
#
#this is fucking stupid
#
# TO DO: Log channel for remove command || Leaderboard || Clock in/out 