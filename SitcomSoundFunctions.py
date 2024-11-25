import threading
import serial
import os
import random

#Door checker
def doorOpenFun():
    #returns 1 if door is open, 0 if door is closed
    
    #initially set door status to open by default. Confusingly, doorOpenFun internally checks if the
    #door is closed.
    global doorStatus
    doorStatus = 1

    #define the serial USB port
    ser = serial.Serial('/dev/cu.usbserial-0001')

    #define the funciton the thread will run
    def thread_function(port):
        global doorStatus
        port.read(1)
        doorStatus = 0

    #define the thread we will run
    readThread = threading.Thread(target=thread_function, args = (ser,), daemon=True)

    #start the thread
    readThread.start()

    #wait / write / wait so as to ensure the correct ordering of things.
    os.system('sleep .1')
    ser.write(b'a')
    os.system('sleep .1')

    return doorStatus


#Bluetooth Pinger
def pingerBTFun(deviceBTAddress):
    pingStatus = os.system("blueutil --connect " + deviceBTAddress)

    if (pingStatus == 0):
        output = 1
    else:
        output = 0
    
    return output


#function for playing a song given its name
def playSoundFun(song):
    os.system("afplay sounds/" + song)



#function for picking a song when there are mutliple devices present
def pickSongFun(thisList):
    output = random.choice(thisList)
    return output 
