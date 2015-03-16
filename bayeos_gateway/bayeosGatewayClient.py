class BayEOSGatewayClient():
    """
    create an instance of bayeosGatewayClient
    @param names: name array e.g. 'Fifo.0', 'Fifo.1'..., used for storage directory e.g. /tmp/Fifo.0
    @param options
    """
    def __init__(self, names, options, defaults):
        pass
    
    """
    helper function to get an option value
    @param key
    @param default
    @return string: value of the specified option key
    """
    def getOption(self, key, default=''):
        pass
    
    """
    runs the BayEOSGatewayClient
    forks one BayEOSWrite and one BayEOSSender per name
    """
    def run(self):
        pass
    
    """
    method called by run()
    can be overwritten by implementation
    """
    def initWriter(self):
        pass
    
    """
    method called by run()
    must be overwritten by implementation
    """
    def readData(self):
        exit("no readData() found!\n")
        return(False)
    
    """
    method called by run()
    can be overwritten by implementation (e.g. to store routed frames)
    """    
    def saveData(self, data):
        pass
     