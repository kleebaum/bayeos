import ConfigParser
from bayeosgatewayclient import BayEOSGatewayClient, BayEOSWriter, BayEOSSender
from random import randint
import time
from time import sleep
import os
import RPi.GPIO as GPIO
from i2c import I2C
from sht21 import SHT21
from mcp3424 import MCP3424
import numpy # apt-get install python-numpy
from scipy import stats # apt-get install python-scipy
from thread import start_new_thread

# GPIO helper methods
def enable():
    """ Funktion enable: Setzt kurz den Enable Pin und DATA wird in die 
        gesetzte Adresse uebernommen."""
    GPIO.output(EN,GPIO.HIGH);
    print "EN is high"
    # time.sleep(0.0001);
    GPIO.output(EN,GPIO.LOW);
    print "EN is low"
    
def address(a):
    for i in range(0,6): # ADR[0]=11, ADR[1]=12...
        GPIO.output(ADR[i],((1<<i) & a))

# constant variables
PATH = '/tmp/raspberrypi/'
ADR = [11, 12, 13, 15, 16, 18] # GPIO 17, 18, 27, 22, 23, 24
DATA = 24 # GPIO 8
EN = 26   # GPIO 7

# create BayEOSSender thread
def samplesender():    
    """Creates an example sender."""
    NAME = 'RaspberryPi'
    URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
    sender = BayEOSSender(PATH, NAME, URL, 'bayeos', 'root')

    while True:
        res = sender.send()
        if res > 0:
            print 'Successfully sent ' + str(res) + ' post requests.\n'
        sleep(5)
        
start_new_thread(samplesender, ())

# instantiate object of BayEOSWriter Class
writer = BayEOSWriter(PATH)

# init GPIO board
GPIO.setmode(GPIO.BOARD)
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


# init sensors
try:
    i2c = I2C()
    sht21 = SHT21(1)
    mcp3424 = MCP3424(i2c.get_smbus())
except IOError, e:
    print "I2C Connection Error :" + str(e) + ". This must be run as root. Did you use the right device number?"

# measurement loop
adr=1   # Adresse reserviert 0 fuer Spuelen

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
        writer.save_msg(message="Test", origin="RaspberryPi Kammer Nr. " + str(adr))
        print "adr: %d - %d" % (adr,1)
        time.sleep(3)          # 60 Sekunden warten, 240 Sekunden Messen
        GPIO.output(DATA,0);     # Data auf 0
        enable()                 # Data auf Adresse uebenehmen
        print "adr: %d - %d" % (adr,0)
     
        adr+=1
     
        if(adr>15):
            adr=1
except KeyboardInterrupt as err:
    print 'Error: ' + str(err)
finally:
    GPIO.cleanup() 
