from os.path import isdir
from posix import mkdir, chdir, rename
from pathlib import Path
class BayEOSWriter():
    """
    creates a BayEOSWriter Instance
    @param path: path of queue directory
    @param maxChunk: maximum file size when a new file is started
    @param maxTime: maximum time when a new file is started
    """
    def __init__(self, path, maxChunk=5000, maxTime=60):
        self.path = path
        self.maxChunk = maxChunk
        self.maxTime = maxTime
        if not isdir(self.path):
            if not mkdir(self.path, mode=0o700):
                exit("Could not create ", self.path)
                
        chdir(self.path)
        files = Path.glob('*')
        last = files[-1]
        if str.find(last, '$', '.act$'):
            # Found active file -- unexpected shutdown
            rename(last, str.replace('.act', '.rd', last))
        #self.startNewFile
        
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
    
    