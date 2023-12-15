import time
import serial


arduino_data = serial.Serial("com9", 2000000)

time.sleep(1)

while True:
    while(arduino_data.inWaiting() == 0):
        pass
    data_packet = arduino_data.readline()
    data_packet = str(data_packet, "utf-8")
    data_packet = data_packet.strip("\r\n")
    x = float(data_packet)
    print(x)
