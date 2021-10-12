import inventory_module

class Player:
    """The Class for each player"""

    def __init__(self, name):
        self.name = name
        self.bal = 3
        self.inventory = inventory_module.Inventory()

    def __repr__(self):
        return f"{self.name}"

    def getBal(self):
        return self.bal

    def getInventory(self):
        return self.inventory


    def setBal(self, bal):
        self.bal = bal



def load_players():
    """Loads the players from the save file"""
    players = []
    data = open("player_data.txt", "r")
    lines = data.readlines()
    if len(lines) != 0:
        player_count = int(lines[0])
        current_line = 0
        for player in range(player_count):
            current_line += 1
            name = lines[current_line][0:-1]
            current_player = Player(name)
            current_line += 1
            current_player.setBal(int(lines[current_line]))
            current_line += 1
            current_score = int(current_line)
            current_line += 1

            player_inventory = lines[current_line]
            if len(player_inventory) != len("{}\n"):
                player_inventory = player_inventory[1:-3]
                player_inventory = player_inventory.split(",")
                for item in player_inventory:
                    item = item.split(":")
                    item_id = item[0]
                    amount = item[1]
                    print(current_player.name, item_id, amount)
                    for i in range(int(amount)):
                        current_player.inventory.add_flag(item_id)
            current_player.inventory.score = current_score
            current_line += 1
            player_claims = lines[current_line]
            player_claims = player_claims[1:-3]
            player_claims = player_claims.split(',')
            for i in range(len(player_claims)):
                current_player.inventory.group_claims[i] = int(player_claims[i])


            print(current_player.name, current_player.inventory.getFlags())
            players.append(current_player)
    data.close()
    return players

def backup(players):
    """Saves the Player Date to the save file"""
    file = open("player_data.txt", "w")
    file.truncate(0)
    file.write(f"{len(players)}\n")
    for player in players:
        file.write(f"{player.name}\n{player.bal}\n{player.inventory.score}\n")
        file.write("{")
        for item in player.inventory.current_inventory:
            file.write(f"{item[0]}:{item[1]},")
        file.write("}\n")
        file.write("{")
        for score in player.inventory.group_claims:
            file.write(f"{score},")
        file.write("}\n")
    file.close()
    return

if __name__ == "__main__":
    testPlayer = Player("Bob")
    players = load_players()
    for player in players:
        print(player.name)
        print(player.inventory)