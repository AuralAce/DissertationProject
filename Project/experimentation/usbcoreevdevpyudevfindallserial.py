import evdev
import usb.core
import usb.util
import pyudev
from pyudev import Context, Device

# Class to hold RFID device information
class RFIDDevice:
    def __init__(self, device, serial_number):
        self.device = device
        self.serial_number = serial_number

# Function to read RFID tags and get the RFID reader serial number
def read_rfid_tags(rfid_event_paths):
    
    rfid_devices = find_rfid_devices()

    print("RFID Readers Found:")
    for device in rfid_devices.values():
        print(f"Serial: {device.serial_number}, Name: {device.device.name}")

    # Read RFID tags
    while True:
        for serial_number, event_path in rfid_event_paths.items():
            if event_path is not None:
                for event in evdev.InputDevice(event_path).read_loop():
                    if event.type == evdev.ecodes.EV_KEY:
                        key_event = evdev.categorize(event)
                        if key_event.keystate == 1:  
                            tag_data = key_event.keycode[10:]
                            print(f"RFID Tag UID: {tag_data}")
                            
                            device = rfid_devices.get(serial_number)
                            if device is not None:
                                location = rfid_locations.get(serial_number)
                                if location is not None:
                                    print(f"Tag scanned by RFID Reader at Location: {location}")
                                else:
                                    print("RFID reader location not found.")
                            else:
                                print("nah")
                                
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
                    rfid_devices[serial_number]= RFIDDevice(device, serial_number)
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
    
    rfid_event_paths = find_rfid_devices()
    
    read_rfid_tags(rfid_event_paths)

if __name__ == "__main__":
    main()
