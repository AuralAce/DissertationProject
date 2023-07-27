import asyncio
import evdev

rfid1 = evdev.InputDevice('/dev/input/event7')
rfid2 = evdev.InputDevice('/dev/input/event9')
rfid3 = evdev.InputDevice('/dev/input/event11')
rfid4 = evdev.InputDevice('/dev/input/event13')
rfid5 = evdev.InputDevice('/dev/input/event15')
rfid6 = evdev.InputDevice('/dev/input/event17')
rfid7 = evdev.InputDevice('/dev/input/event19')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')

for device in rfid1, rfid2, rfid3, rfid4, rfid5, rfid6, rfid7:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()

