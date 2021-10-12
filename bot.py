# Imports
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands as commands
from discord.ext import tasks
import random
from datetime import datetime, timedelta
import flag_module
import player_module
import inventory_module

# Loads Dotenv File
load_dotenv()

# Discord Initialise
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
vc = None
players = None
crate = flag_module.Crate()
scores = {}
bot = commands.Bot(command_prefix="$", intents=intents)
last_drop = None
next_drop = None

@bot.command() # Lets the Players Enter the Game
async def entergame(ctx):
    flag = 0
    for player in players:
        if player.name == f"{ctx.author}":
            flag = 1
            break
    if not flag:
        name = f"{ctx.author}"
        player = player_module.Player(name)
        players.append(player)
        await ctx.channel.send(f"Welcome to the game {ctx.author}")
    else:
        await ctx.channel.send("You are already in the game")

@bot.command() # Lets a user in the server back up the game data
async def backup(ctx):
    player_module.backup(players)
    await ctx.channel.send("Game backed up successfully")

@bot.command() # The bot joins the discord
async def join(ctx):
    discord.opus.load_opus(
        "C:/Users/fawth/Desktop/Programming/Other/DiscordBot/venv/Lib/site-packages/discord/bin/libopus-0.x64.dll")
    channel = ctx.author.voice.channel
    global vc
    vc = await channel.connect()

@bot.command() # The bot makes a fart noise
async def fart(ctx):
    if (vc == None):
        await ctx.channel.send("ERROR please try $join")
    else:
        x = random.randint(1, 4)
        try:
            vc.play(discord.FFmpegPCMAudio(f'C:/Users/fawth/Desktop/Programming/Other/DiscordBot/audio/fart{x}.mp4'))
        except:
            await ctx.channel.send("Please wait until the current audio is finished")

@tasks.loop(seconds=7200) # Gives each player a new roll
async def crateDrop():
    global next_drop
    global last_drop
    now = datetime.now()
    last_drop = now.strftime("%H:%M:%S")
    now = datetime.now() + timedelta(hours=2)
    next_drop = now.strftime("%H:%M:%S")
    print("Players Gettin Moolah")
    for player in players:
        player.setBal(3)

@tasks.loop(seconds=60) # Does an automatic back up
async def backup():
    print("Game Backed Up")
    player_module.backup(players)

@bot.command() # Lists the players in the console
async def playerlist(ctx):
    print("Players in the game:")
    for player in players:
        print(player)

@bot.command() # Prints the Tierlist for the flags in the chat
async def flaglist(ctx):
    await ctx.channel.send(file=discord.File('flags/FlagList.PNG'))

@bot.command() # A player can use one of their roll tokens to get a flag
async def roll(ctx):
    name = f"{ctx.author}"
    index = -1
    for i in range(len(players)):
        if players[i].name == name:
            index = i
            break

    if index == -1:
        await ctx.channel.send("It seems that you are not part of the game, use $entergame to enter this seasons game, if you think there has been a mistake please put a message in the game-bugs")
        return

    if players[index].bal < 1:
        await ctx.channel.send("Sorry you dont have the credits to do that, you will get one more roll within the next hour")
    else:
        players[index].bal -= 1
        flag = crate.open()
        await ctx.channel.send(f"{flag.rarity.upper()}: {flag.name}")
        await ctx.channel.send(file=discord.File(flag.image))
        players[index].inventory.add_flag(flag.name, 1)

@bot.command() # Lets the player view their balance
async def bal(ctx):
    name = f"{ctx.author}"
    index = -1
    for i in range(len(players)):
        if players[i].name == name:
            index = i
            break

    if index == -1:
        await ctx.channel.send("It seems that you are not part of the game, use $entergame to enter this seasons game, if you think there has been a mistake please put a message in the game-bugs")
        return

    await ctx.channel.send(f"You have {players[index].bal} rolls left.")

@bot.command()
async def inventory(ctx):
    name = f"{ctx.author}"
    index = -1
    for i in range(len(players)):
        if players[i].name == name:
            index = i
            break

    if index == -1:
        await ctx.channel.send("It seems that you are not part of the game, use $entergame to enter this seasons game, if you think there has been a mistake please put a message in the game-bugs")
        return
    output = "It seems you do not currently have flags, use $roll to try your luck"
    if players[index].inventory.current_flag_count != 0:
        output = players[index].inventory.getFlags()
        output += "\n\n\n"
        temp, outputList = players[index].inventory.getMissing()
        output += temp

    await ctx.channel.send(output)

@bot.command()
async def scoreboard(ctx):
    await verify(ctx)
    scores = {}
    for player in players:
        scores[player.name] = player.inventory.score
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    output = ""
    counter = 1
    for name, score in scores:
        output += f"{counter}: {name} {score}\n"
        counter += 1
    await ctx.channel.send(output)

@bot.command()
async def verify(ctx):
    for player in players:
        player.inventory.checkScore()
    await ctx.channel.send("The scoreboard has been updated")

@bot.command()
async def time(ctx):
    await ctx.channel.send(f"The last drop was at be {last_drop}, the next will be at {next_drop}")

@bot.command()
async def claim(ctx, arg):

    name = f"{ctx.author}"
    index = -1
    for i in range(len(players)):
        if players[i].name == name:
            index = i
            break

    if index == -1:
        await ctx.channel.send(
            "It seems that you are not part of the game, use $entergame to enter this seasons game, if you think there has been a mistake please put a message in the game-bugs")
        return


    if (not players[index].inventory.claim(arg)):
        await ctx.channel.send("Bro you are Pohara wait till you have all of them")
    else:
        await ctx.channel.send("Success you claimed your flags")

def main():
    """Runs when bot starts"""
    global players
    global crate
    crate = flag_module.load_crate("testflag.txt")
    flag_module.group_score_set("group_data.txt", crate)
    inventory_module.inventory_init(crate)
    players = player_module.load_players()
    crateDrop.start()
    backup.start()
    print("Bot Initialised")

if __name__ == "__main__":
    main()

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
