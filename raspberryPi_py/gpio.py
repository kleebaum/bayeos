#!/usr/bin/python

import time
import RPi.GPIO as GPIO
from time import sleep

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

#PINS
ADR=[11,12,13,15,16,18]
DATA=24
EN=26


# ADR Output setzen
for pin in ADR:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)

GPIO.setup(EN, GPIO.OUT)
GPIO.output(EN, GPIO.LOW)

GPIO.setup(DATA, GPIO.OUT)
GPIO.output(DATA, GPIO.LOW)

#Funktion enable
# set kurz den Enable Pin und DATA wird in die 
# gesetzte Adresse uebernommen
def enable():
  GPIO.output(EN,GPIO.HIGH);
#  print "EN is high"
#  time.sleep(0.0001);
  GPIO.output(EN,GPIO.LOW);
#  print "EN is low"


def address( a ):
  for i in range(0,6):
    GPIO.output(ADR[i],((1<<i) & a))    


# # Dauerschleife
# data=1 # entspricht GPIO.HIGH
# adr=0
# 
# while 1:
#   print "adr: %d - %d" % (adr,data)
#  
#   #Adresse anlegen
#   address(adr)
#   sleep(60)
#   #Data setzen (0 oder 1)
#   GPIO.output(DATA,data);
#   #Data auf Adresse uebenehmen
#   enable()
# 
#   time.sleep(0.1);
# 
#   adr+=1
# 
#   if(adr>15):
#     adr=0
#     data= (data!=1)

# Dauerschleife fuer jeweils 60 s spuelen, 300 s messen
adr=1   # Adresse reserviert 0 fuer Spuelen

while 1:  
    address(0)               # "Spueladresse anlegen"
    GPIO.output(DATA,1);     # Data auf 1 fuer Spuelen setzen
    enable()                 # Data auf Adresse uebenehmen
    print "adr: %d - %d" % (0,1)
    time.sleep(60)           # 60 Sekunden spuelen
    GPIO.output(DATA,0);     # Spuelvorgang beenden
    enable()                 # Data auf Adresse uebenehmen
    print "adr: %d - %d" % (0,0)
    address(adr)             # "Spueladresse anlegen"
    GPIO.output(DATA,1);     # Data auf 1
    enable()                 # Data auf Adresse uebenehmen
    print "adr: %d - %d" % (adr,1)
    time.sleep(300)          # 60 Sekunden warten, 240 Sekunden Messen
    GPIO.output(DATA,0);     # Data auf 0
    enable()                 # Data auf Adresse uebenehmen
    print "adr: %d - %d" % (adr,0)

    adr+=1

    if(adr>15):
        adr=1


