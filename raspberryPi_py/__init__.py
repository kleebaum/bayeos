import ConfigParser
from bayeos_gateway.bayeosGatewayClient import BayEOSGatewayClient
from random import randint

def isset(var):
    return var in locals() or var in globals()

config = ConfigParser.ConfigParser()
config.read("raspberryPi.ini")

if not config.has_option('Special', 'names'):
    for i in range(0, len(config.get('Special', 'host').split(','))):
        names = {}
        names[i] = 'IP' + config.get('Special', 'host').split(',')[i]
else:
    names = config.get('Special', 'names').split(', ')
    
if not config.has_option('Sender', 'sender'):
    config.set('Sender', 'sender', names)

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
   
    
myClient = RasperryPi(names, options)
myClient.run()