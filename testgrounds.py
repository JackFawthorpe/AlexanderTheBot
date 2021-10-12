import player_module
import inventory_module
import flag_module

def main():
    crate = flag_module.load_crate("testflag.txt")
    inventory_module.inventory_init(crate)
    test_player =  player_module.Player("Test_Player")
    test_player.inventory.add_flag("Kazakhstan")
    print(test_player.inventory.getFlags())
    missing, missing_list = test_player.inventory.getMissing()
    print(missing)

if __name__ == "__main__":
    main()