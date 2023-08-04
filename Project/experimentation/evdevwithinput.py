import evdev
from pyudev import Context, Device
import asyncio
import random

# Global Variable
vendor_id = 0x1a86
product_id = 0xdd01
device_name = "RFID Reader RFID Reader Keyboard"
last_id = ""
rfid_devices = {}
sort = ["Cartridge Colour","Room Name, Alphabetically","Size of Memory(GB)"]
expected_answer = {}
current_answer = {}

colour = {
    
    "0009889158": "Red",
    
    "2527844940": "Orange",
    
    "0009889190": "Yellow",
    
    "2528019490": "Green",
    
    "2528028748": "Blue",
    
    "2528028480": "Indigo",
    
    "2528028129": "Violet"
    
    }

colour_array = ["0009889158", "2527844940", "0009889190", "2528019490", "2528028748", "2528028480", "2528028129"] 

room_names = {
    
    "0009889190": "Bathroom",
    
    "0009889158": "Bedroom",
    
    "2528028480": "Garage",
    
    "2528028129": "Hall",
    
    "2528019490": "Kitchen",
    
    "2527844940": "Living Room",
    
    "2528028748": "Utility"
    
    }

room_names_array = ["0009889190", "0009889158", "2528028480", "2528028129", "2528019490", "2527844940", "2528028748"] 

size = {
    
    "2527844940": "8",
    
    "0009889190": "16",

    "2528019490": "32",
    
    "0009889158": "64",
    
    "2528028129": "128",

    "2528028480": "256",
    
    "2528028748": "512"
    
    }

size_array = ["2527844940", "0009889190", "2528019490", "0009889158", "2528028129", "2528028480", "2528028748"] 

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
        
        asyncio.ensure_future(read_input())
        
        
        loop = asyncio.get_event_loop()
        loop.run_forever()   
        
#async function that accepts input from the RFID reader and then sleeps so the next async function can take place
async def read_input():
    
    global last_id
    
    while True:
        last_id = input()
        print("Input = " + last_id)
        await asyncio.sleep(1)

#async function using evdev package to use the event paths to continue with project logic
async def read_events(device):
    async for event in device.async_read_loop():
        print(device.path)
        path = device.path
        print("Hello " + path)
        serial = rfid_devices[path].serial_number
        print("Last ID: " + last_id + " received on " + serial)
        current_answer[serial] = last_id
        print(current_answer[serial])
        print(current_answer)
        if current_answer == expected_answer:
            print("Complete!")
    
def main():
    sorter = choose_sort()
    devices = find_rfid_devices(sorter)
    print(f"Sort the computer's memory by: {sorter}")
    print(expected_answer)
    print(current_answer)
    read_rfid_device(devices)


if __name__ == "__main__":
    main()
