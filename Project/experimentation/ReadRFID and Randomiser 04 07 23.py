import random
import serial

#card tag id 1: 0E0096E586FB
#fob tag id  2: 0796ABDA4CAC
#card tag id 3: 0E0096E5A6DB
#fob tag id  4: 0796AE842299

def read_rfid():
    ser = serial.Serial ("/dev/ttyS0")  #Open named port, if using RXD , TXD pin
    ser.baudrate = 9600                 #Set baud rate to 9600
    data = ser.read(12)                 #Read 12 characters from serial port to data
    ser.close ()						#Close port
    data=data.decode("utf-8")
    return data                         #Return data

def choose_sort():

    sort = ["A","B","C","D","E", "F"]
    rand = random.choice(sort)
    return rand
    
while True:
    print("Tap tag to read")
    id = read_rfid()                  #Function call
    print (id)
    sort = choose_sort()
    print(sort)

