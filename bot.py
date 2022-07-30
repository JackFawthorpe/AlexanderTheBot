# Imports
import os
import discord
from discord.ext import commands as commands
from discord.ext import tasks
import random
from datetime import datetime, timedelta
import flag_module
import player_module
import inventory_module
import game


DISCORD_TOKEN = "ODkyNzExMjIyMDE1ODQ0Mzky.YVQ4HQ.uLejQapSVGa-MMFwl3xrKlzhoY0"
DISCORD_GUILD = "884549583764602921"

# Discord Initialise
intents = discord.Intents.default()
intents.members = True
vc = None
players = None
crate = flag_module.Crate()
scores = {}
bot = commands.Bot(command_prefix="$", intents=intents)
last_drop = None
next_drop = None

@bot.command()  # The bot joins the discord
async def join(ctx):
    discord.opus.load_opus(
        "/home/pi/AlexanderTheBot/libopus-0.x86.dll")
    channel = ctx.author.voice.channel
    global vc
    vc = await channel.connect()


# Requested by my younger sibling (Look away please!)
@bot.command()  # The bot makes a fart noise
async def fart(ctx):
    if (vc == None):
        await ctx.channel.send("ERROR please try $join")
    else:
        x = random.randint(1, 7)
        try:
            vc.play(discord.FFmpegPCMAudio(f'/home/pi/AlexanderTheBot/audio/fart{x}.mp4'))
        except:
            await ctx.channel.send("Please wait until the current audio is finished")


@bot.command()  # Gives the player the time until the next roll drop
async def time(ctx):
    await ctx.channel.send(f"The last drop was at be {last_drop}, the next will be at {next_drop}")


@bot.command()  # Lets the Players Enter the Game
async def entergame(ctx):
    if game.add_player(f"{ctx.author}"):
        await ctx.channel.send(f"Welcome to the game {ctx.author}")
        return
    await ctx.channel.send(f"You are already in the game")


@bot.command()  # Lets a user in the server back up the game data
async def backup(ctx):
    game.save_data()
    await ctx.channel.send("Successfully backed up the game")


@tasks.loop(seconds=3600)  # Gives each player a new roll
async def crateDrop():
    global next_drop
    global last_drop
    now = datetime.now()
    last_drop = now.strftime("%H:%M:%S")
    now = datetime.now() + timedelta(hours=1)
    next_drop = now.strftime("%H:%M:%S")
    print("Players Gettin Moolah")
    game.roll_drop()


@tasks.loop(seconds=60)  # Does an automatic back up
async def backup():
    print("Game Backed Up")
    game.save_data()


@tasks.loop(seconds=14400)  # Gives the player a zap
async def zapDrop():
    print("Players getting Zaps")
    game.zap_drop(1)


@bot.command()  # Zaps a target to lose a flag
async def zap(ctx, arg):
    if f"{ctx.author}" not in game.PLAYERS:
        await ctx.channel.send("You are not in the game, use $entergame to enter the game")
        return
    target, flag = game.zap(f"{ctx.author}", arg)

    if target == "MISSED":
        await ctx.channel.send("Invalid Target, make sure you use the correct #____")
        return

    if target == "FAILED":
        await ctx.channel.send("Failed, you dont currently have a zap")
        return

    if target == f"{ctx.author}":
        await ctx.channel.send(f"You zapped yourself! You lost {flag.name}")
    else:
        await ctx.channel.send(f"You zapped {arg}! They lost {flag.name}")

    await ctx.channel.send(file=discord.File(flag.image))


@bot.command()  # Lists the players in the console
async def playerlist(ctx):
    players = game.get_player_names()
    print("Players in game:")
    for player in players:
        print(player)


@bot.command()  # Prints the Tierlist for the flags in the chat
async def flaglist(ctx):
    await ctx.channel.send(file=discord.File('/home/pi/AlexanderTheBot/flags/FlagList.PNG'))


@bot.command()  # A player can use one of their roll tokens to get a flag
async def roll(ctx):
    if f"{ctx.author}" not in game.PLAYERS:
        await ctx.channel.send("You are not in the game, use $entergame to enter the game")
        return
    flag = game.open(f"{ctx.author}")
    if flag.name == "None":
        await ctx.channel.send("Sorry you don't have any rolls at the moment. Check back later")
        return
    await ctx.channel.send(f"{flag.rarity.upper()}: {flag.name}")
    await ctx.channel.send(file=discord.File(flag.image))


@bot.command()  # Lets the player view their balance
async def bal(ctx):
    if f"{ctx.author}" not in game.PLAYERS:
        await ctx.channel.send("You are not in the game, use $entergame to enter the game")
        return
    await ctx.channel.send(f"You have {game.get_bal(f'{ctx.author}')} rolls left")


@bot.command()
async def morerolls(ctx):
    if f"{ctx.author}" != "Roasted#3169":
        ctx.channel.send("Bruh")
        return
    game.roll_drop()
    await ctx.channel.send("Successfully gave everyone rolls")


@bot.command()
async def inventory(ctx):
    if not game.player_in_game(f"{ctx.author}"):
        await ctx.channel.send("Player not in game, try $entergame")
        return

    flags, amounts = game.PLAYERS[f"{ctx.author}"].inventory.print_current()

    embed = discord.Embed(title=f"{ctx.author}'s Inventory")
    embed.add_field(name="Current:", value=flags, inline=True)
    embed.add_field(name="Amount:", value=amounts, inline=True)
    embed.add_field(name="Missing:", value=game.PLAYERS[f"{ctx.author}"].inventory.print_missing(), inline=True)
    await ctx.channel.send(embed=embed)



@bot.command()
async def scoreboard(ctx):
    score_dict = game.get_scores()
    names = ""
    scores = ""
    for name, score in score_dict:
        names += f"{name}\n"
        scores += f"{score}\n"

    embed = discord.Embed(title="Scoreboard", color=0x87CEEB)
    embed.add_field(name="Players:", value=names, inline=True)
    embed.add_field(name="Scores:", value=scores, inline=True)
    await ctx.channel.send(embed=embed)

@bot.command()
async def verify(ctx):
    for player in players:
        player.inventory.check_score()
    await ctx.channel.send("The scoreboard has been updated")


@bot.command()
async def claim(ctx, arg):

    if f"{ctx.author}" not in game.PLAYERS:
        await ctx.channel.send("You are not in the game, use $entergame to enter the game")
        return

    if game.claim((f"{ctx.author}"), arg):
        await ctx.channel.send("Success you claimed your flags")
        return
    await ctx.channel.send("Bro you are Pohara wait till you have all of them")


@bot.command()
async def trade(ctx, target_player, player_flag, target_flag):
    if not game.player_in_game(target_player) or not game.player_in_game(f"{ctx.author}"):
        await ctx.channel.send("Invalid Players involved in trade")
        return

    if not game.has_flag(f"{ctx.author}", player_flag) or not game.has_flag(target_player, target_flag):
        await ctx.channel.send("Invalid trade, someone doesnt have a flag")
        return

    await ctx.channel.send(f"Waiting for {target_player} to confirm. To confirm use y/n")
    try:
        msg = await bot.wait_for('message', check=lambda message: f"{message.author}" == target_player, timeout=60)
        msg = msg.content.upper()
        if msg == "Y" or msg == "YES":
            game.add_flag(f"{ctx.author}", target_flag)
            game.remove_flag(f"{ctx.author}", player_flag)
            game.add_flag(target_player, player_flag)
            game.remove_flag(target_player, target_flag)
            await ctx.channel.send("Successful Trade")
        elif msg == "N" or msg == "YES":
            await ctx.channel.send("Sucks to be rejected my guy")
        else:
            await ctx.channel.send(f"{target_player} neither confirmed nor denied that statement")
    except:
        await ctx.channel.send("Y'all really out here making the lad wait")


@bot.command()
async def rollcount(ctx, amount):
    amount = int(amount)
    if f"{ctx.author}" != "Roasted#3169":
        await ctx.channel.send("Ahhh naughty naughty trying to cheat")
        return
    game.change_rolls(amount)
    await ctx.channel.send(f"Users will now get {amount} rolls per hour")


@bot.command()
async def rolllimit(ctx, amount):
    amount = int(amount)
    if f"{ctx.author}" != "Roasted#3169":
        await ctx.channel.send("Ahhh naughty naughty trying to cheat")
        return
    game.set_limit_rolls(amount)
    await ctx.channel.send(f"Users will now have a max of {amount} rolls in their inventory")



@bot.command()
async def removeflag(ctx, target, flag, amount=1):
    if f"{ctx.author}" != "Roasted#3169":
        await ctx.channel.send("Ahhhh naughty naughty trying to cheat")
        return
    if target not in game.PLAYERS:
        await ctx.channel.send("Target not found")
        return
    if not game.has_flag(target, flag):
        await ctx.channel.send("Flag not in invetory")
        return
    if amount > game.PLAYERS[target].inventory.current_inventory[flag]:
        await ctx.channel.send("Target does not have enough flags to do that")
        return
    game.remove_flag(target, flag, amount)
    await ctx.channel.send(f"Successfully removed {flag} from {target}")


@bot.command()
async def addflag(ctx, target, flag, amount=1):
    if f"{ctx.author}" != "Roasted#3169":
        await ctx.channel.send("Ahhhh naughty naughty trying to cheat")
        return
    if target not in game.PLAYERS:
        await ctx.channel.send("Target not found")
        return
    game.add_flag(target, flag, amount)
    if amount == 1:
        await ctx.channel.send(f"Successfully gave {target} {flag}")
        await ctx.channel.send(file=discord.File(game.FLAGS[flag].image))
    else:
        await ctx.channel.send(f"Successfully gave {target} {amount} {flag}'s")
        await ctx.channel.send(file=discord.File(game.FLAGS[flag].image))


def main():
    """Runs when bot starts"""
    game.initialise()
    crateDrop.start()
    backup.start()
    zapDrop.start()
    print("Bot Initialised")


if __name__ == "__main__":
    main()

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)
