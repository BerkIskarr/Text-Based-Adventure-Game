import tkinter 
import random as rn


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
    

