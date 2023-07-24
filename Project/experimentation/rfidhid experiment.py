from rfidhid.core import RfidHid

try:
    rfid = RfidHid()
except Exception as e:
    print(e)
    exit()
    
    payload_response = rfid.read_tag()
    uid = payload_response.get_tag_uid()
    
rfid.beep()
print(uid)