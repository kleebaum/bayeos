class BayEOSWriter():
    """creates a BayEOSWriter Instance"""
    
    def __init__(self, path, maxChunk=5000, maxTime=60):
        pass
        
    """writes a data frame to the buffer"""
    def saveDataFrame(self, values, type=0x1, offset=0, ts=0):
        pass

    """save origin frame"""
    def saveOriginFrame(self, origin, frame, ts=0):
        pass
    
    """save routed frame RSSI"""
    def saveRoutedFrameRSSI(self, myID, panID, rssi, frame, ts=0):
        pass
    
    """save message"""
    def saveMessage(self,string,ts=0):
        pass
        
    """save error message"""
    def saveErrorMessage(self, sting, ts=0):
        pass
    
    """save frame, base function
    @param frame must be a valid BayEOS frame
    @param ts Unix epoch time stamp, if zero system time is used 
    """
    def saveFrame(self, frame, ts=0):
        pass