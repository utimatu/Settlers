import random
import copy
board = ["", "","","","","","","","","","","","","","","","","",""]
def main(players):
    string = '\n'
    print(string)
    game_end = 0
    player_turn_index = 0
    starting_dicts = get_dicts()
    buildings_dict = starting_dicts[0]
    roads_dict = starting_dicts[1]
    buildings_to_roads_dict = starting_dicts[2]
    roads_to_roads_dict = starting_dicts[3]
    tiles_to_buildings_dict = starting_dicts[4]
    buildings = []
    roads = []
    board = gen_map_init()
    desert = board[-1]
    rolls = []
    incomes = []
    thief = desert
    del board[-1]
    numbers = gen_numbers_init(desert)
    map_display = display_map(board, numbers, buildings, buildings_dict, roads, roads_dict,  thief)
    inventories = []
    cards =[]
    for x in players:
        inventories.append([x, 0, 0, 0, 0, 0])
    random.shuffle(players)
    for x in list(range(len(players))):
        place_first_town(players[x], buildings, roads, map_display, buildings_to_roads_dict, board, tiles_to_buildings_dict, inventories)
        display_map(board, numbers, buildings, buildings_dict, roads, roads_dict,  thief)
    for x in list(range(len(players))):
        place_first_town(players[(x-(len(players)-1))*(-1)], buildings, roads, map_display, buildings_to_roads_dict, board, tiles_to_buildings_dict, inventories)
        display_map(board, numbers, buildings, buildings_dict, roads, roads_dict,  thief)
    while game_end == 0:
        roll = dice_roll()
        rolls.append(roll)
        string = str("The number that was rolled on " + str(players[player_turn_index]) +"'s turn was " + str(int(roll)))
        print(string)
        if roll != 7:
            backup_inventories = copy.deepcopy(inventories)
            inventories = get_resources_gathered(roll, tiles_to_buildings_dict, buildings, board, numbers, inventories)
            turn_profit = []
            profit = []
            for x in list(range(len(players))):
                profit.append(inventories[x][0])
                for y in [1, 2, 3, 4, 5]:
                    profit.append(inventories[x][y]-backup_inventories[x][y])
                turn_profit.append(profit)
                profit = []
            incomes.append(turn_profit)
        if roll == 7:
            construction_variable = thief_turn(players,  player_turn_index,  thief,  inventories,  buildings,  tiles_to_buildings_dict)
            inventories = construction_variable[0]
            thief = construction_variable[1]
        display_map(board, numbers, buildings, buildings_dict, roads, roads_dict,  thief)
        for x in inventories:
            string = str("Player:" + str(x[0]) + "now has:" + '\t' + "Sheep:" + str(x[1]) + '\t' + "Wood:" + str(x[2]) + '\t' + "Grain:" + str(x[3]) + '\t' + "Bricks:" + str(x[4]) + '\t' + "Ore:" + str(x[5]))
            print(string)
        construction_variable = ask_for_instructions(player_turn_index, players, buildings, roads, buildings_dict, roads_dict, buildings_to_roads_dict, roads_to_roads_dict, tiles_to_buildings_dict, rolls,
                                                     incomes, inventories, board, numbers, cards,  thief)
        buildings = construction_variable[0]
        roads = construction_variable[1]
        inventories = construction_variable[2]
        cards = construction_variable[3]
        thief = construction_variable[4]
        player_turn_index += 1
        if player_turn_index == len(players):
            player_turn_index = 0


        
def ask_for_instructions(player_turn_index, players, buildings, roads, buildings_dict, roads_dict, buildings_to_roads_dict, roads_to_roads_dict, tiles_to_buildings_dict, rolls, incomes, inventories, board, numbers, cards,  thief):
    end_function = 0
    string = str("It is now player " + players[player_turn_index] + "'s turn." + '\n')
    print(string)
    while end_function == 0:
        string = str("What would you like to do, " + str(players[player_turn_index]) + '\n')
        print(string)
        print("Press H to see a list of functions")
        print("")
        request = raw_input("-->")
        request.upper()
        if request == "R":
            data_request(rolls, incomes, inventories, buildings, board, numbers, tiles_to_buildings_dict)
        if request == "B":
            after_build = function_build(buildings, roads, cards, buildings_to_roads_dict, roads_to_roads_dict, inventories, players, player_turn_index)
            buildings = after_build[0]
            roads = after_build[1]
            cards = after_build[2]
        if request == "T":
            destination_player = "None"
            while destination_player == "None":
                destination_player = raw_input("Who would you like to trade with?")
                is_real = 0
                if destination_player != "X":
                    for x in players:
                        if destination_player == x:
                            is_real = 1
                    if is_real == 0:
                        print("Sorry, that is not a real player")
                        destination_player = "None"
                    if is_real == 1:
                        if destination_player == players[player_turn_index]:
                            is_real = 0
                            print("You can't trade with yourself")
                    if is_real == 1:
                        index = 0
                        for player in players:
                            if player[0] == destination_player:
                                final_index = index
                            index += 1
                        inventories = initiate_trade(players, player_turn_index, final_index, inventories)
        if request == "U":
            returned_variable = use_cards(buildings, roads, roads_to_roads_dict, tiles_to_buildings_dict, inventories, cards, players, player_turn_index)

        if request == "H":
            print("[R]equest data")
            print("[B]uild or [B]uy something")
            print("[T]rade with someone")
            print("[U]se a card")
            print("[H]elp")
            print("[E]nd turn")
        if request == "E":
            end_function = 1
    construction_variable = [buildings, roads, inventories, cards,  thief]
    return construction_variable
                    

def thief_turn(players,  player_turn_index,  thief,  inventories,  buildings,  tiles_to_buildings_dict):
    print("Under construction... program will commense to poop out!")
    print("You get to move the thief!  What row would you like to move it to?")
    valid = 0
    while valid == 0:
        row = raw_input("-->")
        print("What column would you like to move it to?")
        column = raw_input("-->")
        row = int(row)
        column = int(column)
        location = find_desired_location_tile(row,  column)
        if location != thief:
            if location != -1:
                valid = 1
        if valid == 0:
            print("Sorry, that location is invalid, please try again.")
    potential_inventories = []
    for locations in tiles_to_buildings_dict[location]:
        for building in buildings:
            if locations == building[0]:
                potential_inventories.append(building[1])
    if len(potential_inventories) == 0:
        returned_variable = [inventories,  theif]
        return returned_variable
    print("Who's inventory would you like to steal from?")
    valid = 0
    while valid == 0:
        player = raw_input("-->")
        player.upper()
        if player in potential_inventories:
            valid = 1
        if valid == 0:
            string = str("Sorry, you can't steal from that player.  Please try again." + '\n')
            print(string)
    index = 0
    final_index = 0
    for inventory in inventories:
        if inventory[0] == player:
            final_index = index
        index += 1
    total_size = inventories[final_index][1]+inventories[final_index][2]+inventories[final_index][3]+inventories[final_index][4]+inventories[final_index][5]
    location = int(random.random()*total_size)
    location -= inventories[final_index][1]
    resource_stolen = 0
    if location < 0:
        resource_stolen = 1
        location += 100
    location -= inventories[final_index][2]
    if location < 0:
        resource_stolen = 2
        location += 100
    location -= inventories[final_index][3]
    if location < 0:
        resource_stolen = 3
        location += 100
    location -= inventories[final_index][4]
    if location < 0:
        resource_stolen = 4
        location += 100
    location -= inventories[final_index][5]
    if location < 0:
        resource_stolen = 5
    inventories[final_index][resource_stolen] -= 1
    inventories[player_turn_index][resource_stolen] += 1
    returned_variable = [inventories,  thief]
    if resource_stolen == 1:
        string_stolen = "Wood"
    if resource_stolen == 2:
        string_stolen = "Brick"
    if resource_stolen == 3:
        string_stolen = "Sheep"
    if resource_stolen == 4:
        string_stolen = "Grain"
    if resource_stolen == 5:
        string_stolen = "Ore"
    string = str(players[player_turn_index]  + " steals " + string_stolen + " from " + player)
    print(string)
    return returned_variable

def data_request(rolls, incomes, inventories, buildings, roads, roads_to_roads_dict):
    print("Under construction. Come back later!")
    return

def find_desired_location_tile(row,  column):
    location = -1
    if row == 1:
        if column == 1:
            location = 0
        if column == 2:
            location = 1
        if column == 3:
            location = 2
    if row == 2:
        if column == 1:
            location = 3
        if column == 2:
            location = 4
        if column == 3:
            location = 5
        if column == 4:
            location = 6
    if row == 3:
        if column == 1:
            location = 7
        if column == 2:
            location = 8
        if column == 3:
            location = 9
        if column == 4:
            location = 10
        if column == 5:
            location = 11
    if row == 4:
        if column == 1:
            location = 12
        if column == 2:
            location = 13
        if column == 3:
            location = 14
        if column == 4:
            location = 15
    if row == 5:
        if column == 1:
            location = 16
        if column == 2:
            location = 17
        if column == 3:
            location = 18
    return location

def function_build(buildings, roads, cards, buildings_to_roads_dict, roads_to_roads_dict, inventories, players, player_turn_index):
    print("Under construction. Come back later!")
    string = str("What would you like to build/buy? [S]ettlement/ci[T]y/[R]oad/[C]ard/[E]xit" + '\n' + "-->")
    request = raw_input(string)
    if request == "S":
        string = str('\n' + "What row would you like to put the settlement in?" + '\n' + "-->")
        row = int(raw_input(string))
        string = str('\n' + "What column would you like to put the settlement in?" + '\n' + "-->")
        column = int(raw_input(string))
        string = str('\n' + "What direction would you like to put the settlement in?" + '\n' + "-->")
        direction = int(raw_input(string))
        location = find_desired_location_building(row, column, direction)
        valid = test_if_building_is_in_range(location, buildings, buildings_to_roads_dict)
        if valid == 1:
            valid = test_if_building_is_connected(location, roads, roads_to_roads_dict, buildings_to_roads_dict, players, player_turn_index)
        if valid != 1:
            location = -1
        if location == -1:
            print("Sorry, that is in invalid location")
        if valid == 1:
            test_inventory = inventory_request_test(players, player_turn_index, inventories, 'S')
        if test_inventory == 1:
            inventories = inventory_withdraw(players, player_turn_index, inventories, 'S')
            buildings.append([location, players[player_turn_index], 'S'])
    if request == "T":
        string = str('\n' + "What row would you like to put the city in?" + '\n' + "-->")
        row = input(string)
        string = str('\n' + "What column would you like to put the city in?" + '\n' + "-->")
        column = input(string)
        string = str('\n' + "What direction would you like to put the city in?" + '\n' + "-->")
        direction = input(string)
        location = find_desired_location_building(row, column, direction)
        valid = test_city_construction(players, player_turn_index, location, buildings)
        if valid == 1:
            test_inventory = inventory_request_test(players, player_turn_index, inventories, 'T')
        else:
            print("You can't build a city there")
        if test_inventory == 1:
            building_counter = 0
            for building in buildings:
                if building[0] == location:
                    final_count = building_counter
                else:
                    building_counter += 1
            del buildings[final_count]
            inventories = inventory_withdraw(players, player_turn_index, inventories, 'T')
            buildings.append[location, players[player_turn_index], "C"]
        else:
            print("You don't have enough resources to build a city")
    if request == "R":
        string = str('\n' + "What row would you like to put the road in?" + '\n' + "-->")
        row = input(string)
        string = str('\n' + "What column would you like to put the road in?" + '\n' + "-->")
        column = input(string)
        string = str('\n' + "What direction would you like to put the road in?" + '\n' + "-->")
        direction = input(string)
        location = find_desired_location_road(row, column, direction)
        valid = test_road_construction(players, player_turn_index, location, roads, buildings, roads_to_roads_dict, buildings_to_roads_dict)
        if valid == 1:
            test_inventory = inventory_request_test(players, player_turn_index, inventories, 'R')
        else:
            print("You can't build a road there")
        if test_inventory == 1:
            inventories = inventory_withdraw(players, player_turn_index, inventories, 'R')
            roads.append([location, players[player_turn_index], 'R'])
        else:
            print("You don't have enought resources to build that")
    if request == "C":
        test_inventory = inventory_request_test(players, player_turn_index, inventories, 'C')
        if test_inventory == 1:
            cards = put_card_into_inventory(players, player_turn_index, cards)
            inventories = inventory_withdraw(players, player_turn_index, inventories, 'C')
        else:
            print("You don't have enought resources to buy a card")
    if request == "E":
        return
    return

def test_city_construction(players, player_turn_index, location, buildings):
    valid = 0
    for building in buildings:
        if building[0] == location:
            if building[1] == players[player_turn_index]:
                if building[2] == "S":
                    valid = 1
    return valid

def put_card_into_inventory(players, player_turn_index, cards):
    
    return cards

def test_road_construction(players, player_turn_index, location, roads, buildings, roads_to_roads_dict, buildings_to_roads_dict):
    valid = 0
    for road in roads:
        if road[0] == location:
            string = str("There is already a road there." + '\n')
            print(string)
            return 0
        if road[1] == players[player_turn_index]:
            if location in roads_to_roads_dict[road[0]]:
                valid += 1
                for building in buildings:
                    if building[1] != players[player_turn_index]:
                        for building_to_road in buildings_to_roads_dict[building[0]]:
                            if road[0] == building_to_road:
                                if location in buildings_to_roads_dict[building]:
                                    valid -= 1
    if valid >= 1:
        valid = 1
    return valid

def inventory_withdraw(players, player_turn_index, inventories, build_type):
    for inventory in inventories:
        if inventory[0] == players[player_turn_index]:
            if build_type == "S":
                inventory[1] -= 1
                inventory[2] -= 1
                inventory[3] -= 1
                inventory[4] -= 1
            if build_type == "T":
                inventory[3] -= 2
                inventory[5] -= 3
            if build_type == "R":
                inventory[2] -= 1
                inventory[4] -= 1
            if build_type == "C":
                inventory[1] -= 1
                inventory[3] -= 1
                inventory[5] -= 1
    return inventories

def inventory_request_test(players, player_turn_index, inventories, build_type):
    for x in inventories:
        if x[0] == players[player_turn_index]:
            inventory = [x[1], x[2], x[3], x[4], x[5]]
    if build_type == 'S':
        valid = -1
        if inventory[0] >= 1:
            if inventory[1] >= 1:
                if inventory[2] >= 1:
                    if inventory[3] >= 1:
                        valid = 1
    if build_type == 'T':
        valid = -1
        if inventory[2] >= 2:
            if inventory[4] >= 4:
                valid = 1
    if build_type == 'R':
        valid = -1
        if inventory[1] >= 1:
            if inventory[3] >= 1:
                valid = 1
    if build_type == 'C':
        valid = -1
        if inventory[0] >= 1:
            if inventory[2] >= 1:
                if inventory[4] >= 1:
                    valid = 1
    return valid

def test_if_building_is_connected(location, roads, roads_to_roads_dct, buildings_to_roads_dict, players, player_turn_index):
    player_owned_roads = []
    for road in roads:
        if road[1] == players[player_turn_index]:
            player_owned_roads.append(road[0])
    road_options = []
    for x in buildings_to_roads_dict[location]:
        road_options.append(x)
    valid = -1
    for x in player_owned_roads:
        for y in road_options:
            if x == y:
                valid = 1
    return valid
    

def initiate_trade(players, player_turn_index, destination_player_index, inventories):
    end = 0
    offer = [0,  0,  0,  0,  0]
    request = [0,  0,  0,  0,  0]
    string = str(players[player_turn_index] + ", what would you like to offer?" + '\n' + "[W]ood/[B]rick/[S]heep/[G]rain/[O]re/[D]one/[E]xit" + '\n')
    print(string)
    while end == 0:
        if offer != [0,  0,  0,  0,  0]:
            string = str("Your offer now consists of " + str(offer[0]) + " sheep, " + str(offer[1]) + " wood, " + str(offer[2]) + " grain, " + str(offer[3]) + " brick, " + str(offer[4]) + " ore.")
            print(string)
        value = raw_input("-->")
        value.upper()
        if value == "S":
            if offer[0] < inventories[player_turn_index][1]:
                offer[0] += 1
            else:
                print("You don't have enough sheep.  Wanna try trading something else?")
        if value == "W":
            if offer[1] < inventories[player_turn_index][2]:
                offer[1] += 1
            else:
                print("You don't have enough wood.  Wanna try trading something else?")
        if value == "G":
            if offer[2] < inventories[player_turn_index][3]:
                offer[2] += 1
            else:
                print("You don't have enough grain.  Wanna try trading something else?")
        if value == "B":
            if offer[3] < inventories[player_turn_index][4]:
                offer[3] += 1
            else:
                print("You don't have enough brick.  Wanna try trading something else?")
        if value == "O":
            if offer[4] < inventories[player_turn_index][5]:
                offer[4] += 1
            else:
                print("You don't have enough ore.  Wanna try trading something else?")
        if value == "D":
            end = 1
        if value == "E":
            return inventories
        if value not in ["W",  "B",  "S",  "G",  "O",  "D",  "E"]:
            print("I don't think that letter means what you think it means.")
    end = 0
    string = str(players[player_turn_index] + ", what would you like to request?" + '\n' + "[W]ood/[B]rick/[S]heep/[G]rain/[O]re/[D]one/[E]xit" + '\n')
    print(string)
    while end == 0:
        if request != [0,  0,  0,  0,  0]:
            string = str("Your request now consists of " + str(request[0]) + " sheep, " + str(request[1]) + " wood, " + str(request[2]) + " grain, " + str(request[3]) + " brick, " + str(request[4]) + " ore.")
            print(string)
        value = raw_input("-->")
        value.upper()
        if value == "S":
            request[0] += 1
        if value == "W":
            request[1] += 1
        if value == "G":
            request[2] += 1
        if value == "B":
            request[3] += 1
        if value == "O":
            request[4] += 1
        if value == "D":
            end = 1
        if value == "E":
            return inventories
        if value not in ["W",  "B",  "S",  "G",  "O",  "D",  "E"]:
            print("I don't think that letter means what you think it means.")
    string = str("Your offer consists of " + str(offer[0]) + " sheep, " + str(offer[1]) + " wood, " + str(offer[2]) + " grain, " + str(offer[3]) + " brick, " + str(offer[4]) + " ore.")
    print(string)
    string = str("Your request consists of " + str(request[0]) + " sheep, " + str(request[1]) + " wood, " + str(request[2]) + " grain, " + str(request[3]) + " brick, " + str(request[4]) + " ore.")
    print(string)
    valid = 0
    while valid == 0:
        for index in list(range(5)):
            if inventories[player_turn_index][index + 1] > request[index]:
                valid += 1
        if valid > 0:
            confirmation = raw_input("Is this the trade you want to make? (Y/N)")
            confirmation.upper()
            if confirmation == "Y":
                for index in list(range(5)):
                    inventories[player_turn_index][index + 1] = inventories[player_turn_index][(index + 1)] - offer[index] + request[index]
                    inventories[destination_player_index][index + 1] = inventories[destination_player_index][(index + 1)] + offer[index] - request[index]
                print("The trade has been accepted.")
                return inventories
            if confirmation == "N":
                print("The trade has been rejected")
                return inventories
        if valid == 0:
            raw_input("Since you don't have enough resources for this trade, press enter to reject it.")
    
def get_resources_gathered(roll, tiles_to_buildings_dict, buildings, board, numbers, inventories):
    gathered_tiles = []
    for x in list(range(19)):
        if int(float(roll)) == int(float(numbers[x])):
            gathered_tiles.append(x)
    gathered_locations = []
    for x in gathered_tiles:
        for y in tiles_to_buildings_dict[x]:
            gathered_locations.append([y, board[x]])
    gathered_locations_with_building= []
    for x in buildings:
        for y in gathered_locations:
            if x[0] == y[0]:
                y.append(x[1])
                y.append(x[2])
                gathered_locations_with_building.append(y)
    for x in inventories:
        for y in gathered_locations_with_building:
            if str(x[0]) == str(y[2]):
                if str(y[3]) == "S":
                    if str(y[1]) == "s":
                        x[1] += 1
                    if str(y[1]) == "w":
                        x[2] += 1
                    if str(y[1]) == "g":
                        x[3] += 1
                    if str(y[1]) == "b":
                        x[4] += 1
                    if str(y[1]) == "o":
                        x[5] += 1
                if str(y[3]) == "C":
                    if str(y[1]) == "s":
                        x[1] += 2
                    if str(y[1]) == "w":
                        x[2] += 2
                    if str(y[1]) == "g":
                        x[3] += 2
                    if str(y[1]) == "b":
                        x[4] += 2
                    if str(y[1]) == "o":
                        x[5] += 2
    return inventories
    
                    


def gen_map_init():
    board = ["", "","","","","","","","","","","","","","","","","",""]
    tiles_left = ["s", "s", "s", "s", "w", "w", "w", "w", "g", "g", "g", "g", "b", "b", "b", "o", "o", "o", "d"]
    for location in list(range(19)):
        x = int(len(tiles_left)*random.random())
        board[location] = tiles_left[x]
        del tiles_left[x]
    y = board.index("d")
    board.append(y)
    return board

def gen_numbers_init(desert):
    pre_numbers = ["5 ", "2 ", "6 ", "3 ", "8 ", "10", "9 ", "12", "11", "4 ", "8 ", "10", "9 ", "4 ", "5 ", "6 ", "3 ", "11"]
    numbers = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    counter = 0
    for location in [0, 1, 2, 6, 11, 15, 18, 17, 16, 12, 7, 3, 4, 5, 10, 14, 13, 8, 9]:
        if location != desert:
            numbers[location] = pre_numbers[counter]
            counter += 1
        else:
            numbers[location] = "0 "
    return numbers
        
def display_map(board, numbers, buildings, buildings_dict, roads, roads_dict,  thief):
    board[thief] = "0"
    map_display = ""
    map_display += str("                                ==                  ==                  ==                                 " +'\n')
    map_display += str("                            ==      ==          ==      ==          ==      ==                             " +'\n')
    map_display += str("                        ==              ==  ==              ==  ==              ==                         " +'\n')
    map_display += str("                        ==     " + board[0] + "   " + numbers[0] + "   ==  ==     " +board[1] + "    " + numbers[1] + "  ==  ==     " + board[2] + "    " + numbers[2] + "  ==                         " +'\n')
    map_display += str("                        ==              ==  ==              ==  ==              ==                         " +'\n')
    map_display += str("                      ==    ==      ==    ==    ==      ==    ==    ==      ==    ==                       " +'\n')
    map_display += str("                  ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==                   " +'\n')
    map_display += str("              ==              ==  ==              ==  ==              ==  ==              ==               " +'\n')
    map_display += str("              ==    "+board[3]+"    "+numbers[3]+"   ==  ==    " + board[4] + "    " + numbers[4] + "   ==  ==    " + board[5] +"    " + numbers[5] + "   ==  ==    " + board[6] + "    " + numbers[6] + "   ==               " +'\n')
    map_display += str("              ==              ==  ==              ==  ==              ==  ==              ==               " +'\n')
    map_display += str("            ==    ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==    ==             " +'\n')
    map_display += str("        ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==         " +'\n')
    map_display += str("    ==              ==  ==              ==  ==              ==  ==              ==  ==              ==     " +'\n')
    map_display += str("    ==    " + board[7] +"    " + numbers[7] + "   ==  ==    " + board[8] + "    " + numbers[8] + "   ==  ==    " +board[9] + "    " + numbers[9] +"   ==  ==    " + board[10] + "    " + numbers[10] +"   ==  ==    " + board[11] + "    " + numbers[11] + "   ==     " +'\n')
    map_display += str("    ==              ==  ==              ==  ==              ==  ==              ==  ==              ==     " +'\n')
    map_display += str("        ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==         " +'\n')
    map_display += str("            ==    ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==    ==             " +'\n')
    map_display += str("              ==              ==  ==              ==  ==              ==  ==              ==               " +'\n')
    map_display += str("              ==    "+board[12]+"    "+numbers[12]+"   ==  ==    " + board[13] + "    " + numbers[13] + "   ==  ==    " + board[14] +"    " + numbers[14] + "   ==  ==    " + board[15] + "    " + numbers[15] + "   ==               " +'\n')
    map_display += str("              ==              ==  ==              ==  ==              ==  ==              ==               " +'\n')
    map_display += str("                  ==      ==    ==    ==      ==    ==    ==      ==    ==    ==      ==                   " +'\n')
    map_display += str("                      ==    ==      ==    ==    ==      ==    ==    ==      ==    ==                       " +'\n')
    map_display += str("                        ==              ==  ==              ==  ==              ==                         " +'\n')
    map_display += str("                        ==     " + board[16] + "   " + numbers[16] + "   ==  ==     " +board[17] + "    " + numbers[17] + "  ==  ==     " + board[18] + "    " + numbers[18] + "  ==                         " +'\n')
    map_display += str("                        ==              ==  ==              ==  ==              ==                         " +'\n')
    map_display += str("                            ==      ==          ==      ==          ==      ==                             " +'\n')
    map_display += str("                                ==                  ==                  ==                                 " +'\n')
    map_display = string_to_list(map_display)
    for building in buildings:
        print(building)
        print(buildings_dict[building[0]])
        map_display[buildings_dict[building[0]]] = str(building[1])
        map_display[buildings_dict[building[0]]+1] = str(building[2])
    for road in roads:
        for different_location in roads_dict[road[0]]:
            map_display[different_location] = str(road[1])
            map_display[different_location + 1] = str(road[2])
    map_display = list_to_string(map_display)
    print(map_display)
    return map_display

def string_to_list(string):
    final_list = []
    for index in list(range(len(string))):
        final_list.append(string[index])
    return final_list

def list_to_string(initial_list):
    final_string = ""
    for index in list(range(len(initial_list))):
        final_string = str(final_string + str(initial_list[index]))
    return final_string

def dice_roll():
    x = int(int(random.random()*6) + int(random.random()*6) + 2)
    return x

def place_first_town(player, buildings, roads, map_display, buildings_to_roads_dict, board, tiles_to_buildings_dict, inventories):
    location = -1
    road_location  = -1
    while location == -1:
        try:
            row = raw_input("What row do you want to place your building on?")
            row = int(row)
            column = raw_input("What column do you want to place your building on?")
            column = int(column)
            direction = raw_input("what direction do you want to place your building on?")
            direction = int(column)
            location = find_desired_location_building(row, column, direction)
            road_direction = raw_input("What direction would you like to build your road in?")
            road_direction = int(road_direction)
            road_location = find_desired_location_road_init(road_direction, location, buildings_to_roads_dict)
        except:
            print("That place don't make any sense")
            location= -1
        valid = test_if_building_is_in_range(location, buildings, buildings_to_roads_dict)
        if valid != 1:
            location = -1
            print("Sorry, that is an invalid location")
    buildings.append([location, str(player), "S"])
    roads.append([road_location, str(player), "R"])
    players_total_buildings = 0
    for x in buildings:
        if x[1] == player:
            players_total_buildings += 1
    gathered_tiles = []
    if players_total_buildings == 2:
        for x in list(range(19)):
            for y in tiles_to_buildings_dict[x]:
                if y == location:
                    gathered_tiles.append(x)
        for x in inventories:
            if x[0] == player:
                for y in gathered_tiles:
                    if board[y] == "s":
                        x[1] += 1
                    if board[y] == "w":
                        x[2] += 1
                    if board[y] == "g":
                        x[3] += 1
                    if board[y] == "b":
                        x[4] += 1
                    if board[y] == "o":
                        x[5] += 1
    
            
    return [buildings]

def test_if_building_is_in_range(location, buildings, buildings_to_roads_dict):
    valid = 1
    list_of_roads = []
    for x in buildings:
        for y in buildings_to_roads_dict[x[0]]:
            if y != 0:
                list_of_roads.append(y)
    for road in list_of_roads:
        for road_2 in  buildings_to_roads_dict[location]:
            if road == road_2:
                valid = -1
    return valid

def find_desired_location_road_init(road_direction, location, buildings_to_roads_dict):
    if road_direction == 7:
        modified_road_direction = 0
    if road_direction == 8:
        modified_road_direction = 1
    if road_direction == 9:
        modified_road_direction = 2
    if road_direction == 3:
        modified_road_direction = 3
    if road_direction == 2:
        modified_road_direction = 4
    if road_direction == 1:
        modified_road_direction = 5
    desired_road = buildings_to_roads_dict[location][modified_road_direction]
    return desired_road

def find_desired_location_road(row, column, direction):
    print("Under construction.  Now the program with proceed to poop out!")
    location = -1
    if row == 1:
        if column == 1:
            if direction == 1:
                location = 12
            elif direction == 4:
                location = 7
            elif direction == 7:
                location = 1
            elif direction == 9:
                location = 2
            elif direction == 6:
                location = 8
            elif direction == 3:
                location = 13
        elif column == 2:
            if direction == 1:
                location = 14
            elif direction == 4:
                location = 8
            elif direction == 7:
                location = 3
            elif direction == 9:
                location = 4
            elif direction == 6:
                location = 9
            elif direction == 3:
                location = 15
        elif column == 3:
            if direction == 1:
                location = 16
            elif direction == 4:
                location = 9
            elif direction == 7:
                location = 5
            elif direction == 9:
                location = 6
            elif direction == 6:
                location = 10
            elif direction == 3:
                location = 17
    elif row == 2:
        if column == 1:
            if direction == 1:
                location = 25
            elif direction == 4:
                location = 19
            elif direction == 7:
                location = 11
            elif direction == 9:
                location = 12
            elif direction == 6:
                location = 20
            elif direction == 3:
                location = 26
        if column == 2:
            if direction == 1:
                location = 27
            elif direction == 4:
                location = 20
            elif direction == 7:
                location = 13
            elif direction == 9:
                location = 14
            elif direction == 6:
                location = 21
            elif direction == 3:
                location = 28
        if column == 3:
            if direction == 1:
                location = 29
            elif direction == 4:
                location = 21
            elif direction == 7:
                location = 15
            elif direction == 9:
                location = 16
            elif direction == 6:
                location = 22
            elif direction == 3:
                location = 30
        if column == 4:
            if direction == 1:
                location = 31
            elif direction == 4:
                location = 22
            elif direction == 7:
                location = 17
            elif direction == 9:
                location = 18
            elif direction == 6:
                location = 23
            elif direction == 3:
                location = 32
    elif row == 3:
        if column == 1:
            if direction == 1:
                location = 40
            elif direction == 4:
                location = 34
            elif direction == 7:
                location = 24
            elif direction == 9:
                location = 25
            elif direction == 6:
                location = 35
            elif direction == 3:
                location = 41
        if column == 2:
            if direction == 1:
                location = 42
            elif direction == 4:
                location = 35
            elif direction == 7:
                location = 26
            elif direction == 9:
                location = 27
            elif direction == 6:
                location = 36
            elif direction == 3:
                location = 43
        if column == 3:
            if direction == 1:
                location = 44
            elif direction == 4:
                location = 36
            elif direction == 7:
                location = 28
            elif direction == 9:
                location = 29
            elif direction == 6:
                location = 37
            elif direction == 3:
                location = 45
        if column == 4:
            if direction == 1:
                location = 46
            elif direction == 4:
                location = 37
            elif direction == 7:
                location = 30
            elif direction == 9:
                location = 31
            elif direction == 6:
                location = 38
            elif direction == 3:
                location = 47
        if column == 5:
            if direction == 1:
                location = 48
            elif direction == 4:
                location = 38
            elif direction == 7:
                location = 32
            elif direction == 9:
                location = 33
            elif direction == 6:
                location = 39
            elif direction == 3:
                location = 49
    elif row == 4:
        if column == 1:
            if direction == 1:
                location = 55
            elif direction == 4:
                location = 50
            elif direction == 7:
                location = 41
            elif direction == 9:
                location = 42
            elif direction == 6:
                location = 51
            elif direction == 3:
                location = 56
        if column == 2:
            if direction == 1:
                location = 57
            elif direction == 4:
                location = 51
            elif direction == 7:
                location = 43
            elif direction == 9:
                location = 44
            elif direction == 6:
                location = 52
            elif direction == 3:
                location = 58
        if column == 3:
            if direction == 1:
                location = 59
            elif direction == 4:
                location = 52
            elif direction == 7:
                location = 45
            elif direction == 9:
                location = 46
            elif direction == 6:
                location = 53
            elif direction == 3:
                location = 60
        if column == 4:
            if direction == 1:
                location = 61
            elif direction == 4:
                location = 53
            elif direction == 7:
                location = 47
            elif direction == 9:
                location = 48
            elif direction == 6:
                location = 54
            elif direction == 3:
                location = 62
    if row == 5:
        if column == 1:
            if direction == 1:
                location = 67
            elif direction == 4:
                location = 63
            elif direction == 7:
                location = 56
            elif direction == 9:
                location = 57
            elif direction == 6:
                location = 64
            elif direction == 3:
                location = 68
        if column == 2:
            if direction == 1:
                location = 69
            elif direction == 4:
                location = 64
            elif direction == 7:
                location = 58
            elif direction == 9:
                location = 59
            elif direction == 6:
                location = 65
            elif direction == 3:
                location = 70
        if column == 3:
            if direction == 1:
                location = 71
            elif direction == 4:
                location = 65
            elif direction == 7:
                location = 60
            elif direction == 9:
                location = 61
            elif direction == 6:
                location = 66
            elif direction == 3:
                location = 72
    return location

def find_desired_location_building(row, column, direction):
    location = -1
    if row == 1:
        if column == 1:
            if direction == 7:
                location = 1
            elif direction == 8:
                location = 2
            elif direction == 9:
                location = 3
            elif direction == 1:
                location = 9
            elif direction == 2:
                location = 10
            elif direction == 3:
                location = 11
        elif column == 2:
            if direction == 7:
                location = 3
            elif direction == 8:
                location = 4
            elif direction == 9:
                location = 5
            elif direction == 1:
                location = 11
            elif direction == 2:
                location = 12
            elif direction == 3:
                location = 13
        elif column == 3:
            if direction == 7:
                location = 5
            elif direction == 8:
                location = 6
            elif direction == 9:
                location = 7
            elif direction == 1:
                location = 13
            elif direction == 2:
                location = 14
            elif direction == 3:
                location = 15
    elif row == 2:
        if column == 1:
            if direction == 7:
                location = 8
            elif direction == 8:
                location = 9
            elif direction == 9:
                location = 10
            elif direction == 1:
                location = 18
            elif direction == 2:
                location = 19
            elif direction == 3:
                location = 20
        if column == 2:
            if direction == 7:
                location = 10
            elif direction == 8:
                location = 11
            elif direction == 9:
                location = 12
            elif direction == 1:
                location = 20
            elif direction == 2:
                location = 21
            elif direction == 3:
                location = 22
        if column == 3:
            if direction == 7:
                location = 12
            elif direction == 8:
                location = 13
            elif direction == 9:
                location = 14
            elif direction == 1:
                location = 22
            elif direction == 2:
                location = 23
            elif direction == 3:
                location = 24
        if column == 4:
            if direction == 7:
                location = 14
            elif direction == 8:
                location = 15
            elif direction == 9:
                location = 16
            elif direction == 1:
                location = 24
            elif direction == 2:
                location = 25
            elif direction == 3:
                location = 26
    elif row == 3:
        if column == 1:
            if direction == 7:
                location = 17
            elif direction == 8:
                location = 18
            elif direction == 9:
                location = 19
            elif direction == 1:
                location = 28
            elif direction == 2:
                location = 29
            elif direction == 3:
                location = 30
        if column == 2:
            if direction == 7:
                location = 19
            elif direction == 8:
                location = 20
            elif direction == 9:
                location = 21
            elif direction == 1:
                location = 30
            elif direction == 2:
                location = 31
            elif direction == 3:
                location = 32
        if column == 3:
            if direction == 7:
                location = 21
            elif direction == 8:
                location = 22
            elif direction == 9:
                location = 23
            elif direction == 1:
                location = 32
            elif direction == 2:
                location = 33
            elif direction == 3:
                location = 34
        if column == 4:
            if direction == 7:
                location = 23
            elif direction == 8:
                location = 24
            elif direction == 9:
                location = 25
            elif direction == 1:
                location = 34
            elif direction == 2:
                location = 35
            elif direction == 3:
                location = 36
        if column == 5:
            if direction == 7:
                location = 25
            elif direction == 8:
                location = 26
            elif direction == 9:
                location = 27
            elif direction == 1:
                location = 36
            elif direction == 2:
                location = 37
            elif direction == 3:
                location = 38
    elif row == 4:
        if column == 1:
            if direction == 7:
                location = 29
            elif direction == 8:
                location = 30
            elif direction == 9:
                location = 31
            elif direction == 1:
                location = 39
            elif direction == 2:
                location = 40
            elif direction == 3:
                location = 41
        if column == 2:
            if direction == 7:
                location = 31
            elif direction == 8:
                location = 32
            elif direction == 9:
                location = 33
            elif direction == 1:
                location = 41
            elif direction == 2:
                location = 42
            elif direction == 3:
                location = 43
        if column == 3:
            if direction == 7:
                location = 33
            elif direction == 8:
                location = 34
            elif direction == 9:
                location = 35
            elif direction == 1:
                location = 43
            elif direction == 2:
                location = 44
            elif direction == 3:
                location = 45
        if column == 4:
            if direction == 7:
                location = 35
            elif direction == 8:
                location = 36
            elif direction == 9:
                location = 37
            elif direction == 1:
                location = 45
            elif direction == 2:
                location = 46
            elif direction == 3:
                location = 47
    if row == 5:
        if column == 1:
            if direction == 7:
                location = 40
            elif direction == 8:
                location = 41
            elif direction == 9:
                location = 42
            elif direction == 1:
                location = 48
            elif direction == 2:
                location = 49
            elif direction == 3:
                location = 50
        if column == 2:
            if direction == 7:
                location = 42
            elif direction == 8:
                location = 43
            elif direction == 9:
                location = 44
            elif direction == 1:
                location = 50
            elif direction == 2:
                location = 51
            elif direction == 3:
                location = 52
        if column == 3:
            if direction == 7:
                location = 44
            elif direction == 8:
                location = 45
            elif direction == 9:
                location = 46
            elif direction == 1:
                location = 52
            elif direction == 2:
                location = 53
            elif direction == 3:
                location = 54
    return location

def get_dicts():
    buildings_dict = dict([(1, 238), (2, 32), (3, 258), (4, 52), (5, 278), (6, 72), (7, 298), (8, 768), (9, 454), (10, 788), (11, 474), (12, 808), (13, 494), (14, 828), (15, 514), (16, 848), (17, 1298), (18, 984),
                           (19, 1318), (20, 1004), (21, 1338), (22, 1024), (23, 1358), (24, 1044), (25, 1378), (26, 1062), (27, 1398), (28, 1514), (29, 1848), (30, 1534), (31, 1868), (32, 1554), (33, 1888), (34, 1574),
                           (35, 1908), (36, 1594), (37, 1928), (38, 1614), (39, 2064), (40, 2398), (41, 2084), (42, 2418), (43, 2104), (44, 2428), (45, 2124), (46, 2448), (47, 2144), (48, 2614), (49, 2948), (50, 2634),
                           (51, 2654), (52, 2654), (53, 2674), (54, 2674)])
    roads_dict = dict([(1, [30, 134]), (2, [34, 146]), (3, [50, 154]), (4, [54, 166]), (5, [70, 174]), (6, [74, 186]), (7, [346]), (8, [366]), (9, [386]), (10, [406]), (11, [560, 664]), (12, [564, 676]), (13, [580, 684]),
                       (14, [584, 696]), (15, [600, 704]), (16, [604, 716]), (17, [620, 724]), (18, [624, 736]), (19, [876]), (20, [896]), (21, [916]), (22, [936]), (23, [956]), (24, [1090, 1194]), (25, [1094, 1206]),
                       (26, [1110, 1214]), (27, [1114, 1226]), (28, [1130, 1234]), (29, [1134, 1246]), (30, [1150, 1254]), (31, [1154, 1266]), (32, [1170, 1274]), (33, [1174, 1286]), (34, [1406]), (35, [1426]),
                       (36, [1446]), (37, [1466]), (38, [1486]), (39, [1506]), (40, [1624, 1736]), (41, [1640, 1744]), (42, [1644, 1756]), (43, [1660, 1764]), (44, [1664, 1776]), (45, [1680, 1784]), (46, [1684, 1796]),
                       (47, [1700, 1804]), (48, [1704, 1816]), (49, [1720, 1824]), (50, [1956]), (51, [1976]), (52, [1996]), (53, [2016]), (54, [2036]), (55, [2170, 2274]), (56, [2174, 2286]), (57, [2190, 2294]), (58, [2194, 2306]),
                       (59, [2210, 2314]), (60, [2214, 2326]), (61, [2230, 2334]), (62, [2234, 2346]), (63, [2506]), (64, [2526]), (65, [2546]), (66, [2566]), (67, [2704, 2816]), (68, [2520, 2824]), (69, [2724, 2836]),
                       (70, [2540, 2844]), (71, [2744, 2856]), (72, [2560, 2864])])
    buildings_to_roads_dict = dict([(1, [0, 0, 1, 0, 7, 0]), (2, [0, 0, 0, 2, 0, 1]), (3, [2, 0, 3, 0, 8, 0]), (4, [0, 0, 0, 4, 0, 3]), (5, [4, 0, 5, 0, 9, 0]), (6, [0, 0, 0, 6, 0, 5]), (7, [6, 0, 0, 0, 10, 0]),
                                    (8, [0, 0, 11, 0, 19, 0]), (9, [0, 7, 0, 12, 0, 11]), (10, [12, 0, 13, 0, 20, 0]), (11, [0, 8, 0, 14, 0, 13]), (12, [14, 0, 15, 0, 21, 0]), (13, [0, 9, 0, 16, 0, 15]),
                                    (14, [16, 0, 17, 0, 22, 0]), (15, [0, 10, 0, 18, 0, 17]), (16, [18, 0, 0, 0, 23, 0]), (17, [0, 0, 24, 0, 34, 0]), (18, [0, 19, 0, 25, 0, 24]), (19, [25, 0, 26, 0, 35, 0]),
                                    (20, [0, 20, 0, 27, 0, 26]), (21, [27, 0, 28, 0, 36, 0]), (22, [0, 21, 0, 29, 0, 28]), (23, [29, 0, 30, 0, 37, 0]), (24, [0, 22, 0, 31, 0, 30]), (25, [31, 0, 32, 0, 38, 0]),
                                    (26, [0, 23, 0, 33, 0, 32]), (27, [33, 0, 0, 0, 39, 0]), (28, [0, 34, 0, 40, 0, 0]), (29, [40, 0, 41, 0, 50, 0]), (30, [0, 35, 0, 42, 0, 41]), (31, [42, 0, 43, 0, 51, 0]),
                                    (32, [0, 36, 0, 44, 0, 43]), (33, [44, 0, 45, 0, 52, 0]), (34, [0, 37, 0, 46, 0, 45]), (35, [46, 0, 47, 0, 53, 0]), (36, [0, 38, 0, 48, 0, 47]), (37, [48, 0, 49, 0, 54, 0]),
                                    (38, [0, 39, 0, 0, 0, 49]), (39, [0, 50, 0, 55, 0, 0]), (40, [55, 0, 56, 0, 63, 0]), (41, [0, 51, 0, 57, 0, 56]), (42, [57, 0, 58, 0, 64, 0]), (43, [0, 52, 0, 59, 0, 58]),
                                    (44, [59, 0, 60, 0, 65, 0]), (45, [0, 53, 0, 61, 0, 60]), (46, [61, 0, 62, 0, 66, 0]), (47, [0, 54, 0, 0, 0, 62]), (48, [0, 63, 0, 67, 0, 0]), (49, [67, 0, 68, 0, 0, 0]),
                                    (50, [0, 64, 0, 69, 0, 68]), (51, [69, 0, 70, 0, 0, 0]), (52, [0, 65, 0, 71, 0, 70]), (53, [71, 0, 72, 0, 0, 0]), (54, [0, 66, 0, 0, 0, 72])])
    roads_to_roads_dict = dict([(1, [7, 2]), (2, [1, 8, 3]), (3, [2, 8, 4]), (4, [3, 9, 5]), (5, [4, 9, 6]), (6, [5, 10]), (7, [1, 11, 12]), (8, [2, 3, 13, 14]), (9, [4, 5, 15, 16]), (10, [6, 17, 18]), (11, [19, 7, 12]),
                                (12, [11, 7, 20, 13]), (13, [12, 20, 8, 14]), (14, [13, 8, 21, 15]), (15, [14, 21, 9, 16]), (16, [15, 9, 17, 22]), (17, [16, 22, 10, 18]), (18, [17, 10, 23]), (19, [16, 24, 25]), (20, [12, 13, 26, 27]),
                                (21, [14, 15, 28, 29]), (22, [16, 17, 30, 31]), (23, [18, 32, 33]), (24, [34, 19, 25]), (25, [24, 19, 26, 35]), (26, [25, 35, 20, 27]), (27, [26, 20, 28, 36]), (28, [27, 36, 21, 29]),
                                (29, [28, 21, 37, 30]), (30, [29, 37, 22, 31]), (31, [30, 22, 32, 38]), (32, [31, 38, 23, 33]), (33, [32, 23, 39]), (34, [24, 40]), (35, [25, 26, 41, 42]), (36, [27, 28, 43, 44]), (37, [29, 30, 45, 46]),
                                (38, [31, 32, 47, 48]), (39, [23, 49]), (40, [34, 41, 50]), (41, [40, 50, 35, 42]), (42, [41, 35, 51, 43]), (43, [42, 51, 36, 44]), (44, [43, 36, 45, 52]), (45, [44, 51, 37, 46]), (46, [45, 37, 47, 53]),
                                (47, [46, 53, 38, 48]), (48, [47, 38, 49, 54]), (49, [48, 54, 39]), (50, [40, 41, 55]), (51, [42, 43, 56, 57]), (52, [44, 45, 58, 59]), (53, [46, 47, 60, 61]), (54, [48, 49, 62]), (55, [50, 56, 63]),
                                (56, [55, 63, 51, 57]), (57, [56, 51, 58, 64]), (58, [57, 64, 52, 59]), (59, [58, 52, 65, 60]), (60, [59, 65, 53, 61]), (61, [60, 53, 62, 66]), (62, [61, 66, 54]), (63, [55, 56, 67]),
                                (64, [57, 58, 68, 69]), (65, [59, 60, 70, 71]), (66, [61, 62, 72]), (67, [63, 68]), (68, [67, 64, 69]), (69, [64, 68, 70]), (70, [69, 65, 71]), (71, [70, 65, 72]), (72, [71, 66])])
    tiles_to_buildings_dict = dict([(0, [1, 2, 3, 9, 10, 11]), (1, [3, 4, 5, 11, 12, 13]), (2, [5, 6, 7, 13, 14, 15]), (3, [8, 9, 10, 18, 19, 20]), (4, [10, 11, 12, 20, 21, 22]), (5, [12, 13, 14, 22, 23, 24]),
                                    (6, [14, 15, 16, 24, 25,26]), (7, [17, 18, 19, 28, 29, 30]), (8, [19, 20, 21, 30, 31, 32]), (9, [21, 22, 23, 32, 33, 34]), (10, [23, 24, 25, 34, 35, 36]), (11, [25, 26, 27, 36, 37, 38]),
                                    (12, [29, 30, 31, 39, 40, 41]), (13, [31, 32, 33, 41, 42, 43]), (14, [33, 34, 35, 43, 44, 45]), (15, [35, 36, 37, 45, 46, 47]), (16, [40, 41, 42, 48, 49, 50]), (17, [42, 43, 44, 50, 51, 52]),
                                    (18, [44, 45, 46, 52, 53, 54])])
    return_list = [buildings_dict, roads_dict, buildings_to_roads_dict, roads_to_roads_dict, tiles_to_buildings_dict]
    return return_list

main(["A", "B"])
