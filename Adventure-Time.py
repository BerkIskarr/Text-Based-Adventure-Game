import tkinter
import random as rn
import tempfile # allows temporary file creation
import shutil # allows to copy an existing file to another file
import sys # used just to end run

# function to sort the lists, bubble sorting
def bubble_sort(data, key):
    for k in range(len(data)):
        for n in range(len(data) - k - 1):
            if data[n][key] > data[n + 1][key]:
                data[n], data[n + 1] = data[n + 1], data[n]
    return data
# description of the belonging type in the shop
def shop_description(file, word):
    with open(file, "r") as shop_file:
        for line in shop_file:
            if word in line.lower():
                print(line, end="")
# update the health in GUI
def set_health(health):
    user_health.config(text="health: " + str(health))
# copies the file
def copy_file(source_file, target_file):
    shutil.copy(source_file, target_file)
# manages the healing pad section of the shop
def healing_pad(temp_file):
    global health
    buy_heal_bool=False
    with open(temp_file.name, "r+") as shop_file:
        lines_in_file = shop_file.readlines()  
        # checks each line in the file      
        for count, line in enumerate(lines_in_file):
            if "healingpad" in line.lower():
                quantity = int(lines_in_file[count + 1].strip())
                shop_description(temp_file.name, "healing") 
                print("Amount of peds: ", quantity) 
                print("\n"+"-"*20+"\n")                
                while buy_heal_bool==False:
                    buy_heal= input("1. buy\n2. go back\n") 
                    # updates health of the user and the amount shown in shop according to the conditions 
                    if buy_heal=="1":
                        pad_health = int(line.split("health +")[1].split(",")[0])
                        if health == 100 and quantity > 0:
                            print("Max health, cannot buy! ")
                            buy_heal_bool=True
                        elif health + pad_health <= 100 and quantity > 0:
                            health += pad_health
                            quantity -= 1
                            print("BOUGHT")
                            buy_heal_bool=True
                        elif quantity <= 0:
                            print("Run out of HealingPads! ")
                            buy_heal_bool=True
                        else:
                            exceeds = input("Health exceeds the max(100)\nAre you sure? ('yes' or 'no') ")
                            if exceeds == "yes":
                                health = 100
                                quantity -= 1
                                buy_heal_bool=True
                        print("\n"+"-"*20+"\n")
                        # updates the file
                        lines_in_file[count + 1] = str(quantity) + "\n"
                        shop_file.seek(0)
                        shop_file.writelines(lines_in_file)
                        shop_file.truncate()
                        set_health(health)
                    elif buy_heal=="2":
                        buy_heal_bool=True
                    else:
                        print("Please enter valid option!")
# by reading from file adds the item to belonging list of items
def append_to_inventory(file, list, word):
    my_file = open(file, "r")
    global rand_money
    whole_text = my_file.readlines()
    for line in whole_text:
        # checks the line and creates the intended dict
        if word in line.lower():
            split_line = line.split(",")
            if "weapon" in word:
                dict = {"name": split_line[0].split(":")[1], "damage": int(split_line[1]), "price": int(split_line[2])}
            elif "armour" in word:
                dict = {"name": split_line[0].split(":")[0], "durability": int(split_line[0].split(":")[1]), "price": int(split_line[1])}
            elif "key" in word:
                dict = {"name": split_line[0].split(":")[0], "code": int(split_line[0].split(":")[1]), "price": int(split_line[1])}
            if rand_money >= dict["price"]:
                if dict not in list:
                    rand_money -= dict["price"]
                    list.append(dict)
                    print("\nBought\n")
                    user_money.config(text=("money : " + str(rand_money)))
                else:
                    print("You already have it in your inventory! ")
            else:
                print("Not enough money! ")
    my_file.close()
    return list

name = input("Enter your name? >> ")
rand_money = rn.randint(50, 300)

weapons=[]
keys=[]
armours=[]
# the window of tkinter
window=tkinter.Tk()
window.geometry("700x200")
window.title("Adventure Time")

Frame_info= tkinter.Frame(window)
Frame_info.pack()
health=100
point=0 
# GUI labels for health, name, money, and point
user_name=tkinter.Label(Frame_info,text=("name : "+name),font=("TimesRoman, 12"))
user_name.grid(row=0,column=1)
user_money=tkinter.Label(Frame_info,text=("money : "+str(rand_money)),font=("TimesRoman, 12"))
user_money.grid(row=0,column=2)
user_health=tkinter.Label(Frame_info,text=("health : "+str(health)),font=("TimesRoman, 12"))
user_health.grid(row=0,column=3)
user_point=tkinter.Label(Frame_info,text=("point : "+str(point)),font=("TimesRoman, 12"))
user_point.grid(row=0,column=4)

def show_inventory(word):
    global armours
    global armour_bool
    if word=="all":
        print("weapons :",*bubble_sort(weapons,"damage"),"\nkeys : ", *bubble_sort(keys,"code"),"\narmours : ",*bubble_sort(armours,"durability"))
    # in room need only the showcase of weapons
    elif word=="weapons":
        print("weapons :",*bubble_sort(weapons,"damage"))
    # in room first need to check if the user has any armour and prints the armour in inventory
    elif word=="armours":
        if len(armours)>0:
            print("armours : ",*bubble_sort(armours,"durability"))  
            armour_bool=True      
        else:
            print("dont have any armour to wear ")
            armour_bool=False
            

# creates temp files and copies existing files to temp files
with tempfile.NamedTemporaryFile(mode="w", delete=False) as shop_copy:
    copy_file("shop.txt", shop_copy.name)
with tempfile.NamedTemporaryFile(mode="w", delete=False) as room1_copy:
    copy_file("room1.txt", room1_copy.name)
with tempfile.NamedTemporaryFile(mode="w", delete=False) as room2_copy:
    copy_file("room2.txt", room2_copy.name)
with tempfile.NamedTemporaryFile(mode="w", delete=False) as room3_copy:
    copy_file("room3.txt", room3_copy.name)
with tempfile.NamedTemporaryFile(mode="w", delete=False) as room4_copy:
    copy_file("room4.txt", room4_copy.name)
# manages the sell section of the shop
def sell(list, word):
    global rand_money
    sell_bool=False
    # checks if there is any item to sell
    if len(list)!=0:
        sorted_list=bubble_sort(list,word)
        print("\n"+"-"*20+"\n")
        print(*sorted_list)
        print("\n"+"-"*20+"\n")
        # if item exist, sells the intended item and updates GUI and inventory
        while(sell_bool==False):
            number_to_sell=int(input("which one do wanna sell, enter number(etc, 1 for the 1st, 2 for the 2nd)\n"))        
            for dicts in list:
                try:
                    if sorted_list[number_to_sell-1] == dicts:
                        price_sell=sorted_list[number_to_sell-1]["price"]
                        rand_money+=price_sell
                        user_money.config(text=("money : "+str(rand_money)))
                        list.remove(dicts)
                        sell_bool=True
                        break
                except:
                    print("\n"+"-"*20+"\n")
                    print("You don't have that many items\nPlease enter the number correctly!")
                    print("\n"+"-"*20+"\n")
        print("\n"+"-"*20+"\n")
    else:
        print("\n"+"-"*20+"\n")
        print("You don't have nothing to sell!\nDirecting to the main menu... ")
        print("\n"+"-"*20+"\n")
# where all the shop algorithms take place and implemented
def shopping():
    try:
        while True:
                buy_sell=input("1. Buy \n2. Sell \n3. Quit (type 1 or 2) ")
                print("\n"+"-"*20+"\n")
                # buys according to the intended type of item
                if buy_sell=="1":
                    while True:                    
                        with open(shop_copy.name,"r+") as shop_txt:
                            first_line=shop_txt.readline()      
                            print("\n",first_line)
                            print("\n"+"-"*20+"\n")
                        wep_arm_heal=input("\nwhat would you like? \n1 for Weapon \n2 for Key \n3 for HealingPad \n4 for Armour \n5 for go back  >> ")
                        print("\n"+"-"*20+"\n")
                        if wep_arm_heal=="1":
                            shop_description(shop_copy.name, "weapon")
                            print("\n"+"-"*20+"\n")
                            wep_shop_choice= input("Which weapon would you like to buy, type the number (etc.,type '1' for weapon1)? >> ")
                            append_to_inventory(shop_copy.name,weapons,"weapon"+wep_shop_choice)
                            print("\n"+"-"*20+"\n")
                        elif wep_arm_heal=="2":
                            shop_description(shop_copy.name, "key")
                            buy_key=input("1. buy\n2. go back\n")
                            if buy_key=="1":
                                append_to_inventory(shop_copy.name,keys, "key:")
                            print("\n"+"-"*20+"\n")
                        elif wep_arm_heal=="3":
                            healing_pad(shop_copy)
                            print("\n"+"-"*20+"\n")                      
                        elif wep_arm_heal=="4": 
                            shop_description(shop_copy.name, "armour")
                            wep_shop_choice= input("\nWhich armor would you like to buy, type the number (etc.,type '1' for armour1) ? >> ")
                            append_to_inventory(shop_copy.name,armours,"armour"+wep_shop_choice)
                            print("\n"+"-"*20+"\n")
                        elif wep_arm_heal=="5":
                            break
                        else:
                            print("Doesn't exist, try again! ")
                # menu for selling the intended item        
                elif buy_sell=="2":
                    while True:
                        sell_choice=input("1 for weapon\n2 for keys\n3 for armour\n4 for go back ")
                        if sell_choice=="1":
                            sell(weapons, "damage")
                        elif sell_choice=="2":
                            sell(keys, "code")
                        elif sell_choice=="3":
                            sell(armours, "durability")
                        elif sell_choice=="4":
                            break
                        else:
                            print("Invalid! ")
                elif buy_sell=="3":
                    break
                else:
                    print("Doesn't exist, try again! ")
    except:
        print("Invalid! ")   
# ends the run
def close():
    sys.exit(0)
# manages the pop up of the ending of the game
def win_loss(sentence):
    window_new = tkinter.Tk()
    window_new.geometry("700x700")
    window_new.title("And...")
    frame = tkinter.Frame(window_new)
    frame.pack(expand=True)
    win_loss_condition = tkinter.Label(frame, text=sentence, font=("TimesRoman", 40))
    win_loss_condition.pack(expand=True)
    window_new.protocol("WM_DELETE_WINDOW", close)
    window_new.mainloop()
# to discriminate enemy being dead or alive in each file
dead_bool=[True,True,True,True]
# manages everyting about the rooms
def adventure_room(room_copy,idx):
    global rand_money
    global point
    global health
    global run
    global dead_bool
    global armour_bool
    treasure_bool=False
    key_bool=False
    pad_bool=False   
    key_exist=False
    found_wep=False
    found_arm=False
    arm_choice_bool=False
    key_found_bool=False
    fight_run_bool=False

    with open(room_copy.name, "r+") as room_file:
        lines_room = room_file.readlines()
        print("\n"+"-"*20+"\n")
        for lines in lines_room:
            print(lines, end="")
        print("\n"+"-"*20+"\n")
        # to check if enemy is alive or not
        if dead_bool[idx]==True:
            fight_run = input("1 for fight\n2 for run\n")
            while fight_run_bool==False:
                if fight_run == "1":
                    if len(weapons) != 0 and health > 0:
                        # ask which wep to choose
                        show_inventory("weapons")
                        while(found_wep==False):                                                     
                            chose_wep = input("Enter the name of the weapon as given >> ")
                            for dict in weapons:
                                if dict["name"]==chose_wep:
                                    chosen_weapon=dict
                                    found_wep=True           
                                else:
                                    print("Doesn't exist, please enter from existing weapons")
                        chosen_armour = {}
                        treasure_enemy = {}   
                        # asks to choose armour if exist and user wants to wear an armour      
                        show_inventory("armours")
                        if armour_bool==True:
                            while(arm_choice_bool==False):
                                arm_choice=input("Do you wanna wear armour? (y/n)")
                                if arm_choice=='y':
                                    while(found_arm==False):  
                                        chose_arm = input("Enter the name of the desired armour as given >> ")   
                                        for dict in armours:                        
                                            if dict["name"]==chose_arm:
                                               chosen_armour=dict
                                               found_arm=True
                                               arm_choice_bool=True 
                                            else:
                                                print("Doesn't exist, please enter from existing weapons")
                                elif arm_choice=='n':
                                    armour_bool=False
                                    print("\n"+"-"*20+"\n")
                                    print("as you wish ") 
                                    arm_choice_bool=True                           
                                else:
                                    print("Invalid input, please reenter!\n")
                        # according to the key words, saves each value in variables, mostly as dicts
                        for count, lines in enumerate(lines_room):
                            if "# enemy" in lines.lower():
                                enemy_line = lines_room[count + 1].split(",")
                                dict_enemy = {"name": enemy_line[0], "damage": int(enemy_line[1]), "health": int(enemy_line[2])}
                            elif "# point" in lines.lower():
                                point_line = int(lines_room[count + 1])
                            elif "# weapon" in lines.lower():
                                weapon_line = lines_room[count + 1].split(",")
                                dict_weapon = {"name": weapon_line[0], "damage": int(weapon_line[1]), "price": int(weapon_line[2])}
                            elif "# money" in lines.lower():
                                money_line = int(lines_room[count + 1])
                            elif "# treasure" in lines.lower():
                                treasure_bool=True
                                treasure_line = lines_room[count + 1].split(",")
                                treasure_enemy = {"code": int(treasure_line[0]), "point": int(treasure_line[1])}
                            elif "# key" in lines.lower():
                                key_bool=True
                                key_line = lines_room[count + 1].split(",")
                                key_enemy = {"name": "key", "code": int(key_line[0]), "price": int(key_line[1])}
                            elif "# healingpad" in lines.lower():
                                pad_bool=True
                                pad_line=int(lines_room[count + 1])
                        updated_lines = []
                        # saves the main intro of the room
                        for i in range(2):
                            updated_lines.append(lines_room[i])
                        # part where the fight occur, different if the arm was worn
                        while dict_enemy["health"] > 0 and health > 0:
                            dict_enemy["health"] -= chosen_weapon["damage"]
                            if armour_bool==True:
                                health -= round(dict_enemy["damage"] / chosen_armour["durability"])
                            else:
                                health -= dict_enemy["damage"]
                        # losing condition: extracts points, set health of the both enemy and the user, updating the file
                        if health<=0 and health<dict_enemy["health"]:
                            updated_lines.clear()
                            updated_lines=lines_room
                            print("\n"+"-"*20+"\n")
                            print("You lost! ")
                            point-=2
                            user_point.config(text=("point: " + str(point)))
                            weapons.remove(chosen_weapon)
                            health=0
                            set_health(health)
                            if found_arm==True:
                                armours.remove(chosen_armour)
                            for count, lines in enumerate(updated_lines):
                                if "# enemy" in lines.lower():
                                    updated_lines[count + 1] = dict_enemy["name"] + "," +str(dict_enemy["damage"]) + "," + str(dict_enemy["health"]) + "\n"
                                    break
                        # winning condition: updates every value
                        elif dict_enemy["health"] <= 0:
                            run=("You already killed the enemy\n2 for leave")
                            set_health(health)
                            weapons.remove(chosen_weapon)
                            if found_arm==True:
                                armours.remove(chosen_armour)
                            #  if there is health pad in the room, adds to health
                            if pad_bool==True:
                                if health + pad_line <= 100:
                                    health += pad_line
                                else:
                                    health=100
                                user_health.config(text=("health : "+str(health)))  
                            print("\n"+"-"*20+"\n")
                            print("Congrats!! " + dict_enemy["name"] + " has been defeated!!\n")
                            weapons.append(dict_weapon)
                            point += point_line
                            user_point.config(text=("point: " + str(point)))
                            rand_money += money_line
                            user_money.config(text=("money: " + str(rand_money)))
                            print("Weapon, point, and money added!\n")
                            if key_bool==True:
                                keys.append(key_enemy)
                            if treasure_bool==True:
                                while(key_found_bool==False):
                                    treasure_choice = input("Wanna open the treasure? (y/n) ")
                                    for key in keys:
                                        if treasure_enemy["code"] in key.values():
                                            key_exist=True
                                    if treasure_choice == "y":
                                        # if the user has the key opens the treasure and updates the file
                                        if key_exist==True:
                                            for key in keys:
                                                if treasure_enemy["code"] in key.values():
                                                    print("\nChest opened\n")
                                                    point += treasure_enemy["point"]
                                                    user_point.config(text=("point: " + str(point)))
                                                    keys.remove(key)
                                                    key_found_bool=True
                                                    break
                                        # if cannot open treasure saves the lines belonging to the treasure for later
                                        else:
                                            print("You don't have the correct key! Please type 'n' to skip! ")  
                                    # saves the lines belonging to the treasure for later
                                    elif treasure_choice == "n":
                                        print("You can come back anytime for the treasure!")
                                        for count, lines in enumerate(lines_room):
                                            if "# treasure" in lines.lower():
                                                updated_lines.append(lines_room[count-1])
                                                updated_lines.append(lines_room[count])
                                                updated_lines.append(lines_room[count + 1])
                                                key_found_bool=True
                                    else:
                                        print("Invalid input, try again!\n")
                            dead_bool[idx]=False
                        # updates the file
                        room_file.seek(0)
                        room_file.writelines(updated_lines)
                        room_file.truncate()
                        break
                    else:
                        print("Don't have any weapons or health, go to the shop!")
                        break
                elif fight_run == "2":
                    print("\n"+"-"*20+"\n")
                    print("Get stronger and come back!")
                    print("\n"+"-"*20+"\n")
                    break
                else:
                    print("Invalid input, please enter valid option")
                    break
        # if enemy is already dead
        elif dead_bool[idx]==False:
            print("Enemy is dead")
            updated_lines=[]
            for i in range(2):
                updated_lines.append(lines_room[i])
            # if there is still treasure in the room
            for count, lines in enumerate(lines_room):
                if "# treasure" in lines.lower():
                    treasure_bool=True
                    treasure_line = lines_room[count + 1].split(",")
                    treasure_enemy = {"code": int(treasure_line[0]), "point": int(treasure_line[1])}
            if treasure_bool==True:
                while(key_found_bool==False):
                    treasure_choice = input("Wanna open the treasure? (y/n) ")
                    for key in keys:
                        if treasure_enemy["code"] in key.values():
                            key_exist=True
                    # if the user has the key opens the treasure and updates the file
                    if treasure_choice == "y":
                        if key_exist==True:
                            for key in keys:
                                if treasure_enemy["code"] in key.values():
                                    print("\nChest opened\n")
                                    point += treasure_enemy["point"]
                                    user_point.config(text=("point: " + str(point)))
                                    keys.remove(key)
                                    key_found_bool=True
                                    break
                        else:
                            print("You don't have the correct key! Please type 'n' to skip! ") 
                    # saves the treasure for later entrance to the room
                    elif treasure_choice == "n":
                        print("You can come back anytime for the treasure!")
                        for count, lines in enumerate(lines_room):
                            if "# treasure" in lines.lower():
                                updated_lines.append(lines_room[count-1])
                                updated_lines.append(lines_room[count])
                                updated_lines.append(lines_room[count + 1])
                                key_found_bool=True
                    else:
                        print("Invalid input, try again!\n")
            room_file.seek(0)
            room_file.writelines(updated_lines)
            room_file.truncate()
    if point < 0:
        win_loss("You Lost! Such a Loser!")
    elif point >= 10:
        win_loss("Congrats! You won!")

# the creation of all the buttons and commands the functions
inventory=tkinter.Button(Frame_info, text="inventory", command=lambda:show_inventory("all"))
inventory.grid(row=0, column=5)
room1_bt=tkinter.Button(Frame_info, text="Room 1", command=lambda:adventure_room(room1_copy,0), height=4,width=8)
room1_bt.grid(row=3, column=1)
room2_bt=tkinter.Button(Frame_info, text="Room 2", command=lambda:adventure_room(room2_copy,1), height=4,width=8)
room2_bt.grid(row=3, column=2)
room3_bt=tkinter.Button(Frame_info, text="Room 3", command=lambda:adventure_room(room3_copy,2), height=4,width=8)
room3_bt.grid(row=3, column=3)
room4_bt=tkinter.Button(Frame_info, text="Room 4", command=lambda:adventure_room(room4_copy,3), height=4,width=8)
room4_bt.grid(row=3, column=4)
shop_bt=tkinter.Button(Frame_info, text="Shop", command=shopping, height=4,width=8)
shop_bt.grid(row=3, column=5)

window.mainloop()
    
