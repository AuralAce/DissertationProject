import evdev
from pyudev import Context, Device
import selectors

# Class to hold RFID device information
class RFIDDevice:
    def __init__(self, device, serial_number, event_path):
        self.device = device
        self.serial_number = serial_number
        self.event_path = event_path

# Function to read RFID tags and get the RFID reader serial number
def read_rfid_tags(rfid_event_paths):
    
    rfid_devices = find_rfid_devices()

    print("RFID Readers Found:")
    for device in rfid_devices.values():
        print(f"Serial: {device.serial_number}, Name: {device.device.name}, Path: {device.event_path}")

    sel = selectors.DefaultSelector()
    
    print("hello")
    
    for serial_number, device in rfid_event_paths.items():
        if device.event_path is not None:
            event_device = evdev.InputDevice(device.event_path)
            event_device.grab()
            sel.register(event_device, selectors.EVENT_READ, data=(serial_number, event_device))
         
            
    while True:
        print("hello")
        for key, mask in sel.select():
            print("hello2")
            serial_number, event_device = key.data
            print("hello3")
            try:
                print("hello4")
                for event in event_device.read():
                    print("hello5")
                    if event.type == evdev.ecodes.EV_KEY:
                        key_event = evdev.categorize(event)
                        if key_event.keystate == 1:
                            tag_data = key_event.keycode[10:]
                            location = rfid_locations.get(serial_number)
                            if location is not None:
                                print(f"Tag ID: {tag_data}, scanned by RFID: {location}")
                            else:
                                print(f"Tag ID: {tag_data}, scanned by RFID: unknown")
            except Exception as e:
                print(e)
        
# Function to find USB RFID devices and retrieve their serial numbers
def find_rfid_devices():
    # Vendor and Product IDs for the RFID readers
    vendor_id = 0x1a86
    product_id = 0xdd01

    rfid_devices = {}
    
    for path in evdev.list_devices():
        try:
            device = evdev.InputDevice(path)
            if device.info.vendor==vendor_id and device.info.product==product_id:
                serial_number = get_usb_device_serial(device.path)
                if serial_number is not None:
                    rfid_devices[serial_number]= RFIDDevice(device, serial_number, path)
        except Exception as e:
            print(e)
    if not rfid_devices:
        print("Nope")
            
    return rfid_devices

def get_usb_device_serial(path: str)->str:
    context = Context()
    udev_device = Device.from_device_file(context, path)
    return udev_device.get("ID_SERIAL_SHORT")

# Serial numbers and their associated locations or names
rfid_locations = {
    "ID32B056A6": "1",
    "ID32DCC243": "2",
    "ID321845A6": "3",
    "ID3213FB4C": "4",
    "ID3275EAB8": "5",
    "ID32D085B8": "6",
    "ID32D385B8": "7"
    }

def main():
    print("hello")
    rfid_event_paths = find_rfid_devices()
    print("hello2")
    read_rfid_tags(rfid_event_paths)

if __name__ == "__main__":
    main()
