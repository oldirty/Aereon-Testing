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

    try:
      em = newEmbed(title=f"{userat}'s stats",
        fields={
          "Balance Owed": "${:,}".format(user["wallet"]),
          "Life Time Flights:": user["tft"],
          "Lifetime Passengers": user["try"],
          "Lifetime Ticket Value": "${:,}".format(user["bank"]),
          "Pilot Join Date": user["jdate"],
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
      
      total_amount = u["bank"] + u["wallet"]
      leader_board[total_amount] = discord_user.name

    keys = sorted(leader_board.keys(),reverse=True)

    em = discord.Embed(title = f"Top {limit} Earners!" , description = "This is decided on the basis of Total Lifetime Ticket Value",color = discord.Color(0xfa43ee))
    keys = keys[:limit]
    for index, amt in enumerate(keys):
        em.add_field(name = f"{index + 1}. {leader_board[amt]}" , value = f"${amt:,}",  inline = False)

    await ctx.send(embed = em)
#---------------------------------------------------------------------------------------
#---------------------------Dirty-Register--------------------------------------------------------------------------------------------------------------------------------------
#@client.command(aliases=['Reg','register'])
#async def Register(ctx):
 # await open_profile(ctx.author, register=True)
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
      js = {"Registered": True, "wallet": 0, "bank": 0, "try": 0, "jdate":ts.strftime('%x'), "cdin" : False } #added try to this and line 89/95
     # Sets jdate value to right nows date though ts.strtime("%x") when a new person
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
  user["jdate"] = "08/25/21"
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
        
    tlp =  user["tft"] + (int(1)) 
    balance = user["wallet"]
    tbal = user["bank"]
    total_passengers = user["try"]

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
    
    user["tft"] = tlp
    user["bank"] = earnings + tbal
    user["try"] = total_passengers + int(passengers)
    user["wallet"] = balance + earnings
    user["shift_wallet"] = user["shift_wallet"] + earnings
    user["shift_passengers"] = user["shift_passengers"] + passengers
    user["shift_flights"] = user["shift_flights"] + 1
    db[str(ctx.author.id)] = json.dumps(user)

#======================================================================================================================================================================================================================================================================    
@client.command(aliases=['onduty', 'offduty', 'Onduty', 'Offduty'])
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
    start_time = datetime.datetime.strptime(user["cistart"], '%a, %b %d, %Y\n\n%I:%M:%S %p')
    end_time = datetime.datetime.now()
    shift_time = (end_time - start_time)
    print(shift_time)
    #shift_time = datetime.timedelta(seconds=int(shift_time.total_seconds())) - somewhat working

   
    fm = newEmbed(title=f"{uid.name} has clocked out",
      fields={
        "Time on shift": shift_time,
        "Total Flights this shift": user["shift_flights"],
        "Passengers this shift": user["shift_passengers"],
        "Shift earnings": "${:,}".format(user["shift_wallet"])
      })
    await ctx.send(embed=fm)
  else: # clocked_in is false-y
    user["clocked_in"] = True
    user["cistart"] = now
    fm = newEmbed(title=f"{uid.name} has clocked in",
      fields={"Start time": "{}".format(now)})
    await ctx.send(embed=fm)
    
  user["shift_flights"] = 0
  user["shift_wallet"] = 0
  user["shift_passengers"] = 0
  db[uid.id] = json.dumps(user)

#------------------------------------------------REMOVECOMMAND--------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

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
      fm = newEmbed(title=f"{ctx.author}'s Invoice Created",
        fields={ "Payment Recieved": "${:,}".format (earnings), "Remaining Balance": "${:,}".format (user["wallet"] + earning)})
      ##fm.add_field(name="Life Time Passangers", value= user["try"] + psngr)##
      await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))

    if earnings > 0: #PUSH TO LOG CHANNEL
      channel = client.get_channel(880002977753071626)

      earning = earnings * -1
      fm = newEmbed(title=f"{ctx.author}'s remove log",
        fields={ "Payment From": "${:,}".format(UserAt), "Payment Received": "${:,}".format (earnings)})
      ##fm.add_field(name="Life Time Passangers", value= user["try"] + psngr)##
      await channel.send(embed=fm)  #("{} added to {}".format(earnings, balance))
      
    user["wallet"] = balance + earning
    db[str(Userid)] = json.dumps(user)
    
@r.error
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
      await ctx.send('Please Use a Positive Number.')
      return

    if earnings > 0:
      earning = earnings * -1
      fm = newEmbed(title=f"{ctx.author.name}'s Invoice Created",
        fields={"Payment Received": "${:,}".format (earnings), "Remaining Balance": "${:,}".format (user["wallet"] + earning)})

      await ctx.send(embed=fm)  #("{} added to {}".format(earnings, balance))
   
    if earnings > 0: #PUSH TO LOG CHANNEL
      channel = client.get_channel(880002977753071626) 
      #This Tells it were to sent the message

      earning = earnings * -1
      fm = newEmbed(title=f"{ctx.author}'s remove log",
        fields={ "Payment From": ctx.author, "Payment Received": earning })
      await channel.send(embed=fm)  #("{} added to {}".format(earnings, balance))
    
    else:
      ctx.send("!remove @Person Amount") 
   
   
    user["wallet"] = balance + earning
    db[str(ctx.author.id)] = json.dumps(user)
#----------------------------------------------------------------------------
#----------------------------------CREATE USER PROFLE------------------------
#----------------------------------------------------------------------------
#================================ Dirtys =======================================
#async def open_profile(user, register=False):
#    users = await get_profile_data()
#    
#    if str(user.id) in users and register == False:
#      js = json.loads(str(db[str(user.id)]))
#      for field in ["wallet", "bank", "try",
#       "tft", "jdate", "cistart", "cbank","cwallet",
#       "clocked_in", "shift", "shift_wallet", "shift_flights",
#       "shift_passengers", "totaltime"]:
#        try:
#          tmp = js[field]
#          db[user.id] = json.dumps(js)
#        except:
#          js[field] = 0
#          db[user.id] = json.dumps(js)
#      return js
#    else:
#      fm = newEmbed(title=f"{user} is not registered!", fields={
#        "Error": f"Unrecognized or unregistered user: {user}"
#      })
    
    
#    if register == True:
#      ts = datetime.datetime.now() # Gets Date from right now and set it to TS
#      print("Registering user {}".format(user.id))
#      js = {"Registered": True, "wallet": 0, "bank": 0, "try": 0, "jdate":ts.strftime('%x'), "clocked_in" : False } #added try to this and line 89/95
     # Sets jdate value to right nows date though ts.strtime("%x") when a new person
     # Creates a profile and Registers
      
#      db[user.id] = json.dumps(js)
#      return js
#    else:
#      fm = newEmbed(title=f"{user} is not registered!", fields={
#        "Error": f"Unrecognized or unregistered user: {user}"
#      })
#======================================================================================
#=============================== Infintiys============================================
async def open_profile(user):
    users = await get_profile_data()
    
    if str(user.id) in users:
      js = json.loads(str(db[str(user.id)]))
      for field in ["wallet", "bank", "try", "tft", "jdate", "cistart", "cbank","cwallet", "cdin", "shift","totaltime"]:
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