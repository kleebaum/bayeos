import ConfigParser
from bayeosgatewayclient.bayeosgatewayclient import BayEOSGatewayClient
from random import randint
import time
from time import sleep
#from bayeosraspberrypi import *
import os

def isset(var):
    return var in locals() or var in globals()

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "raspberryPi.ini")

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

gpio = {15 : 0, 17 : 0, 18 : 0, 22 : 0, 23 : 0, 24 : 0, 25 : 0}
found = True

# for i in range(0, 10):    
#     for eachGpio in gpio:
#         if gpio[eachGpio] == 1:
#             gpio[eachGpio] = 0
#             found = True
#         elif found == True:
#             gpio[eachGpio] = 1
#             found = False    
#     print gpio

class RasperryPi(BayEOSGatewayClient):

    
    def readData(self):
        if self.i == 0:
            tFile = open("/sys/class/thermal/thermal_zone1/temp")
            temp = int(tFile.read()) / 1000
            tFile.close()
            return [temp]
        if self.i == 1:
            global found
            for eachGpio in gpio:
                if gpio[eachGpio] == 1:
                    gpio[eachGpio] = 0
                    found = True
                elif found == True:
                    gpio[eachGpio] = 1
                    found = False
            return gpio.items()
   


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