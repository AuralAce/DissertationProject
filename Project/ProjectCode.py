import asyncio
import evdev
import random

rfid1 = evdev.InputDevice('/dev/input/event7')
rfid2 = evdev.InputDevice('/dev/input/event9')
rfid3 = evdev.InputDevice('/dev/input/event11')
rfid4 = evdev.InputDevice('/dev/input/event13')
rfid5 = evdev.InputDevice('/dev/input/event15')
rfid6 = evdev.InputDevice('/dev/input/event17')
rfid7 = evdev.InputDevice('/dev/input/event19')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')

sort = ["Cartridge Colour","Room Name, Alphabetically","Size of Memory(GB)"]

colour = {
    
    "0009889158": "Red",
    
    "2527844940": "Orange",
    
    "0009889190": "Yellow",
    
    "2528019490": "Green",
    
    "2528028748": "Blue",
    
    "2528028480": "Indigo",
    
    "2528028129": "Violet"
    
    }

room_names = {
    
    "2527844940": "Living Room",
    
    "0009889158": "Bedroom",
    
    "2528019490": "Kitchen",
    
    "0009889190": "Bathroom",
    
    "2528028480": "Garage",
    
    "2528028129": "Hall",
    
    "2528028748": "Utility"
    
    }
    
size = {
    
    "0009889158": "64",
    
    "2527844940": "8",
    
    "0009889190": "16",

    "2528019490": "32",

    "2528028748": "512",

    "2528028480": "256",

    "2528028129": "128"
    
    }

answer = []
colour_order = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
room_names_order = ["Bathroom", "Bedroom", "Garage", "Hall" "Kitchen", "Living Room", "Utility"]
size_order = ["8", "16", "32", "64", "128", "256", "512"]

def choose_sort():
    rand = random.choice(sort)
    return rand

'''
for device in rfid1, rfid2, rfid3, rfid4, rfid5, rfid6, rfid7:
    #asyncio.ensure_future(print_events(device))
    uid = input()
    if uid == "0009889158" and evdev.util.is_device(rfid1):
        print("hello")
    elif uid == "0009889158" and evdev.util.is_device(rfid2):
        print("hello 2")
    elif uid == "0009889158" and evdev.util.is_device(rfid3):
        print("hello 3")
    elif uid == "0009889158" and evdev.util.is_device(rfid4):
        print("hello 4")
    elif uid == "0009889158" and evdev.util.is_device(rfid5):
        print("hello 5")
    elif uid == "0009889158" and evdev.util.is_device(rfid6):
        print("hello 6")
    elif uid == "0009889158" and evdev.util.is_device(rfid7):
        print("hello 7")
   
    
loop = asyncio.get_event_loop()
loop.run_forever()
'''

while True:
    sorter = choose_sort()
    print(f"Sort the computer's memory by: {sorter}")

    if sorter == "Cartridge Colour":
    
        while len(answer) < 7:
        
            uid = input()
            print (colour.get(uid))
            answer.append(colour.get(uid))
            print(answer)
        
            if answer == colour_order and len(answer) == 7:
            
                print("Correct!")
                break
        
            elif answer != colour_order and len(answer) == 7:
            
                print("Incorrect! Try Again!")
                answer.clear()
        
    if sorter == "Room Name, Alphabetically":
    
        while len(answer) < 7:
        
            uid = input()
            print (room_names.get(uid))
            answer.append(room_names.get(uid))
            print(answer)
        
            if answer == room_names_order and len(answer) == 7:
            
                print("Correct!")
                break
        
            elif answer != room_names_order and len(answer) == 7:
            
                print("Incorrect! Try Again!")
                answer.clear()
        
    if sorter == "Size of Memory(GB)":
    
        while len(answer) < 7:
        
            uid = input()
            print (size.get(uid))
            answer.append(size.get(uid))
            print(answer)
        
            if answer == size_order and len(answer) == 7:
            
                print("Correct!")
                break
        
            elif answer != size_order and len(answer) == 7:
            
                print("Incorrect! Try Again!")
                answer.clear()
    print("Puzzle Complete!")
    break