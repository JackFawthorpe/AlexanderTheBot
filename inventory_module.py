import flag_module

# Global Variables
groups = []

crate = None

class Inventory:
    def __init__(self):
        self.current_inventory = []
        self.season_flags = []
        self.current_flag_count = 0
        self.score = 0
        self.group_claims = [0] * len(groups)

    def __repr__(self):
        output = ""
        for flag, amount in self.current_inventory:
            output += f"{flag}: {amount}\n"
        return output

    def add_flag(self, new_flag, value=1):
        """Adds a Flag to the players inventory"""

        global crate
        value = int(value)
        self.current_flag_count += value
        self.score += crate.flagValues[new_flag]

        if type(new_flag) == flag_module.Flag:
            new_flag = new_flag.name

        # Adds the flag to the season stats
        check = False
        for flag, amount in self.season_flags:
            if new_flag == flag:
                amount += value
                check = True
                break
        if not check:
            self.season_flags.append([new_flag, 1])

        # Adds the flag to current inventory
        for i in range(len(self.current_inventory)):
            if new_flag == self.current_inventory[i][0]:
                self.current_inventory[i][1] += value
                return
        self.current_inventory.append([new_flag, 1])

    def claim(self, group):
        check = 1
        index = -1
        for i in range(len(crate.groups)):
            if group == crate.groups[i].name:
                index = i
                break

        if index == -1:
            return False

        output, outputList = self.getMissing()
        if len(outputList[index]) != 0:
            return False

        for flag in groups[index].flags:
          self.remove_flag(flag.name)

        self.group_claims[index] += 1
        return True

    def remove_flag(self, old_flag):
        """Removes players flag from inventory"""

        self.current_flag_count -= 1

        for i in range(len(self.current_inventory)):
            if self.current_inventory[i][0] == old_flag:
                self.current_inventory[i][1] -= 1
                if self.current_inventory[i][1] == 0:
                    self.current_inventory.pop(i)
                return True
        return False

    def getFlags(self):
        output = "YOU HAVE:\n"
        for group in groups:
            output += f"{group.name}: \n"
            for flag in group.flags:
                for item in self.current_inventory:
                    if item[0] == flag.name:
                        output += f"     {item[0]}: {item[1]}\n"
        return output

    def getMissing(self):
        output = "MISSING:\n"
        output_list = []
        for group in groups:
            group_list = []
            output += f"{group.name}: "
            for flag in group.flags:
                has = False
                for inv in self.current_inventory:
                    if inv[0] == flag.name:
                        has = True
                        break
                if not has:
                    group_list.append(flag.name)
                    output += f" {flag.name}"
            output += "\n"
            output_list.append(group_list)
        return output, output_list

    def getScore(self):
        return self.score

    def checkScore(self):
        self.score = 0
        for flag in self.current_inventory:
            self.score += crate.flagValues[flag[0]] * flag[1]

        for i in range(len(groups)):
            self.score += groups[i].score * self.group_claims[i]

def inventory_init(input):
    global crate
    crate = input
    global groups
    for group in input.groups:
        groups.append(group)

if __name__ == "__main__":
    test = Inventory()
    crate = flag_module.load_crate("testflag.txt")
    inventory_init(crate)
    test.add_flag("Kazakhstan")
    test.add_flag("Kazakhstan")
    output = test.getFlags()
    print(output)
