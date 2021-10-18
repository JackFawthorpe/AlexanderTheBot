# Imports
import random

# Defines
TOTAL_PROBABILITY = 750
RARITIES = [5, 25, 100, 350, TOTAL_PROBABILITY] # Cumulative Probability

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


class Crate:
    def __init__(self):
        self.flag_count = 0
        self.CommonCount = 0
        self.opens = 0
        self.groups = []
        self.rarity_counts = [0, 0, 0, 0, 0]
        self.flags = [[], [], [], [], []]
        self.flagValues = {}

    def get_flag_group(self, rarity):
        return self.flags[rarities_t[rarity.upper()]]

    def get_rarity_count(self, rarity):
        return self.rarity_counts[rarities_t[rarity.upper()]]

    def add_flag(self, flag):
        """Adds a flag to the Crate"""
        index = -1
        for i in range(len(self.groups)):
            if self.groups[i].name == flag.group:
                index = i
                break

        if index == -1:
            self.groups.append(ItemGroup(flag.group))
            self.groups[len(self.groups)-1].add_flag(flag)
            self.groups = sorted(self.groups)
        else:
            self.groups[index].add_flag(flag)

        index = rarities_t[flag.rarity.upper()]
        self.rarity_counts[index] += 1
        self.flag_count += 1
        self.flags[index].append(flag)
        self.flags[index] = sorted(self.flags[index])

        self.flagValues[flag.name] = values_t[flag.rarity.upper()]

    def open(self):
        """Opens A Crate and returns the Flag Received"""
        x = random.randint(1, TOTAL_PROBABILITY)
        if x <= RARITIES[0]:
            return self.get_flag_group("Legendary")[random.randint(1, self.get_rarity_count("Legendary")) - 1]
        if x <= RARITIES[1]:
            return self.get_flag_group("Epic")[random.randint(1, self.get_rarity_count("Epic")) - 1]
        if x <= RARITIES[2]:
            return self.get_flag_group("Rare")[random.randint(1, self.get_rarity_count("Rare")) - 1]
        if x <= RARITIES[3]:
            return self.get_flag_group("Uncommon")[random.randint(1, self.get_rarity_count("Uncommon")) - 1]
        return self.get_flag_group("Common")[random.randint(1, self.get_rarity_count("Common")) - 1]


class Flag:
    def __init__(self, name, rarity, group):
        self.name = name
        self.image = f"flags/{name}.png"
        self.rarity = rarity
        self.group = group

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self,other):
        return self.name != other.name

    def __ge__(self,other):
        return self.name >= other.name

    def __le__(self, other):
        return self.name <= other.name

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name


class ItemGroup:
    def __init__(self, name):
        self.item_count = 0
        self.flags = []
        self.name = name
        self.score = 0

    def __repr__(self):
        output = f"{self.name}:\n"
        for flag in self.flags:
            output += f"{flag.name}\n"
        return output

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __ge__(self, other):
        return self.name >= other.name

    def __le__(self, other):
        return self.name <= other.name

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name

    def add_flag(self, new_item):
        self.item_count += 1
        self.flags.append(new_item)
        self.flags = sorted(self.flags)
        return


def load_game_data(filename):
    crate = Crate()
    data = open(filename)
    flags = data.readlines()
    for flag_string in flags:
        flag_string = flag_string.split(",")
        crate.add_flag(Flag(flag_string[0], flag_string[1], flag_string[2]))
    group_score_set("group_data.txt", crate)
    return crate


def load_flags(filename):
    """Returns a list of flags"""
    flags = []
    data = open(filename)
    lines = data.readlines()
    for flag_string in lines:
        flag_string = flag_string.split(',')
        flags.append(Flag(flag_string[0], flag_string[1], flag_string[2]))
    return flags


def group_score_set(filename, crate):
    data = open(filename)
    lines = data.readlines()
    for line in lines:
        title, score = line.split(',')
        for group in crate.groups:
            if group.name == title:
                group.score = int(score)
                break


if __name__ == "__main__":
    crate = load_game_data("testflag.txt")
    group_score_set("group_data.txt", crate)
