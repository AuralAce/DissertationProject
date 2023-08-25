import random
import usb

sort = ["Colour","Alphabetically","Size"]

colour = {
    
    "0E0096E586FB": "Red",
    
    "0796ABDA4CAC": "Orange",
    
    "0E0096E5A6DB": "Yellow",
    
    "0796AE842299": "Green"
    
    }

room_names = {
    
    "0E0096E586FB": "Living",
    
    "0796ABDA4CAC": "Bedroom",
    
    "0E0096E5A6DB": "Kitchen",
    
    "0796AE842299": "Bathroom"
    
    }
    
size = {
    
    "0E0096E586FB": "64",
    
    "0796ABDA4CAC": "8",
    
    "0E0096E5A6DB": "16",

    "0796AE842299": "32"
    
    }

answer = []
colour_order = ["Red", "Orange", "Yellow", "Green"]
room_names_order = ["Bathroom", "Bedroom", "Kitchen", "Living"]
size_order = ["8", "16", "32", "64"]

def choose_sort():
    rand = random.choice(sort)
    return rand

# while True:
    type = input()