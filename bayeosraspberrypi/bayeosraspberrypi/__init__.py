import ConfigParser
from bayeosgatewayclient import BayEOSGatewayClient
from random import randint
import time
from time import sleep
import os
import RPi.GPIO as GPIO
from sht21 import SHT21
from mcp3424 import MCP3424

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "../config/", "bayeosraspberrypi.ini")

config = ConfigParser.ConfigParser()
try:
    config.read(DATA_PATH)
    if not config.has_option('Special', 'names'):
        for i in range(0, len(config.get('Special', 'host').split(','))):
            names = {}
            names[i] = 'IP' + config.get('Special', 'host').split(',')[i]
    else:
        names = config.get('Special', 'names').split(', ')
    
    if not config.has_option('Sender', 'sender'):
        config.set('Sender', 'sender', names)
except ConfigParser.NoSectionError as e:
    print "Config File (.ini) not found or with missing values."


options = {}
for section in config.sections():
    for key, val in config.items(section):
        options[key] = val

print options

try:
    sht21 = SHT21(1)
    mcp3424 = MCP3424(0x68, 18)
    
except IOError, e:
    print e
    print "Error creating connection to i2c.  This must be run as root. Did you use the right device number?"

def measure():
    print "Channel 1: %02f" % mcp3424.read_voltage(1)
    print "Temperature: %s" % sht21.read_temperature()
    print "Humidity: %s" % sht21.read_humidity()

measure()

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

#PINS
ADR=[11,12,13,15,16,18] # GPIO 17, 18, 27, 22, 23, 24
DATA=24 # GPIO 8
EN=26   # GPIO 7

#Funktion enable
# set kurz den Enable Pin und DATA wird in die 
# gesetzte Adresse uebernommen
def enable():
    GPIO.output(EN,GPIO.HIGH);
#  print "EN is high"
#  time.sleep(0.0001);
    GPIO.output(EN,GPIO.LOW);
#  print "EN is low"


def address(a):
    for i in range(0,6): # ADR[0]=11, ADR[1]=12...
        GPIO.output(ADR[i],((1<<i) & a)) # binary shift to left (2^i) and 
        #print str(ADR[i]) + ": " + str((1<<i) & a)
        # Bsp.: a = 3
        # Pin 11 = 1
        # Pin 12 = 2, alle anderen 0
        
try:
    # ADR Output setzen
    for pin in ADR:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    GPIO.setup(EN, GPIO.OUT)
    GPIO.output(EN, GPIO.LOW)
    
    GPIO.setup(DATA, GPIO.OUT)
    GPIO.output(DATA, GPIO.LOW)
    
except KeyboardInterrupt:
    GPIO.cleanup() 
    
    # Dauerschleife fuer jeweils 60 s spuelen, 300 s messen
    adr=1   # Adresse reserviert 0 fuer Spuelen

class RasperryPi(BayEOSGatewayClient):
    
    def readData(self):
        if self.i == 0:
            tFile = open("/sys/class/thermal/thermal_zone1/temp")
            temp = int(tFile.read()) / 1000
            tFile.close()
            return [temp]
        if self.i == 1:
            try:
                while 1:  
                    address(0)               # "Spueladresse anlegen"
                    GPIO.output(DATA,1);     # Data auf 1 fuer Spuelen setzen
                    enable()                 # Data auf Adresse uebenehmen
                    print "adr: %d - %d" % (0,1)
                    time.sleep(0.6)            # 60 Sekunden spuelen
                    GPIO.output(DATA,0);     # Spuelvorgang beenden
                    enable()                 # Data auf Adresse uebenehmen
                    print "adr: %d - %d" % (0,0)
                    address(adr)             # "Spueladresse anlegen"
                    GPIO.output(DATA,1);     # Data auf 1
                    enable()                 # Data auf Adresse uebenehmen
                    print "adr: %d - %d" % (adr,1)
                    time.sleep(3)          # 60 Sekunden warten, 240 Sekunden Messen
                    GPIO.output(DATA,0);     # Data auf 0
                    enable()                 # Data auf Adresse uebenehmen
                    print "adr: %d - %d" % (adr,0)
                
                    adr+=1
                    return adr
                
                    if(adr>15):
                        adr=1
            except KeyboardInterrupt:
                pass
            finally:
                GPIO.cleanup() 
           
   


# Dauerschleife
# adr=1   # Adresse reserviert 0 fuer Spuelen
# 
# while 1:  
#     #address(0)               # "Spueladresse anlegen"
#     #GPIO.output(DATA,1);     # Data auf 1 fuer Spuelen setzen
#     #enable()                 # Data auf Adresse uebenehmen
#     print "adr: %d - %d" % (0,1)
#     time.sleep(60)            # 60 Sekunden spuelen
#     #GPIO.output(DATA,0);     # Spuelvorgang beenden
#     #enable()                 # Data auf Adresse uebenehmen
#     print "adr: %d - %d" % (0,0)
#     #address(adr)             # "Spueladresse anlegen"
#     #GPIO.output(DATA,1);     # Data auf 1
#     #enable()                 # Data auf Adresse uebenehmen
#     print "adr: %d - %d" % (adr,1)
#     time.sleep(300)           # 60 Sekunden warten, 240 Sekunden Messen
#     #GPIO.output(DATA,0);     # Data auf 0
#     #enable()                 # Data auf Adresse uebenehmen
#     print "adr: %d - %d" % (adr,0)
# 
#     adr+=1
# 
#     if(adr>15):
#         adr=1


#myClient = RasperryPi(names, options)
#myClient.run()