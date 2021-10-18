import flag_module
import game
import game_stats
# Global Variables
FLAGS = {}
GROUPS = {}

GROUP_INDEX = {

}

class Inventory:
    def __init__(self):
        self.current_inventory = {}
        self.flag_count = 0
        self.score = 0
        self.group_claims = [0] * len(GROUPS)

    def __repr__(self):
        output = ""
        for flag, amount in self.current_inventory:
            output += f"{flag}: {amount}\n"
        return output

    def add_flag(self, new_flag, value=1):
        """Adds a Flag to the players inventory"""
        if new_flag not in self.current_inventory:
            self.current_inventory[new_flag] = value
        else:
            self.current_inventory[new_flag] += value
        self.flag_count += value
        self.score += game.values_t[FLAGS[new_flag].rarity.upper()] * value
        game_stats.add_to_current(new_flag)

    def claim(self, group):

        if group not in GROUPS:
            return False

        for flag in GROUPS[group]:
            if flag.name not in self.current_inventory:
                return False

        for flag in GROUPS[group]:
            self.remove_flag(flag.name, 1)

        for i in range(len(CRATE.groups)):
            if CRATE.groups[i].name == group:
                print(CRATE.groups[i].score)
                self.score += CRATE.groups[i].score
                self.group_claims[i] += 1
                break
        return True

    def remove_flag(self, old_flag, amount=1):
        """Removes players flag from inventory"""
        if old_flag in self.current_inventory:
            if self.current_inventory[old_flag] < amount:
                return False
            self.current_inventory[old_flag] -= amount
            if self.current_inventory[old_flag] == 0:
                self.current_inventory.pop(old_flag)
            self.flag_count -= amount
            self.score -= game.values_t[FLAGS[old_flag].rarity.upper()]
            return True
        return False

    def get_missing(self):
        output = []
        for group in GROUPS:
            group_list = []
            for flag in group:
                if flag not in self.current_inventory:
                    group_list.append(flag)
            output.append(group_list)
        return output

    def print_missing(self):
        missing_list = self.get_missing()
        output = ""
        for group, flags in GROUPS.items():
            output += f"{group}:\n"
            for flag in flags:
                if flag.name not in self.current_inventory:
                    output += f"{flag.name}\n"
            output += "\n"
        return output

    def print_current(self):
        amounts = ""
        output = ""
        for group, flags in GROUPS.items():
            output += "\n\n"
            amounts += "\n\n"
            for flag in flags:
                if flag.name in self.current_inventory:
                    output += f"{flag.name}\n"
                    amounts += f"{self.current_inventory[flag.name]}\n"
        return output, amounts


    def get_score(self):
        return self.score

    def check_score(self):
        self.score = 0
        for flag, amount in self.current_inventory.items():
            self.score += game.values_t[FLAGS[flag].rarity.upper()] * amount
        for i in range(len(CRATE.groups)):
            self.score += self.group_claims[i] * CRATE.groups[i].score


def push_data(flags, groups, crate):
    """Gets the main flag data and stores"""
    global FLAGS
    global GROUPS
    global CRATE
    FLAGS = flags
    GROUPS = groups
    CRATE = crate

if __name__ == "__main__":
    game.initialise()
    test = Inventory()
    crate = flag_module.load_game_data("testflag.txt")
    test.add_flag("Kazakhstan")
    test.add_flag("Kazakhstan")
    test.remove_flag("Kazakhstan")
    print(test.print_missing())
