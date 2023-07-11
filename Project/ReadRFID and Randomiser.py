import random
import serial

#card tag id 1: 0E0096E586FB
#fob tag id  2: 0796ABDA4CAC
#card tag id 3: 0E0096E5A6DB
#fob tag id  4: 0796AE842299

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

def read_rfid():
    ser = serial.Serial ("/dev/ttyS0")  #Open named port, if using RXD , TXD pin
    ser.baudrate = 9600                 #Set baud rate to 9600
    data = ser.read(12)                 #Read 12 characters from serial port to data
    ser.close ()						#Close port
    data=data.decode("utf-8")
    return data                         #Return data

def choose_sort():
    rand = random.choice(sort)
    return rand
    
sorter = choose_sort()
print("Sort by: " + sorter)
print("Tap tags in correct order")
print(colour)
print(size)
print(room_names)

if sorter == "Colour":
    
    while len(answer) < 4:
        
        id = read_rfid()
        print (colour.get(id))
        answer.append(colour.get(id))
        print(answer)
        
        if answer == colour_order and len(answer) == 4:
            
            print("Correct!")
            break
        
        elif answer != colour_order and len(answer) == 4:
            
            print("Incorrect! Try Again!")
            answer.clear()
        
if sorter == "Alphabetically":
    
    while len(answer) < 4:
        
        id = read_rfid()
        print (room_names.get(id))
        answer.append(room_names.get(id))
        print(answer)
        
        if answer == room_names_order and len(answer) == 4:
            
            print("Correct!")
            break
        
        elif answer != room_names_order and len(answer) == 4:
            
            print("Incorrect! Try Again!")
            answer.clear()
        
if sorter == "Size":
    
    while len(answer) < 4:
        
        id = read_rfid()
        print (size.get(id))
        answer.append(size.get(id))
        print(answer)
        
        if answer == size_order and len(answer) == 4:
            
            print("Correct!")
            break
        
        elif answer != size_order and len(answer) == 4:
            
            print("Incorrect! Try Again!")
            answer.clear()
