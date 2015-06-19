# bayeosraspberrypi
An implementation for a real BayEOS Gateway Client.

## Installation
You need to install [bayeosgatewayclient](../bayeosgatewayclient) first.

- Install the package by running ```python setup.py install``` as root

## Example
### Inheritance of BayEOSGatewayClient Class
```from bayeosgatewayclient import BayEOSGatewayClient```
Implement the abstract readData() method.


```
class RasperryPi(BayEOSGatewayClient):
    
    def readData(self):
    	pass
```