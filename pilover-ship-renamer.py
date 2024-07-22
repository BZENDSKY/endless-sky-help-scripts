# Doesn't actually exactly help with content creating, but here anyway.
# Originally posted by pilover100 here: https://discord.com/channels/251118043411775489/769121688503582730/980429505166442526

"""
ship prefix adder

Instructions:
Windows users: run as is
Linux users: Comment out lines 15 and 122
             Uncomment lines 18 and 125
"""

import os
import pathlib

file_name = input("Enter save file name including extension: ")
# Windows version
path = str(pathlib.Path.home()) + "/AppData/Roaming/endless-sky/saves/" + file_name

# Linux version
#path = os.path.join("~/.local/share/endless-sky/saves", file_name)

file = open(path, "r")
text = file.read().split("\n")
file.close()

ship_section = text.index("# What you own:") + 1  # This finds the index of the first player ship in the file
pos = ship_section

ships = {}
sorting_ships = True
while sorting_ships: # This finds the next ship node
    if "ship " in text[pos] and (not "\t" in text[pos]):  # must be a root node, can't be indented
        model = (text[pos].split(" "))[1]  # Extract the model of the ship itself
        model = model.replace("\"", "")  # Remove any quotes around ship models
        pos += 1
        temp_text = text[pos].replace("\t", "")
        name_parts = temp_text.split(" ")[1:]
        name = ""
        for i in name_parts:  # This pieces back together long names with white space in
            name += i + " "
        name.strip()
        name = name.replace("\"", "")  # Remove quotes
        ships[pos-1] = [model, name]  # save the model and name tied to the starting index of the ship definition
    elif (not "\t" in text[pos]) and len(text[pos]) >= 1:  # If we are no longer in player ships, we're done here
        sorting_ships = False
    pos += 1  # Move forwards through the file
    
print("Ships loaded into memory!\n")

while True:
    # Menu
    print("+" + ("-" * 25) + "+")  # Top bar
    print("|" + "1) Remove prefixes".center(25, " ") + "|")  # this allows the player to specify prefixes to remove such as "R.N.S."
    print("|" + "2) Add prefixes".center(25, " ") + "|")  # This adds a prefix to ships, either all or specific models
    print("|" + "3) Apply name scheme".center(25, " ") + "|")  # This creates generic name schemes, either all the same or prefix + incrimenting number
    print("|" + "4) Fleet overview".center(25, " ") + "|")  # Just a quick tally of each type of ship
    print("|" + "5) Save".center(25, " ") + "|")
    print("|" + "6) Exit".center(25, " ") + "|")
    print("+" + ("-" * 25) + "+")  # bottom bar

    option = int(input("> "))
    print()
    if not 1 <= option <= 6:
        continue
        
    if 1 <= option <= 3:  # Ask which ships to apply to
        print("Which model of ship should this be applied to?")
        print("Enter nothing for all ships.")
        apply = input("> ")
        print()
    
    if option == 1:
        print("Option 1: Remove Prefixes")
        prefix = input("Enter the prefix to remove from ships: ")
        for i in ships:
            if apply == "" or apply == ships[i][0]:  # If applying to all or this model
                if ships[i][1].startswith(prefix):
                    ships[i][1] = ships[i][1][len(prefix):].strip()  # Strip off the prefix if it exists at the start and any whitespace
        print("Prefixes removed!")
    
    elif option == 2:
        print("Option 2: Add prefixes")
        prefix = input("Enter prefix to apply (whitespace will be added automatically): ") + " "
        for i in ships:
            if apply == "" or apply == ships[i][0]:  # If applying to all or this model
                ships[i][1] = prefix + ships[i][1]
        print("prefixes added!")
    
    elif option == 3:
        print("Option 3: Apply name scheme")
        numbered = int(input("Add an incrimenting number? 0 = No, 1 = Prefix, 2 = Suffix: "))
        core = input("Enter the core name for the naming system: ")
        num = 1
        
        for i in ships:
            if apply == "" or apply == ships[i][0]:  # If applying to all or this model
                if numbered == 1:
                    ships[i][1] = num + " " + core
                elif numbered == 2:
                    ships[i][1] = core + " " + num
                else:
                    ships[i][1] = core
                num += 1
    
    elif option == 4:
        print("Option 4: Fleet overview")
        models = {}
        for i in ships:
            if ships[i][0] in models:
                models[ships[i][0]] += 1
            else:
                models[ships[i][0]] = 1
        print("Model name\tnumber")
        for i in models:
            print(f"{i}\t{str(models[i])}")
    
    elif option == 5:
        print("Option 5: Save file")
        for i in ships:
            text[i] = "ship \"" + ships[i][0] + "\""
            text[i+1] = "\tname \"" + ships[i][1] + "\""
        file_name = input("Enter save file name including extension: ")
        # Windows version
        path = str(pathlib.Path.home()) + "/AppData/Roaming/endless-sky/saves/" + file_name

        # Linux version
        #path = os.path.join("~/.local/share/endless-sky/saves", file_name)
        file = open(path, "w")
        for i in text:
            file.write(i + "\n")
        file.close()
        print("File saved!")

    elif option == 6:
        break
