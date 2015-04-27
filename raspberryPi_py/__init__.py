import ConfigParser
from bayeos_gateway.bayeosGatewayClient import isset, BayEOSGatewayClient

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
    
print names
  
class RasperryPi(BayEOSGatewayClient):
    
    def readData(self):
        return BayEOSGatewayClient.readData(self)
    
myClient = RasperryPi(names)
#myClient.run()