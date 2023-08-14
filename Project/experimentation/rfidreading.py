import serial                          #import serial module

def read_rfid ():
    ser = serial.Serial ("/dev/ttyS0")  #Open named port, if using RXD , TXD pin
    #ser = serial.Serial ("/dev/ttyUSB0") # with raspberry pi/linux usb interface
    #ser = serial.Serial ("COM2") # with windows, use assigned com port number from device manager
    ser.baudrate = 9600                 #Set baud rate to 9600
    data = ser.read(12)                 #Read 12 characters from serial port to data
    ser.close ()                        #Close port
    data=data.decode("utf-8")
    return data                         #Return data

def write_rfid ():
    ser = serial.Serial ("/dev/ttyS0")  #Open named port, if using RXD , TXD pin
    ser.baudrate = 9600                 #Set baud rate to 9600
    info = input("What is your name? ")
    info = info.encode()
    data = ser.write(info)                 
    ser.close ()                        #Close port
    return data                

while True:
    id = read_rfid ()                  #Function call
    print (id)
    writer = write_rfid ()
    id = read_rfid ()                  #Function call
    print (id)