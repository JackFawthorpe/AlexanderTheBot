import game

FLAG_ROLLS = {}
CURRENT_FLAGS = {}


def add_to_rolls(flag):
    """Adds a flag to the roll data"""
    if flag not in FLAG_ROLLS:
        FLAG_ROLLS[flag] = 1
    else:
        FLAG_ROLLS[flag] += 1


def add_to_current(flag):
    """Keeps track of the flags in circulation"""
    CURRENT_FLAGS[flag] += 1


def remove_from_current(flag):
    """Removes a flag from circulation"""
    CURRENT_FLAGS[flag] -= 1
    if CURRENT_FLAGS[flag] == 0:
        CURRENT_FLAGS.pop(flag)


def save_stats():
    """Saves the statistics into a file"""
    file = open("/home/pi/AlexanderTheBot/stats.txt", "w")
    file.write("# Roll Data\n")
    for flag, amount in FLAG_ROLLS.items():
        file.write(f"{flag},{amount}\n")
    file.write("\n\n# Circulation Stats\n")
    for flag, amount in CURRENT_FLAGS.items():
        file.write(f"{flag},{amount}\n")
    file.close()


def stats_init(flags):
    """Adds all the flags to circulation with 0"""
    for name in flags:
        CURRENT_FLAGS[name] = 0
        FLAG_ROLLS[name] = 0
    file = open("/home/pi/AlexanderTheBot/stats.txt")
    lines = file.readlines()
    index = 1
    while lines[index][0] != "#":
        index += 1
    index += 1
    for i in range(index, len(lines)):
        flag, amount = lines[i].split(',')
        FLAG_ROLLS[flag] = int(amount)
    file.close()
