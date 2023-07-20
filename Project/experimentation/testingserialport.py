import serial.tools.list_ports as list_ports

device_signature = '1a86:dd01'

def find_serial_device():
    
    
    candidates = list(list_ports.grep(device_signature))
    
    if not candidates:
        
        raise ValueError(f'No device with signature {device_signature} found')
    
    if len(candidates)>1:
        
        raise ValueError(f'Multiple devices with signature {device_signature} found')
    
    return cadidates[0].device

print(find_serial_device())