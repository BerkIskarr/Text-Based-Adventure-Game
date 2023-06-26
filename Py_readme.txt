# Text_based adventure game
By: Berk Iskar	


# How to play the game: 
The game is a text based adventure game which allows user to choose one's own name. In the main page, GUI of the user and the directory buttons, four of which directs to the rooms and one of which to the shop, are shown. Initially, the user must enter to the shop and buy a weapon- without weapon, isn't allowed to get into the fight. Also, from the shop user can buy  a key- opens the treasure- and armours -decreases the damage taken- and heal oneself, limiting five times. After buying the weapon, user can now enter the desired room. In rooms, first the description of the intro and the awards of the room is displayed, and the user can choose to either attack or run away. If attack is chosen, user will be asked to choose weapon and armour, if exist, and fight will be made. If the user comes as the winner, all of the rewards will be added to the inventory and GUI will be updated, and in condition that the user have the belonging key of the treasure, one can open it, receiving the point inside. When the user doesn't have the key, one can come back to the room to open the treasure. If the user loses, can come back to fight again but needs to heal up from the shop. In any winning condition, all of the item used in a battle will be lost afterwards. The point goes below 0 means loss, having 10 means win.


# List of libraries needed:
Tkinter 
Random
Tempfile # allows creation of temporary files
Shutil # allows to copy an existing file to another file
Sys # allows to end the run


# Link to GitHub:
https://github.com/BerkIskarr/Py_Final