import random

import flag_module
import game
import player_module
import inventory_module
import game_stats

PLAYER_DATA = "player_data.txt"
FLAG_DATA = "flag_data.txt"
PLAYERS = {}
CRATE = None
FLAGS = {}
GROUPS = {}
ROLLS_PER_DROP = 3

values_t = {
    "LEGENDARY": 60,
    "EPIC": 20,
    "RARE": 10,
    "UNCOMMON": 5,
    "COMMON": 2,
}

# Typedefs for Rarities
rarities_t = {
    "LEGENDARY": 0,
    "EPIC": 1,
    "RARE": 2,
    "UNCOMMON": 3,
    "COMMON": 4,
}


def crate_init():
    """Initialises the crate"""
    global CRATE
    CRATE = flag_module.load_game_data(FLAG_DATA)
    print(type(CRATE))

def flag_init():
    """Initialises the flags"""
    flag_list = flag_module.load_flags(FLAG_DATA)
    for flag in flag_list:
        FLAGS[flag.name] = flag
        if flag.group in GROUPS:
            GROUPS[flag.group].append(flag)
        else:
            GROUPS[flag.group] = [flag]


def player_init():
    """Initialises the players"""
    global PLAYERS
    player_list = player_module.load_players(PLAYER_DATA)
    for player in player_list:
        PLAYERS[player.name] = player

def stats_init():
    """Initialises the stats module"""
    game_stats.stats_init(FLAGS)

def initialise():
    """Initialises the game"""
    crate_init()
    flag_init()
    inventory_module.push_data(FLAGS, GROUPS, CRATE)
    stats_init()
    player_init()
    for name, player in PLAYERS.items():
        player.inventory.check_score()
    print(type(CRATE))


def get_random_flag(player_name):
    """Returns a random flag (String) from the players inventory"""
    flag_index = random.randint(1, PLAYERS[player_name].inventory.flag_count)
    for flag, amount in PLAYERS[player_name].inventory.current_inventory.items():
        flag_index -= amount
        if flag_index <= 0:
            return flag


def get_scores():
    """Returns a sorted list of a tuple of players and scores"""
    players = sorted(PLAYERS.items(), key=lambda item: item[1].inventory.score, reverse=True)
    output = []
    for name, player in players:
        output.append((player.name, player.inventory.score))
    return output


def print_scores():
    """Returns a Leaderboard string"""
    players = get_scores()
    output = ""
    counter = 1
    for player in players:
        output += f"{counter:>2}: {player[0]:<25} {player[1]}\n"
        counter += 1
    if len(PLAYERS) == 0:
        return "Jack Really fucked up"
    return output


def get_player_names():
    """Returns a list of player names"""
    output = []
    for name in PLAYERS:
        output.append(name)
    return output


def print_player(playerName):
    """"Returns a string for a player"""
    return f"{PLAYERS[playerName].name}"


def give_rolls(playerName, amount=3):
    """Gives the player 3 rolls"""
    PLAYERS[playerName].bal = amount


def give_zap(player_name, amount=1):
    """Gives a player a zap"""
    if PLAYERS[player_name].zap != 1:
        PLAYERS[player_name].zap = 1


def change_rolls(roll_count):
    global ROLLS_PER_DROP
    ROLLS_PER_DROP = roll_count


def roll_drop(amount=3):
    """Gives every player 3 rolls"""
    for name, player in PLAYERS.items():
        player.bal += amount
        player.bal = min(player.bal, ROLLS_PER_DROP)


def zap_drop(amount=1):
    """Gives every player 1 zap"""
    for name, player in PLAYERS.items():
        player.zap = amount


def add_flag(playerName, flag, amount=1):
    """Adds a flag to the player"""
    PLAYERS[playerName].add_flag(flag, amount)
    print(f"Added {flag} to {playerName}, the player now has a score of {PLAYERS[playerName].inventory.score}")


def remove_flag(player_name, flag, amount=1):
    """Removes a flag from the player"""
    PLAYERS[player_name].inventory.remove_flag(flag, amount)
    print(f"Removed {flag} from {player_name}, the player now has a score of {PLAYERS[player_name].inventory.score}")


def open(playerName):
    """Rolls a flag and returns a none Flag"""
    if get_bal(playerName) <= 0:
        return flag_module.Flag("None", "None", "None")
    flag = CRATE.open()
    PLAYERS[playerName].bal -= 1
    add_flag(playerName, flag.name, 1)
    game_stats.add_to_rolls(flag.name)
    return flag


def get_player_flag_count(playerName):
    """"Gets the amount of flags a player has"""
    return PLAYERS[playerName].inventory.flag_count


def player_in_game(inputName):
    """Returns a bool for if the player is in the game"""
    for player in PLAYERS:
        if player == inputName:
            return True
    return False


def get_bal(input_name):
    """Gets the balance of a player"""
    return PLAYERS[input_name].getBal()


def add_player(input_name):
    """Adds a player to the game, returns false if the player is already in the game"""
    if input_name in PLAYERS:
        return False
    PLAYERS[input_name] = player_module.Player(input_name)
    return True


def claim(player_name, group):
    """"Lets a player claim points for a group and returns true if successful"""

    if not player_in_game(player_name):
        return False

    if not PLAYERS[player_name].inventory.claim(group):
        return False

    return True


def print_player_inventory(playerName):
    """Returns an output string """
    output = f"Inventory for {playerName}\n"
    output += f"Number of flags: {get_player_flag_count(playerName)}\n"
    output += PLAYERS[playerName].inventory.print_flags()
    output += PLAYERS[playerName].inventory.print_missing()
    return output


def save_data():
    """Backs up the player data"""
    player_module.backup(PLAYERS, "player_data.txt")
    game_stats.save_stats()


def has_flag(player_name, flag):
    """"Bool for if player has the flag"""
    for current in PLAYERS[player_name].inventory.current_inventory:
        if current == flag:
            return True
    return False


def get_groups():
    """Returns a list of the groups in the game"""
    output = []
    for group in GROUPS:
        output.append(group)
    return output


def get_flags_in_group(group):
    """Returns a list of flags within the group"""
    return GROUPS[group]


def zap(player_name, target_name):
    """Deletes a random flag from a random player, returns whether or not it was a success"""

    if target_name not in PLAYERS:
        return "MISSED", flag_module.Flag("NONE", "NONE", "NONE")

    if PLAYERS[player_name].zap <= 0:
        return "FAILED", flag_module.Flag("NONE", "NONE", "NONE")

    PLAYERS[player_name].zap -= 1

    if random.randint(1, 5) == 1:
        flag = get_random_flag(player_name)
        remove_flag(player_name, flag)
        return player_name, FLAGS[flag]

    flag = get_random_flag(target_name)
    remove_flag(target_name, flag)
    return target_name, FLAGS[flag]




def main():
    """Used for testing"""

if __name__ == "__main__":
    main()