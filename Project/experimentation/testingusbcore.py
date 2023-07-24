import usb

dev = usb.core.find(idVendor=0x1a86, idProduct=0xdd01)

for device in range(7): 
    
    serial = usb.util.get_string(dev, dev.iSerialNumber)
    print("Serial: "+serial)