import evdev
from pyudev import Context, Device
import asyncio
import random
from colorama import Fore, Back, Style
import os
from hubclient import hubclient

# Global Variable
vendor_id = 0x1a86
product_id = 0xdd01
device_name = "RFID Reader RFID Reader Keyboard"
last_id = ""
rfid_devices = {}
sort = ["Cartridge Colour","Room Name, Alphabetically","Size of Memory(MB)"]
expected_answer = {}
current_answer = {}
bar = Fore.WHITE + '█'
bars = {}
names = {}
sorter = ""

colour_array = ["0009889158", "0009882317", "0009889190", "0009882781", "0009881990", "0009891572", "0009889520"] 

room_names_array = ["0009889190", "0009889158", "0009891572", "0009889520", "0009882781", "0009882317", "0009881990"] 

size_array = ["0009882317", "0009889190", "0009882781", "0009889158", "0009889520", "0009891572", "0009881990"] 

colour = {
    
    "0009889158": "Red",
    
    "0009882317": "Orange",
    
    "0009889190": "Yellow",
    
    "0009882781": "Green",
    
    "0009881990": "Blue",
    
    "0009891572": "Indigo",
    
    "0009889520": "Violet"
    
    }

room_names = {
    
    "0009889190": "Bathroom",
    
    "0009889158": "Bedroom",
    
    "0009891572": "Garage",
    
    "0009889520": "Hall",
    
    "0009882781": "Kitchen",
    
    "0009882317": "Living Room",
    
    "0009881990": "Utility"
    
    }

size = {
    
    "0009882317": "8MB",
    
    "0009889190": "16MB",

    "0009882781": "32MB",
     
    "0009889158": "64MB",
    
    "0009889520": "128MB",

    "0009891572": "256MB",
    
    "0009881990": "512MB"
    
    }

device = { # a dictionary containing our device details
        "room": "1", # ID of the room we are to register to
        "name": "Bookcase", # display name of the device
        "status": "Active", # textual status for management display
        "actions": [ # list of actions (of empty list!)
            {
                "actionid": "reset", # the ID we will receive for this action
                "name": "Reset", # friendly name for display in the hub
                "enabled": True # is this action currently available
            },
            {
                "actionid": "resettocolour", 
                "name": "Reset To Colour", 
                "enabled": True 
            },
            {
                "actionid": "resettoname", 
                "name": "Reset To Room Name", 
                "enabled": True 
            },
            {
                "actionid": "resettosize", 
                "name": "Reset To Size", 
                "enabled": True 
            },
            {
                "actionid": "printsort",
                "name": "Print Sort Type",
                "enabled": True
            }
        ]
    }

def ActionHandler(actionid): # handler when we receive an action for us
    global sorter
    print("Action handler for ID "+actionid)
    # for the demo we will toggle i.e. ACTONE will disable ONE and enable TWO and vice-versa
    if actionid == "reset":
        device['status'] = "Active"
        hub.Update(device)
        sorter = choose_sort()
        reset_program()
    elif actionid == "resettocolour":
        device['status'] = "Active"
        hub.Update(device)
        sorter = sort[0]
        reset_program()
    elif actionid == "resettoname":
        device['status'] = "Active"
        hub.Update(device)
        sorter = sort[1]
        reset_program()
    elif actionid == "resettosize":
        device['status'] = "Active"
        hub.Update(device)
        sorter = sort[2]
        reset_program()
    elif actionid == "_PING":
        print('Clearing Screen')
        os.system('clear')
    elif actionid == "printsort"
        print('Sort Cartridges By: '+sorter)
    else:
        print("Unknown action") # useful for debug
        # and we update this state i.e. push it back to the hub
        hub.Update(device)

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

#resets the program on action from hub
def reset_program():
    
    print(Style.RESET_ALL)
    devices = find_rfid_devices(sorter)
    print(f"Sort the computer's memory by: {sorter}")    
    for values in bars.values():
        print(values, end=" ")
    print("\n")

# get device paths
def find_device_paths():
    device_paths = []

    for path in evdev.list_devices():

        device = evdev.InputDevice(path)

        if (device.info.vendor == vendor_id and device.info.product == product_id
            and device.name == device_name):
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
                    
                    bars[serial_number] = bar
                    
                    if(sorter=="Cartridge Colour"):
                        
                        expected_answer[serial_number] = colour_array[i]
                        names[colour_array[i]] = colour[colour_array[i]]
                        i+=1

                    if(sorter=="Room Name, Alphabetically"):

                        expected_answer[serial_number] = room_names_array[i]
                        names[room_names_array[i]] = room_names[room_names_array[i]]
                        i+=1

                    if(sorter=="Size of Memory(MB)"):
                        
                        expected_answer[serial_number] = size_array[i]
                        names[size_array[i]] = size[size_array[i]]
                        i+=1
                    
                    current_answer[serial_number] = ""
                    #print(rfid_devices[path].serial_number, rfid_devices[path].event_path)

        except Exception as e:

            print(e)

    if not rfid_devices:
        print("No RFID Devices Found")

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
    global device
    
    while True:

        for values in bars.values():
            print(values, end= " ") 
        if current_answer == expected_answer:
            #print("\n" + Fore.WHITE + "Complete!")
            print("\n" + Fore.WHITE + "PUZZLE COMPLETE!!!")
            print(Fore.WHITE + r"""                                   .''.       
       .''.      .        *''*    :_\/_:     . 
      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-
 :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'
 : /\ : :::::     *_\/_*     -= o =-  /)\    '  *
  '..'  ':::'     * /\ *     .'/.\'.   '
      *            *..*         :
        *
        *""")
            print(Style.RESET_ALL)
            device["status"] = "Complete"
            hub.Update(device)
            await asyncio.sleep(100)
        last_id = input("\n")
        print("\x1B[F\x1B[2K", end="")
        if len(last_id) != 10:
            last_id = ""
            print("Insert 1 Card at a time! :)")
        else:
            print(Style.RESET_ALL + "Cartridge Inserted: " + names[last_id])
            await asyncio.sleep(1)

#async function using evdev package to use the event paths to continue with project logic
async def read_events(device):
    async for event in device.async_read_loop():
        #print(device.path)
        path = device.path
        #print("Hello " + path)
        serial = rfid_devices[path].serial_number
        #print("Last ID: " + last_id + " received on " + serial)
        current_answer[serial] = last_id
        #print(current_answer[serial])
        if current_answer[serial] == expected_answer[serial]:
            bars[serial] = Fore.GREEN + "█"
        else:
            bars[serial] = Fore.RED + "█"

def main():
    
    sorter = choose_sort()
    devices = find_rfid_devices(sorter)
    print(f"Sort the computer's memory by: {sorter}")
    #print(expected_answer)
    #print(current_answer)
    read_rfid_device(devices)


if __name__ == "__main__":
    
    huburi = "ws://192.168.0.2:8000/connect" # URI of the EscapeHub WS service

    hub = hubclient() # the instance of the hubclient
    
    hub.setDebug(False) # will output LOTS to the console
    
    hub.actionHandler = ActionHandler # assign the function above to handle (receive) actions for us
    
    print("Startup")

    print("Connecting to EscapeHub via "+huburi)

    hub.Connect(huburi)

    print("Registering Device")
    myid = hub.Register(device)
     
    main()

