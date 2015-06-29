import ConfigParser
from bayeosgatewayclient import BayEOSGatewayClient
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

class RaspberryPi(BayEOSGatewayClient):
    """Raspberry Pi class."""
    
    def __init__(self, names, options1={}, defaults1={}, config_file="../config/bayeosraspberrypi.ini"):
        BayEOSGatewayClient.__init__(self, names, options1, defaults1)
        self.names = names
        self.config_file = os.path.join(os.path.split(__file__)[0], config_file)
        self.read_config(self.config_file)
        self.init_sensors()
        # RPi.GPIO Layout verwenden (wie Pin-Nummern)
        GPIO.setmode(GPIO.BOARD)
        # PINS
        self.ADR = [11, 12, 13, 15, 16, 18] # GPIO 17, 18, 27, 22, 23, 24
        self.DATA = 24 # GPIO 8
        self.EN = 26   # GPIO 7
        try:
            # ADR Output setzen
            for pin in self.ADR:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
     
            GPIO.setup(self.EN, GPIO.OUT)
            GPIO.output(self.EN, GPIO.LOW)
     
            GPIO.setup(self.DATA, GPIO.OUT)
            GPIO.output(self.DATA, GPIO.LOW)     
        except KeyboardInterrupt:
            GPIO.cleanup() 
    
    def readData(self):
        if self.i == 0:
            return (randint(-1, 1), 3, 4)
        return 0    
        
    def enable(self):
        """ Funktion enable: Setzt kurz den Enable Pin und DATA wird in die 
            gesetzte Adresse uebernommen."""
        GPIO.output(self.EN,GPIO.HIGH);
        print "EN is high"
        # time.sleep(0.0001);
        GPIO.output(self.EN,GPIO.LOW);
        print "EN is low"
        
    def address(self, a):
        for i in range(0,6): # ADR[0]=11, ADR[1]=12...
            GPIO.output(self.ADR[i],((1<<i) & a)) # binary shift to left (2^i) and 
            # print str(ADR[i]) + ": " + str((1<<i) & a)
            # Bsp.: a = 3
            # Pin 11 = 1
            # Pin 12 = 2, alle anderen 0

#     
#     # Dauerschleife fuer jeweils 60 s spuelen, 300 s messen
#     adr=1   # Adresse reserviert 0 fuer Spuelen
        
    def init_sensors(self):
        try:
            self.i2c = I2C()
            self.sht21 = SHT21(1)
            self.mcp3424 = MCP3424(self.i2c.get_smbus())
        except IOError, e:
            print "I2C Connection Error :" + str(e) + ". This must be run as root. Did you use the right device number?"
        
    def measure(self, seconds=10):
        measured_seconds = []
        temp = []
        hum = []
        co2 = []
        for i in range(0,seconds):
            temp.append(self.sht21.read_temperature())
            hum.append(self.sht21.read_humidity())
            co2.append(self.mcp3424.read_voltage(1))
            measured_seconds.append(i)
            sleep(1)
        mean_temp = numpy.mean(temp)
        var_temp = numpy.var(temp)    
        mean_hum = numpy.mean(hum)
        var_hum = numpy.var(hum)
        slope, intercept, r_value, p_value, std_err = stats.linregress(measured_seconds,co2)
        print "Mean temp.: " + str(mean_temp) + " Variance: " + str(var_temp)
        print "Mean humidity: " + str(mean_hum) + " Variance: " + str(var_hum)
        print "Slope: " + str(slope)
    
    def read_config(self, config_file):
        config = ConfigParser.ConfigParser()
        try:
            config.read(config_file)
            if not config.has_option('Special', 'names'):
                for i in range(0, len(config.get('Special', 'host').split(','))):
                    names = {}
                    names[i] = 'IP' + config.get('Special', 'host').split(',')[i]
            else:
                names = config.get('Special', 'names').split(', ')
            
            if not config.has_option('Sender', 'sender'):
                config.set('Sender', 'sender', names)
        except ConfigParser.NoSectionError as e:
            print "Error: " + str(e) + "Config File (.ini) not found or with missing values."        
        
        self.options = {}
        for section in config.sections():
            for key, val in config.items(section):
                self.options[key] = val
                

co2_chambers = ['Kammer_1']
                
test = RaspberryPi(co2_chambers)
print test.options

print test.measure(3)

test.run()


# class RasperryPi(BayEOSGatewayClient):
#     
#     def readData(self):
#         if self.i == 0:
#             tFile = open("/sys/class/thermal/thermal_zone1/temp")
#             temp = int(tFile.read()) / 1000
#             tFile.close()
#             return [temp]
#         if self.i == 1:
#             try:
#                 while 1:  
#                     address(0)               # "Spueladresse anlegen"
#                     GPIO.output(DATA,1);     # Data auf 1 fuer Spuelen setzen
#                     enable()                 # Data auf Adresse uebenehmen
#                     print "adr: %d - %d" % (0,1)
#                     time.sleep(0.6)            # 60 Sekunden spuelen
#                     GPIO.output(DATA,0);     # Spuelvorgang beenden
#                     enable()                 # Data auf Adresse uebenehmen
#                     print "adr: %d - %d" % (0,0)
#                     address(adr)             # "Spueladresse anlegen"
#                     GPIO.output(DATA,1);     # Data auf 1
#                     enable()                 # Data auf Adresse uebenehmen
#                     print "adr: %d - %d" % (adr,1)
#                     time.sleep(3)          # 60 Sekunden warten, 240 Sekunden Messen
#                     GPIO.output(DATA,0);     # Data auf 0
#                     enable()                 # Data auf Adresse uebenehmen
#                     print "adr: %d - %d" % (adr,0)
#                 
#                     adr+=1
#                     return adr
#                 
#                     if(adr>15):
#                         adr=1
#             except KeyboardInterrupt:
#                 pass
#             finally:
#                 GPIO.cleanup() 
#            
#    
# 
# 
# # Dauerschleife
# # adr=1   # Adresse reserviert 0 fuer Spuelen
# # 
# # while 1:  
# #     #address(0)               # "Spueladresse anlegen"
# #     #GPIO.output(DATA,1);     # Data auf 1 fuer Spuelen setzen
# #     #enable()                 # Data auf Adresse uebenehmen
# #     print "adr: %d - %d" % (0,1)
# #     time.sleep(60)            # 60 Sekunden spuelen
# #     #GPIO.output(DATA,0);     # Spuelvorgang beenden
# #     #enable()                 # Data auf Adresse uebenehmen
# #     print "adr: %d - %d" % (0,0)
# #     #address(adr)             # "Spueladresse anlegen"
# #     #GPIO.output(DATA,1);     # Data auf 1
# #     #enable()                 # Data auf Adresse uebenehmen
# #     print "adr: %d - %d" % (adr,1)
# #     time.sleep(300)           # 60 Sekunden warten, 240 Sekunden Messen
# #     #GPIO.output(DATA,0);     # Data auf 0
# #     #enable()                 # Data auf Adresse uebenehmen
# #     print "adr: %d - %d" % (adr,0)
# # 
# #     adr+=1
# # 
# #     if(adr>15):
# #         adr=1
# 
# 
# #myClient = RasperryPi(names, options)
# #myClient.run()