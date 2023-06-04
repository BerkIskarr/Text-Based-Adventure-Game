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

def shopping():
    while True:
        try:
            buy_sell=input("1. Buy \n2. Sell \n3. Quit (type 1 or 2) ")
            if buy_sell=="1":
                with open("Shop.txt","r+") as shop_txt:
                    first_line=shop_txt.readline()
                    global rand_money        
                    print("\n",first_line)
                wep_arm_heal=input("\nwhat would you like? \n1 for Weapon, \n2 for Key, \n3 for HealingPad, \n4 for Armour, \n5 for quit  >> ")
                if wep_arm_heal=="1":
                    shop_description("Shop.txt", "weapon")
                    wep_shop_choice= input("Which weapon would you like to buy, type the number (etc.,type '1' for weapon1)? >> ")
                    append_to_inventory("shop.txt",weapons,"weapon"+wep_shop_choice)
                elif wep_arm_heal=="2":
                    shop_description("Shop.txt", "key")
                    buy_key=input("1. buy\n2. go back\n")
                    if buy_key=="1":
                        append_to_inventory("shop.txt",keys, "key:") 
                elif wep_arm_heal=="3":
                    shop_description("Shop.txt", "healing") 
                    buy_heal= input("1. buy\n2. go back\n")           
                    if buy_heal=="1":
                        healing_pad()                      
                elif wep_arm_heal=="4": 
                    shop_description("Shop.txt", "armour")
                    wep_shop_choice= input("\nWhich armor would you like to buy, type the number (etc.,type '1' for armour1) ? >> ")
                    append_to_inventory("shop.txt",armours,"armour"+wep_shop_choice)
                elif wep_arm_heal=="5":
                    break
                shop_txt.close()
            elif buy_sell=="2":
                print("hello")
            if buy_sell=="3":
                break
        except:
            print("Invalid!!  ")
            
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
    

