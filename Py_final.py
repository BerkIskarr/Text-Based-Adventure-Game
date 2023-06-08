import tkinter 
import random as rn

def bubble_sort(data,key):
    for k in range(len(data)):
        for n in range(len(data)-k-1):# -1 is to avoid resorting the elements
            if data[n][key]>data[n+1][key]:#we are comparing the key value to the next dictionary's. 
                data[n], data[n+1] = data[n+1], data[n] #if the key value is bigger than the next, it swaps the dictionaries

    return data

def shop_description(file, word):
    with open(file, "r") as shop_file:
        for line in shop_file:
            if word in line.lower():
                print(line)
def set_health(health):
    user_health.config(text="health: " + str(health))

def copy_file(source_file, target_file):
    shutil.copy(source_file, target_file)

def healing_pad(temp_file):
    global health
    with open(temp_file.name, "r+") as shop_file:
        lines_in_file = shop_file.readlines()
        for count, line in enumerate(lines_in_file):
            if "healingpad" in line.lower():
                quantity = int(lines_in_file[count + 1].strip())
                shop_description(temp_file.name, "healing") 
                print("Amount of peds: ", quantity) 
                buy_heal= input("1. buy\n2. go back\n")  
                if buy_heal=="1":
                    pad_health = int(line.split("health +")[1].split(",")[0])
                    if health == 100 and quantity > 0:
                        print("Max health, cannot buy! ")
                    elif health + pad_health <= 100 and quantity > 0:
                        health += pad_health
                        quantity -= 1
                    elif quantity <= 0:
                        print("Run out of HealingPads! ")
                    else:
                        exceeds = input("Health exceeds the max(100)\nAre you sure? ('yes' or 'no') ")
                        if exceeds == "yes":
                            health = 100
                            quantity -= 1
                    lines_in_file[count + 1] = str(quantity) + "\n"
                    shop_file.seek(0)
                    shop_file.writelines(lines_in_file)
                    shop_file.truncate()
                    set_health(health)

def append_to_inventory(file, list, word):
    my_file = open(file, "r")
    global rand_money
    whole_text = my_file.readlines()
    for line in whole_text:
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
                    print("Bought")
                    user_money.config(text=("money : " + str(rand_money)))
                else:
                    print("You already have it in your inventory! ")
            else:
                print("Not enough money! ")
    my_file.close()
    return list

name= input("Enter your name? >> ")
rand_money=rn.randint(50,310)

weapons=[]
keys=[]
armours=[]

window=tkinter.Tk()
window.geometry("700x200")
window.title("Adventure Time")

Frame_info= tkinter.Frame(window)
Frame_info.pack()

user_name=tkinter.Label(Frame_info,text=("name : "+name),font=("TimesRoman, 12"))
user_name.grid(row=0,column=1)
user_money=tkinter.Label(Frame_info,text=("money : "+str(rand_money)),font=("TimesRoman, 12"))
user_money.grid(row=0,column=2)
user_health=tkinter.Label(Frame_info,text=("health : "+str(100)),font=("TimesRoman, 12"))
user_health.grid(row=0,column=3)
user_point=tkinter.Label(Frame_info,text=("point : "+str(0)),font=("TimesRoman, 12"))
user_point.grid(row=0,column=4)

def change():
    global rand_money
    rand_money+=100
    user_health=tkinter.Label(Frame_info,text=("health : "+str(rand_money)),font=("TimesRoman, 12"))
    user_health.grid(row=0,column=3)
    
def show_inventory():
    print("weapons :",*bubble_sort(weapons,"damage"),"\nkeys : ", *bubble_sort(keys,"code"),"\narmours : ",*bubble_sort(armours,"durability"))

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
    
def sell(list, word):
    global rand_money
    if len(list)!=0:
        sorted_list=bubble_sort(list,word)
        print(sorted_list)
        number_to_sell=int(input("which one do wanna sell, enter number(etc, 1 for the 1st, 2 for the 2nd)\n"))
        price_sell=sorted_list[number_to_sell-1]["price"]
        rand_money+=price_sell
        user_money.config(text=("money : "+str(rand_money)))
        for dicts in list:
            if sorted_list[number_to_sell-1] == dicts:
                list.remove(dicts)


def shopping():
    try:
        while True:
                buy_sell=input("1. Buy \n2. Sell \n3. Quit (type 1 or 2) ")
                if buy_sell=="1":
                    with open(shop_copy.name,"r+") as shop_txt:
                        first_line=shop_txt.readline()      
                        print("\n",first_line)
                    wep_arm_heal=input("\nwhat would you like? \n1 for Weapon, \n2 for Key, \n3 for HealingPad, \n4 for Armour, \n5 for quit  >> ")
                    if wep_arm_heal=="1":
                        shop_description(shop_copy.name, "weapon")
                        wep_shop_choice= input("Which weapon would you like to buy, type the number (etc.,type '1' for weapon1)? >> ")
                        append_to_inventory(shop_copy.name,weapons,"weapon"+wep_shop_choice)
                    elif wep_arm_heal=="2":
                        shop_description(shop_copy.name, "key")
                        buy_key=input("1. buy\n2. go back\n")
                        if buy_key=="1":
                            append_to_inventory(shop_copy.name,keys, "key:") 
                    elif wep_arm_heal=="3":
                        healing_pad(shop_copy)                      
                    elif wep_arm_heal=="4": 
                        shop_description(shop_copy.name, "armour")
                        wep_shop_choice= input("\nWhich armor would you like to buy, type the number (etc.,type '1' for armour1) ? >> ")
                        append_to_inventory(shop_copy.name,armours,"armour"+wep_shop_choice)
                    elif wep_arm_heal=="5":
                        break
                    shop_txt.close()
                elif buy_sell=="2":
                    sell_choice=input("1 for weapon\n2 for keys\n3 for armour\n4 for quit")
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
                if buy_sell=="3":
                    break
    except:
        print("Invalid! ")  
def close():
    sys.exit(0)

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
    
dead_bool=[True,True,True,True]

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
    try:
        with open(room_copy.name, "r+") as room_file:
            lines_room = room_file.readlines()
            print("\n"+"-"*20+"\n")
            for lines in lines_room:
                print(lines, end="")
            print("\n"+"-"*20+"\n")
            if dead_bool[idx]==True:
                fight_run = input("1 for fight\n2 for run\n")

                if fight_run == "1":
                    if len(weapons) != 0 and health > 0:
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
                        for i in range(2):
                            updated_lines.append(lines_room[i])
                        while dict_enemy["health"] > 0 and health > 0:
                            dict_enemy["health"] -= chosen_weapon["damage"]
                            if armour_bool==True:
                                health -= round(dict_enemy["damage"] / chosen_armour["durability"])
                            else:
                                health -= dict_enemy["damage"]
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
                            for count, lines in enumerate(updated_lines):
                                if "# enemy" in lines.lower():
                                    updated_lines[count + 1] = dict_enemy["name"] + "," +str(dict_enemy["damage"]) + "," + str(dict_enemy["health"]) + "\n"
                                    break
                        elif dict_enemy["health"] <= 0:
                            run=("You already killed the enemy\n2 for leave")
                            set_health(health)
                            weapons.remove(chosen_weapon)
                            if found_arm==True:
                                armours.remove(chosen_armour)
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
                                            for count, lines in enumerate(lines_room):
                                                if "# treasure" in lines.lower():
                                                    updated_lines.append(lines_room[count-1])
                                                    updated_lines.append(lines_room[count])
                                                    updated_lines.append(lines_room[count + 1])   
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
                    
inventory=tkinter.Button(Frame_info, text="inventory", command=change)
inventory.grid(row=0, column=5)
room1_bt=tkinter.Button(Frame_info, text="Room 1", command=change, height=4,width=8)
room1_bt.grid(row=3, column=1)
room2_bt=tkinter.Button(Frame_info, text="Room 2", command=change, height=4,width=8)
room2_bt.grid(row=3, column=2)
room3_bt=tkinter.Button(Frame_info, text="Room 3", command=change, height=4,width=8)
room3_bt.grid(row=3, column=3)
room4_bt=tkinter.Button(Frame_info, text="Room 4", command=change, height=4,width=8)
room4_bt.grid(row=3, column=4)
shop_bt=tkinter.Button(Frame_info, text="Shop", command=change, height=4,width=8)
shop_bt.grid(row=3, column=5)

window.mainloop()
    

