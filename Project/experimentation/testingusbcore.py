import usb.core
import usb

dev=usb.core.find(idVendor=0x1a86, idProduct= 0xdd01,iSerial= "ID3213FB4C")

print(usb.util.get_string(dev, dev.iSerialNumber))
