from vpython import *
import time
import serial


arduino_data = serial.Serial("com9", 2000000)
time.sleep(1)
mRadius = 3
wallThickness = .3
roomWidth = 7
roomDepth = 7
roomHight = 500


floor = box(pos=vector(0, -roomHight / 2, 0), color=color.white,
            size=vector(roomWidth, wallThickness, roomDepth))
ceiling = box(pos=vector(0, +roomHight / 2, 0), color=color.white,
              size=vector(roomWidth, wallThickness, roomDepth))
rightWall = box(pos=vector(+roomWidth / 2, 0, 0), color=color.white,
                size=vector(wallThickness, roomHight, roomDepth))
leftWall = box(pos=vector(-roomWidth / 2, 0, 0), color=color.white,
               size=vector(wallThickness, roomHight, roomDepth))
backWall = box(pos=vector(0, 0, -roomDepth / 2), color=color.white,
               size=vector(roomWidth, roomHight, wallThickness))
marble = sphere(pos=vector(0, 0, 0), color=color.red, radius=mRadius)
deltaZ = .1
zPos = 7
hits = 0

while True:
    while(arduino_data.inWaiting() == 0):
        pass
    data_packet = arduino_data.readline()
    data_packet = str(data_packet, "utf-8")
    data_packet = data_packet.strip("\r\n")
    zPos = float(data_packet)
    zPos = zPos + 2
    rate(100)
    # Z direction
    zPos = zPos + deltaZ
    Zfme = zPos - mRadius
    Zbme = zPos + mRadius
    Fwe = roomHight / 2 - wallThickness / 2
    Bwe = -roomHight / 2 + wallThickness / 2
    if Zfme <= Bwe:
        zPos = -roomHight / 2 + mRadius
        hits += 1
        print(hits)

    elif Zbme >= Fwe:
        zPos = roomHight / 2 - mRadius
        hits += 1
        print(hits)
    marble.pos = vector(0, zPos, 0)
    pass
