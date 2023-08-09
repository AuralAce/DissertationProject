import evdev
from pyudev import Context, Device
import asyncio
import random
from colorama import Fore, Back, Style
from PIL import Image

# Global Variable
vendor_id = 0x1a86
product_id = 0xdd01
device_name = "RFID Reader RFID Reader Keyboard"
last_id = ""
rfid_devices = {}
sort = ["Cartridge Colour","Room Name, Alphabetically","Size of Memory(GB)"]
expected_answer = {}
current_answer = {}
#main_img = Image.open("Images/Sort The Memory Cards.png")
#green_images = {}
#red_images = {}
bar = Fore.WHITE + '█'
bars = {}

'''
green_bars = [Image.open("Images/Green 1.png"), Image.open("Images/Green 2.png"), Image.open("Images/Green 3.png"),
              Image.open("Images/Green 4.png"), Image.open("Images/Green 5.png"), Image.open("Images/Green 6.png"),
              Image.open("Images/Green 7.png")]

red_bars = [Image.open("Images/Red 1.png"), Image.open("Images/Red 2.png"), Image.open("Images/Red 3.png"),
              Image.open("Images/Red 4.png"), Image.open("Images/Red 5.png"), Image.open("Images/Red 6.png"),
              Image.open("Images/Red 7.png")]
'''

colour_array = ["0009889158", "0009882317", "0009889190", "0009882781", "0009881990", "0009891572", "0009889520"] 

room_names_array = ["0009889190", "0009889158", "0009891572", "0009889520", "0009882781", "0009882317", "0009881990"] 

size_array = ["0009882317", "0009889190", "0009882781", "0009889158", "0009889520", "0009891572", "0009881990"] 

# Class to hold RFID device information
class RFIDDevice:
    def __init__(self, device, serial_number, event_path):
        self.device = device
        self.serial_number = serial_number
        self.event_path = event_path

#function to choose how the puzzle must be sorted
def choose_sort():
    rand = random.choice(sort)
    return rand

'''
#Uses PIL to composite the correct sort image onto the background image
def sort_image(sorter):
    
    global main_img
    
    sort_img = Image.open(f"Images/{sorter}.png")
    
    main_img = Image.alpha_composite(main_img, sort_img)
'''

# get device paths
def find_device_paths():
    device_paths = []

    for path in evdev.list_devices():

        device = evdev.InputDevice(path)

        if device.info.vendor == vendor_id and device.info.product == product_id and device.name == device_name:
            device_paths.append(path)

    return device_paths

# Global path variables
rfids = []
for i in range(7):
    rfids.append(evdev.InputDevice(find_device_paths()[i]))

# Function to find USB RFID devices and retrieve their serial numbers
def find_rfid_devices(sorter):

    i = 0

    for path in evdev.list_devices():

        try:

            device = evdev.InputDevice(path)

            if device.info.vendor == vendor_id and device.info.product == product_id and device.name == device_name:

                serial_number = get_usb_device_serial(device.path)

                if serial_number is not None:
                    
                    rfid_devices[path] = RFIDDevice(device, serial_number, path)
                    
                    #green_images[serial_number] = green_bars[i]
                    
                    #red_images[serial_number] = red_bars[i]
                    
                    bars[serial_number] = bar
                    
                    if(sorter=="Cartridge Colour"):
                        
                        expected_answer[serial_number] = colour_array[i]
                        i+=1

                    if(sorter=="Room Name, Alphabetically"):

                        expected_answer[serial_number] = room_names_array[i]
                        i+=1

                    if(sorter=="Size of Memory(GB)"):
                        
                        expected_answer[serial_number] = size_array[i]
                        i+=1
                    
                    current_answer[serial_number] = ""
                    print(rfid_devices[path].serial_number, rfid_devices[path].event_path)

        except Exception as e:

            print(e)

    if not rfid_devices:
        print("Nope")

    return rfid_devices

#using udev to get the serial number of the usb devices
def get_usb_device_serial(path: str) -> str:
    context = Context()
    udev_device = Device.from_device_file(context, path)
    return udev_device.get("ID_SERIAL_SHORT")

#function that starts the reading from the RFID devices
def read_rfid_device(rfid_devices):

    global last_id
    
    devices = rfid_devices

    while True:
     
        for device in rfids:
            asyncio.ensure_future(read_events(device))
        
        #asyncio.ensure_future(display_image())
        
        asyncio.ensure_future(read_input())
        
        
        loop = asyncio.get_event_loop()
        loop.run_forever()   
        
#async function that accepts input from the RFID reader and then sleeps so the next async function can take place
async def read_input():
    
    global last_id
    #global main_img
    
    while True:
        for values in bars.values():
            print(values, end=" ")
        last_id = input("\n")
        print("Input = " + last_id)
        await asyncio.sleep(1)
        #main_img.show()
        if current_answer == expected_answer:
            print("Complete!")

#async function using evdev package to use the event paths to continue with project logic
async def read_events(device):
    async for event in device.async_read_loop():
        #global main_img
        print(device.path)
        path = device.path
        print("Hello " + path)
        serial = rfid_devices[path].serial_number
        print("Last ID: " + last_id + " received on " + serial)
        current_answer[serial] = last_id
        print(current_answer[serial])
        '''
        if current_answer[serial] == expected_answer[serial]:
            bar_img = green_images[serial]
            main_img = Image.alpha_composite(main_img, bar_img)
        else:
            bar_img = red_images[serial]
            main_img = Image.alpha_composite(main_img, bar_img)
        '''
        if current_answer[serial] == expected_answer[serial]:
            bars[serial] = Fore.GREEN + "█"
        else:
            bars[serial] = Fore.RED + "█"
'''           
#uses PIL Image.show() to display image to screen
async def display_image():
    main_img.show()
'''

def main():
    
    sorter = choose_sort()
    #img = sort_image(sorter)
    #main_img.show()
    devices = find_rfid_devices(sorter)
    print(f"Sort the computer's memory by: {sorter}")
    print(expected_answer)
    print(current_answer)
    read_rfid_device(devices)


if __name__ == "__main__":
    main()

