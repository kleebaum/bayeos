from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from time import sleep
from i2c import I2C
from sht21 import SHT21
from mcp3424 import MCP3424
import sys, numpy  # apt-get install python-numpy
from scipy import stats  # apt-get install python-scipy
from thread import start_new_thread
from gpio import GPIO

# gpio pins
ADDR_PINS = [11, 12, 13, 15, 16, 18]  # GPIO 17, 18, 27, 22, 23, 24
DATA_PIN = 24  # GPIO 8
EN_PIN = 26  # GPIO 7

# configuration for BayEOSWriter and BayEOSSender
PATH = '/tmp/raspberrypi/'
NAME = 'RaspberryPi'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

# instantiate objects of BayEOSWriter and BayEOSSender
writer = BayEOSWriter(PATH)
sender = BayEOSSender(PATH, NAME, URL)

# initialize GPIO Boardon Raspberry Pi
gpio = GPIO(ADDR_PINS, EN_PIN, DATA_PIN)

# initialize I2C Bus with sensors
try:
    i2c = I2C()
    sht21 = SHT21(1)
    mcp3424 = MCP3424(i2c.get_smbus())
except IOError as err:
    sys.stderr.write('I2C Connection Error: ' + str(err) + '. This must be run as root. Did you use the right device number?')

# measurement method
def measure(self, seconds=10):
    measured_seconds = []
    temp = []
    hum = []
    co2 = []
    for i in range(0, seconds):
        temp.append(sht21.read_temperature())
        hum.append(sht21.read_humidity())
        co2.append(mcp3424.read_voltage(1))
        measured_seconds.append(i)
        sleep(1)
    mean_temp = numpy.mean(temp)
    var_temp = numpy.var(temp)
    mean_hum = numpy.mean(hum)
    var_hum = numpy.var(hum)
    slope, intercept, r_value, p_value, std_err = stats.linregress(measured_seconds, co2)
    # print "Mean temp.: " + str(mean_temp) + " Variance: " + str(var_temp)
    # print "Mean humidity: " + str(mean_hum) + " Variance: " + str(var_hum)
    # print "Slope: " + str(slope)
    return [mean_temp, var_temp, mean_hum, var_hum, slope, intercept]

start_new_thread(sender.run, (5,))


while True:
    for addr in range(0, 15):   # address 0 is reserved for flushing with air
        gpio.set_addr(0)        # set flushing address
        sleep(0.6)              # flush for 60 seconds
        gpio.reset()            # stop flushing

        gpio.set_addr(addr)     # start measuring wait 60 seconds, 240 measure
        writer.save(measure(seconds=3), origin="RaspberryPi Kammer Nr. " + str(addr))
        writer.flush()
        gpio.reset()

gpio.cleanup()
