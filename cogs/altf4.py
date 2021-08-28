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
  
  @commands.command(aliases=['s', 'Stats', 'STATS'])
  async def stats(ctx, user: discord.User=None):
        
    if not user:
      userid = ctx.author.id
      userat = ctx.author
    else:
      userid = user.id
      userat = user.name

    user = open_profile(ctx.author)
    shift_time = user["total_hours_worked"]
    shift_time_str = calculate_shift_time(shift_time)
          
    try:
      em = new_embed(title=f"{userat}'s stats",
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

  @commands.command(aliases=['lb', 'LB'])
  async def leaderboard(ctx, limit=10):
    leader_board = {}
    for user in db.keys():
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

  @commands.command(aliases=['wh','WH'])
  async def weeklyhours(ctx, limit=100):
    weekly_hours = {}
    for user in db.keys():
      u = json.loads(str(db[str(user)]))
      discord_user = await client.fetch_user(str(user))
      shift_time = u["weekly_hours_worked"]
      shift_time_str = calculate_shift_time(shift_time)
      
      total_amount = shift_time_str
      weekly_hours[total_amount] = discord_user.name
        
      keys = sorted(weekly_hours.keys(),reverse=True)

      em = discord.Embed(title = f"Weekly hours for employees!" , description = "Make sure to log these in excel before purging!!!",color = discord.Color(0xfa43ee))
      keys = keys[:limit]
      for index, amt in enumerate(keys):
        em.add_field(name = f"{index + 1}. {weekly_hours[amt]}", value = f"{amt}",  inline = False)

      await ctx.send(embed = em)  

  @client.command()
  @commands.has_role("Management")
  async def purge(ctx): 
    weeklyhours(ctx, limit=1000)

    for uid in db.keys():
      user = json.loads(str(db[str(uid)]))
      user["weekly_hours_worked"] = 0
      db[uid] = json.dumps(user)
    await ctx.send("Weekly hours have been purged")

  @client.command(aliases=['Reg','register'])
  async def Register(ctx):
    if str(ctx.author.id) in db.keys():
      await ctx.send("You Are Already Registered")
    else:
      ts = datetime.datetime.now()
      print("Registering user {}".format(ctx.author.id))
      js = {
          "Registered": True,
          "balance_owed": 0,
          "total_money_earned": 0,
          "total_passengers": 0,
          "join_date":ts.strftime('%x'),
          "cdin" : False,
          "total_flights" : 0,
          "shift_flights" : 0,
          "shift_passengers" : 0,
          "shift_wallet":0,
          "total_hours_worked":0,
          "clock_start":0,
          "clocked_in": False,
          "weekly_hours_worked": 0,
          "shift_time": 0
          }
      await ctx.send("You Are Now Registered")
      db[ctx.author.id] = json.dumps(js)
      return js

  @client.command()
  async def jd(ctx):
    user = open_profile(ctx.author)
    user["join_date"] = "08/25/21"
    db[ctx.author.id] = json.dumps(user)

  @client.command(aliases=['Flight','FLIGHT','fl', 'f'])
  async def flight(ctx, destination=None, passengers=None):
    user =  open_profile(ctx.author) 

    if user["clocked_in"] == False: 
      await ctx.send ("You are not clocked in")
    else:
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

    fm = new_embed(title=f"Ticket Collected {ctx.author.name}",
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

  @client.command(aliases=['ss','sstats',"shsta"])
  async def shstats (ctx, user: discord.User=None):
    if not user:
      userid = ctx.author.id
      userat = ctx.author
    else:
      userid = user.id
      userat = user.name
      
    user = open_profile(userat)
        
    if user["clocked_in"] == False:
      await ctx.send("You must be Clocked in")   
    else:  
      start_time = datetime.datetime.strptime(user["clock_start"], '%a, %b %d, %Y\n\n%I:%M:%S %p')
      shift_time_str = calculate_shift_time(start_time)
      
      try:
        em = new_embed(title=f"{userat}'s Shift Stats",
          fields={
            "Total Balance Owed": "${:,}".format(user["balance_owed"]),
            "Ticket Value This Shift": "${:,}".format(user["shift_wallet"]),
            "Flights during Shift": user["shift_flights"],
            "Passenger's during shift": user["shift_passengers"],
            "Hours worked this shift": shift_time_str,
          })
      except BaseException as e:
        em = discord.Embed(title=f"{userat}")
        em.add_field(name="debug", value=user)
        em.add_field(name="error", value=str(e))
      await ctx.send(embed=em)

  @client.command(aliases=['onduty', 'offduty', 'Onduty', 'Offduty', 'ofd', 'od'])
  @commands.has_role('Money Remover')
  async def clock(ctx, username: discord.User=None):
    if username is not None:
      uid = username
    else:
      uid = ctx.author

    user = open_profile(uid) 

    timestamp = datetime.datetime.now()
    now = timestamp.strftime('%a, %b %d, %Y\n\n%I:%M:%S %p')
    if user["clocked_in"] is not None and user["clocked_in"] == True:
      user["clocked_in"] = False
      start_time = datetime.datetime.strptime(user["clock_start"], '%a, %b %d, %Y\n\n%I:%M:%S %p')
      shift_time = (datetime.datetime.now() - start_time).total_seconds()
      user["shift_time"] = calculate_shift_time(start_time)

      user["total_hours_worked"] = user["total_hours_worked"] + shift_time
      user["weekly_hours_worked"] = user["weekly_hours_worked"] + shift_time
      fm = new_embed(title=f"{uid.name} has clocked out",
        fields={
          "Time on shift": user["shift_time"],
          "Total Flights this shift": user["shift_flights"],
          "Passengers this shift": user["shift_passengers"],
          "Shift earnings": "${:,}".format(user["shift_wallet"])
        })
      await ctx.send(embed=fm)
    else: # clocked_in is false-y
      user["clocked_in"] = True
      user["clock_start"] = now
      fm = new_embed(title=f"{uid.name} has clocked in",
        fields={"Start time": "{}".format(now)})
      await ctx.send(embed=fm)
      user["shift_flights"] = 0
      user["shift_wallet"] = 0
      user["shift_passengers"] = 0
   
    db[uid.id] = json.dumps(user)

  def calculate_shift_time(shift_time=None):
    shift_time_hrs = int(shift_time // 3600)
    shift_time_mins = int((shift_time % 3600) // 60)
    shift_time_secs = int(shift_time % 60)
    shift_time_str = "{} Hours, {} Minutes, {} Seconds".format(shift_time_hrs, shift_time_mins, shift_time_secs)
    return shift_time_str

  @client.command(aliases=['R','remove','Remove'])
  @commands.has_role("Management")
  async def r(ctx, user: discord.User=None):   
    user = open_profile(ctx.author)
    
    balance = user["balance_owed"]
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
         
    if earnings > 0: # generate invoice, and fork to log channel
      earning = earnings * -1
      fm = new_embed(title=f"{user.name}'s Invoice Created",
        fields={ "Payment Recieved": "${:,}".format (earnings), "Remaining Balance": "${:,}".format (user["balance_owed"] + earning)})
      await ctx.send(embed=fm)

      #this is the log channel numeric ID
      channel = client.get_channel(880002977753071626) 
      earning = earnings * -1
      fm = new_embed(title=f"{user.name}'s remove log",
        fields={ "Payment From": user.name, "Payment Received": earning })
      await channel.send(embed=fm)
      
    else:
      ctx.send("!remove @Person Amount") 
     
     
    user["balance_owed"] = balance + earning
    db[str(user.id)] = json.dumps(user)

  def open_profile(user):
    if str(user.id) in db.keys():
      js = json.loads(str(db[str(user.id)]))
      for field in [
          "balance_owed",
          "total_money_earned",
          "total_passengers",
          "total_flights",
          "join_date",
          "clock_start",
          "clocked_in",
          "total_hours_worked",
          "shift_wallet",
          "shift_passengers",
          "shift_flights",
          "weekly_hours_worked",
          "shift_time"
          ]:
        try:
          tmp = js[field]
          db[user.id] = json.dumps(js)
        except:
          js[field] = 0
          db[user.id] = json.dumps(js)
      return js
    else:
      await user.send("You Need to Register")

  def new_embed(title=None, fields=None, **kwargs):
    fm = discord.Embed(title=f"{title}",color=0x96DDFF)
    fm.set_thumbnail(url="https://www.jetforums.net/attachments/piperjet-aircraft-jpg.319/")
    for key in fields:
       fm.add_field(name=key, value=fields[key], inline=False)
    fm.set_footer(text="Aeron Flight Bot v1.0")
    return fm

def setup(client):
      client.add_cog(Altf4(client))
