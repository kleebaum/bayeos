from os.path import isdir
from posix import mkdir, chdir, rename
from pathlib import Path
from bayeos import BayEOS

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
        
    """
    writes a data frame to the buffer
    @param values: array for values
    @param type: valid BayEOS data frame number
    @param offset: offset parameter for BayEOS data frames (relevant for some types)
    @param ts: Unix epoch time stamp, if zero system time is used
    """
    def saveDataFrame(self, values, type=0x1, offset=0, ts=0):
        self.saveFrame(BayEOS.createDataFrame(), ts)

    """
    save origin frame
    @param origin: name to appear in the gateway
    @param frame: must be a valid BayEOS frame
    @param ts: Unix epoch time stamp, if zero system time is used
    """
    def saveOriginFrame(self, origin, frame, ts=0):
        origin = origin[0:255]
        self.saveFrame(frame, ts)
    
    """
    save routed frame RSSI
    @param myId: TX-XBee MyId
    @param panId: XBee PANID
    @param rssi: RSSI
    @param frame: must be a valid BayEOS frame
    @param ts: Unix epoch time stamp, if zero system time is used
    """
    def saveRoutedFrameRSSI(self, myId, panId, rssi, frame, ts=0):
        self.saveFrame(frame, ts)
    
    """
    save message
    @param sting: message to save
    @param ts: Unix epoch time stamp, if zero system time is used
    """
    def saveMessage(self,sting,ts=0):
        self.saveFrame(sting, ts)
        
    """
    save error message
    @param sting: message to save
    @param ts: Unix epoch time stamp, if zero system time is used
    """
    def saveErrorMessage(self, sting, ts=0):
        self.saveFrame(sting, ts)
    
    """save frame, base function
    @param frame: must be a valid BayEOS frame
    @param ts: Unix epoch time stamp, if zero system time is used 
    """
    def saveFrame(self, frame, ts=0):
        if not ts:
            ts = 0
    
    