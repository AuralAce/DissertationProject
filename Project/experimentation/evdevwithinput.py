import evdev
from pyudev import Context, Device
import threading
import queue
import asyncio

# Global Variable
vendor_id = 0x1a86
product_id = 0xdd01
device_name = "RFID Reader RFID Reader Keyboard"


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
rfid1 = evdev.InputDevice(find_device_paths()[6])
rfid2 = evdev.InputDevice(find_device_paths()[5])
rfid3 = evdev.InputDevice(find_device_paths()[4])
rfid4 = evdev.InputDevice(find_device_paths()[3])
rfid5 = evdev.InputDevice(find_device_paths()[2])
rfid6 = evdev.InputDevice(find_device_paths()[1])
rfid7 = evdev.InputDevice(find_device_paths()[0])


# Function to find USB RFID devices and retrieve their serial numbers
def find_rfid_devices():
    rfid_devices = {}

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
    devices = rfid_devices

    while True:

        read = input()

        for device in rfid1, rfid2, rfid3, rfid4, rfid5, rfid6, rfid7:
            asyncio.ensure_future(print_events(device))

        loop = asyncio.get_event_loop()
        loop.run_forever()


async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path)


def main():
    devices = find_rfid_devices()
    read_rfid_device(devices)


if __name__ == "__main__":
    main()
