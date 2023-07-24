import usb.core
import usb.util
import threading
import keyboard

def find_rfid_devices(vendor_id, product_id):
    
    devices = usb.core.find(find_all=True)
    
    rfids = []
    
    for dev in devices:
        
        #checking if the vendor and product ids match
        if dev.idVendor == vendor_id and dev.idProduct == product_id:
            rfids.append(dev)
            
    return rfids

def rfid_read(serial_number):
    
    while True:
        try:
            rfid_data = input("Please Scan RFID Tag: ")
            print(f"Tag: {rfid_data}, Serial Number: {serial_number}")
        except KeyboardInterrupt:
            break
    
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
        
        for i, dev in enumerate(devices):
        
            serial_number = usb.util.get_string(dev, dev.iSerialNumber)
            reader_serial_numbers[dev] = serial_number
            print("hello")
          
        threads = []
        
        for serial_number in reader_serial_numbers.values():
            print("thread")
            thread = threading.Thread(target=rfid_read, args=(serial_number))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        while True:
            pass
        
if __name__=="__main__":
    main()