#  Demo to show a simple MQTT subscriber to BayEOS Gateway bridge
#  Oliver Archner
#  29.07.2015

from bayeosgatewayclient import BayEOSWriter, BayEOSSender
import paho.mqtt.client as mqtt

# BayEOS sender
sender = BayEOSSender(url='http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat',user='root', password='bayeos')
sender.start()

# BayEOS writer
writer = BayEOSWriter()

# MQTT connect and subscribe 
def on_connect(client, userdata, rc):
    print("Connected with result code:{0}".format(rc))
    # Subscribe everything     
    client.subscribe("#")
 
# MQTT receive and save message
def on_message(client, userdata, msg):
    # Expects a payload in csv format like '1.0,2.0,3.0,4.0'
    try:
        lst = msg.payload.split(',')
        writer.save(values=[float(i) for i in lst],origin=str(msg.topic))        
    except:
        print("Failed to save message topic:{0} payload:{1}".format(msg.topic, msg.payload)) 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost')
client.loop_forever()


