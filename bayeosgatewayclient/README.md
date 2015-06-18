# bayeosgatewayclient
A generic Python module to transfer client (sensor) data to a BayEOS Gateway.

## Installation
You can use either the setup.py script, pip or a Linux binary to install the package.

### Setup.py
Do the following steps to install the package via the setup.py script:
- git clone request ```git clone git://github.com/kleebaum/bayeos.git```
- find the right directory ```cd bayeos/bayeosgatewayclient```
- run ```python setup.py install``` as root

### PIP

### Linux Binary
#### Debian
- Add the following repositories to /etc/apt/sources.list ```deb http://www.bayceer.uni-bayreuth.de/edv/debian wheezy/```
- run ```apt-get update```
- install the Debian gateway client package ```apt-get install bayeosgatewayclient```

Alternatively:
- run ```dpkg -i python-bayeosgatewayclient_0.1-1_all.deb``` as root

### Arch Linux
coming soon

## Example usage
- import the module ```import bayeosgatewayclient```

### Example writer
Run the method ```bayeosgatewayclient.samplewriter()``` to see how the BayEOSWriter class is instantiated.

This is how it works:
```
from time import sleep
from bayeosgatewayclient import BayEOSWriter

PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 100)

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], valueType=0x02, offset=2)
    writer.saveMessage("This is a message.")
    writer.saveErrorMessage("This is an error message.")
    sleep(1)
```

