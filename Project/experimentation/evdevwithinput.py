import evdev
from pyudev import Context, Device
import asyncio

# Global Variable
vendor_id = 0x1a86
product_id = 0xdd01
device_name = "RFID Reader RFID Reader Keyboard"
last_id = ""
rfid_devices = {}


# Class to hold RFID device information
class RFIDDevice:
    def __init__(self, device, serial_number, event_path):
        self.device = device
        self.serial_number = serial_number
        self.event_path = event_path


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
def find_rfid_devices():

    for path in evdev.list_devices():

        try:

            device = evdev.InputDevice(path)

            if device.info.vendor == vendor_id and device.info.product == product_id and device.name == device_name:

                serial_number = get_usb_device_serial(device.path)

                if serial_number is not None:
                    rfid_devices[path] = RFIDDevice(device, serial_number, path)

                    print(rfid_devices[path].serial_number, rfid_devices[path].event_path)

        except Exception as e:

            print(e)

    if not rfid_devices:
        print("Nope")

    return rfid_devices


def get_usb_device_serial(path: str) -> str:
    context = Context()
    udev_device = Device.from_device_file(context, path)
    return udev_device.get("ID_SERIAL_SHORT")


def read_rfid_device(rfid_devices):

    global last_id
    
    devices = rfid_devices

    while True:
 
        #last_id = input()
        #print(last_id)

        for device in rfids:
            asyncio.ensure_future(print_events(device))
        
        asyncio.ensure_future(read_input())
        loop = asyncio.get_event_loop()

        loop.run_forever()   
        
        
async def read_input():
    
    global last_id
    
    while True:
        last_id = input()
        print("Input = " + last_id)
        await asyncio.sleep(1)


async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path)
        path = device.path
        print("Hello " + path)
        serial = rfid_devices[path].serial_number
        print("Last ID: " + last_id + " received on " + serial)
    
def main():
    devices = find_rfid_devices()
    read_rfid_device(devices)


if __name__ == "__main__":
    main()
