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


class RasperryPi(BayEOSGatewayClient):
    
    def readData(self):
        return (randint(-1,1), 3, 4)
   
    
myClient = RasperryPi(names, options)
myClient.run()