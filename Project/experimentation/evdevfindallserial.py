import evdev

def find_rfid_devices(vendor_id, product_id):
    
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    rfids = {}
    
    for dev in devices:
        
        if dev.info.vendor == vendor_id and dev.info.product == product_id:
            serial_number = get_device_serial_number(dev)
            if serial_number is not None:
                rfids[dev] = serial_number
            
    return rfids

def get_device_serial_number(device):
    
    serial_number = device.version
    return serial_number

def rfid_read(device, serial_number):
    
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.value == 1:
            rfid_data = evdev.ecodes.KEY[event.code]
            print(f"Tag: {rfid_data}, Reader Serial Number: {serial_number}")
    
def main():
    
    vendor_id = 0x1a86
    product_id = 0xdd01
    
    devices = find_rfid_devices(vendor_id, product_id)
    
    if not devices:
        print("No devices found with specified vendor and product IDS.")
    else:
        print(f"Found {len(devices)} RFID devices.")
        
        #dictionary for an RFID reader's serial number
        reader_serial_numbers = {}
        
        for device, serial_number in reader_serial_numbers.items():
            rfid_read(device, serial_number)
        
if __name__=="__main__":
    main()