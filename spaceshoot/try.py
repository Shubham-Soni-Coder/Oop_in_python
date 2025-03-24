import json 
import os



if 
# load program 
with open('data/data.json','r') as file:
    data = json.load(file)


def check_level(level_name):
    # check for file exists or not 
    if level_name not in data["levels"]:
        return f"{level_name} not found"
    
    # check if level is completed or not
    is_complete = data["levels"][level_name]["completed"]

    return is_complete if is_complete else False



def complete_level(current_level):
    levels = list(data["levels"].keys())

    is_complete = check_level(current_level)

    if current_level not in levels:
        return f"{current_level} not found"

    if not is_complete:
        return f"complete {current_level} first "

    level_index = levels.index(current_level) # get the index of current level

    # mark current level is completed 
    data["levels"][current_level]["completed"] = True


    # unlocked next index if its exists 

    if level_index +1 < len(levels):
        next_level = levels[current_level+1]
        data["levels"][next_level]["completed"] = True
        print(f"{current_level} completed.{next_level} is unlocked")

    else :
        print(f"{current_level} completed you completed all the levels")

    # updated the json file 
    with open('data?data.json','w') as file:
        json.dump(data, file, indent=4)

if __name__=="__main__":
    print(complete_level('level1')) # should return False