#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time
import signal

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT)

openState = 2.5
closeState = 5.0
doorOpen = False

cardReading = True

p = GPIO.PWM(8,50)
p.start(2.5)

MIFAREReader = MFRC522.MFRC522()

def end_read(signal,frame):
    print "Ctrl+C captured, ending read."
    p.stop()
    GPIO.cleanup()
    exit

signal.signal(signal.SIGINT, end_read)


while cardReading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "A card has been detected. \n"
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print("Card UID: " + str(uid))
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        if status == MIFAREReader.MI_OK:
            card_Data = MIFAREReader.MFRC522_Read(8)
            print "Card Data: " + card_Data
            MIFAREReader.MFRC522_StopCrypto1()
            if card_Data == "[1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2]":
                print("Access granted.")
                if doorOpen == True:
                    p.ChangeDutyCycle(closeState)
                    doorOpen = False
                    print("The door is now closed.")
                    time.sleep(1)
                else:
                    p.ChangeDutyCycle(openState)
                    doorOpen = True
                    print("The door is now open.")
                    time.sleep(1)
            else:
                print("Access denied.")
        else:
            print("Card authorisation failed.")
