import serial
from Crypto.Cipher import AES
import time

ser = serial.Serial(            
	port='/dev/serial0',
	baudrate = 38400,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1000)

keyraw = b'2b7e151628aed2a6abf7158809cf4f3c'
key = [int(keyraw[i:i+2],16) for i in range(0, len(keyraw),2)]
cipher = AES.new(bytes(key), AES.MODE_ECB)

ack = b'z00\n'


while True:
	try:
		if ser.in_waiting > 0:
			data = ser.readline() 

			if len(data)==34:
				command = data[0]
				pt = [int(data[i:i+2],16) for i in range(1, len(data)-1,2)]

				if chr(command) == 'p':
					
					ct = cipher.encrypt(bytes(pt))

					
					rawmsg = ['r']
					rawmsg.extend(['{:02x}'.format(a) for a in ct])
					rawmsg.extend(['\n'])
					msg = ''.join(rawmsg)
					
					print(msg.encode())

					#ser.flush()
					
					a=ser.write(msg.encode())
					#time.sleep(0.05)
					a=ser.write(ack) 
			
	except OSError:
		print("error")
		ser.close()
		ser.open()
ser.close()
