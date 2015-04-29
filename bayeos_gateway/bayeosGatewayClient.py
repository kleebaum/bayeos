import os, time, datetime, string, urllib, urllib2, base64, glob, tempfile, re
from posix import chdir, rename
from struct import pack, unpack
from _socket import gethostname
from time import sleep

class BayEOS():
    def createDataFrame(self, values, valueType=0x1, offset=0):
        """
        Creates a BayEOS Data Frame.
        @param values: list with [channel index, value] tuples
        @param valueType: defines Offset and Data Types
        @param offset: length of Channel Offset (if Offset Type is 0x0)
        @return Data Frame as a binary string
        """
        frame = pack('bb', 0x1, valueType)          # 0x1 represents data frame 
        offsetType = (0xf0 & valueType)             # first four bits of frame type
        dataType = (0x0f & valueType)               # last four bits of frame type    
        if offsetType == 0x0:                       # data frame with channel offset
                frame += pack('b', offset)          # 1 byte channel offset
        
        for [key, each_value] in values:
            if offsetType == 0x40:                  # data frame with channel indices
                frame += pack('b', key)
            if dataType == 0x1:                     # float32 4 bytes
                frame += pack('f', each_value)
            elif dataType == 0x2:                   # int32 4 bytes
                frame += pack('i', each_value)   
            elif dataType == 0x3:                   # int16 2 bytes
                frame += pack('h', each_value)  
            elif dataType == 0x4:                   # int8 1 byte
                frame += pack('b', each_value)  
            elif dataType == 0x5:                   # double 8 bytes
                frame += pack('d', each_value)  
                    
        return(frame)
            
    def parseFrame(self, frame, ts=False, origin='', rssi=False):
        """
        Parses a binary coded BayEOS Frame into a Python dictionary.
        @param frame
        @param ts
        @param origin
        @param rssi
        @return array
        """
        if not ts:
            ts = time.time()
        frameType = unpack('=b', frame[0:1])[0]
        res = {}
        if frameType == 0x1:
            res['type'] = 'DataFrame'
            res['value'] = self.parseDataFrame(frame)
        elif frameType == 0x2:
            res['type'] = 'Command'
            res['cmd'] = unpack('=b', frame[1:2])[0]
            res['value'] = frame[2:]
        elif frameType == 0x3:
            res['type'] = 'CommandResponse'
            res['cmd'] = unpack('=b', frame[1:2])[0]
            res['value'] = frame[2:]
        elif frameType == 0x4:
            res['type'] = 'Message'
            res['value'] = frame[1:]
        elif frameType == 0x5:
            res['type'] = 'ErrorMessage'
            res['value'] = frame[1:]
        elif frameType == 0x6:
            res['type'] = 'RoutedFrame'
            
        elif frameType == 0x7:
            res['type'] = 'DelayedFrame'
        elif frameType == 0x8:
            res['type'] = 'RoutedFrameRSSI'
        elif frameType == 0x9:
            res['type'] = 'TimestampFrame'
            #ts 
        elif frameType == 0xa:
            res['type'] = 'Binary'
            res['pos'] = unpack('=f', frame[1:5])[0]
            res['value'] = frame[5:]
        elif frameType == 0xb:
            res['type'] = 'OriginFrame'
        elif frameType == 0xc:
            res['type'] = 'TimestampFrame'
            ts = unpack('=d', frame[1:9])[0]
            return self.parseFrame(frame[9:], ts, origin, rssi)
        else:
            res['type'] = 'Unknown'
            res['value'] = frame
        if ts:
            res['ts'] = ts
        if origin:
            res['origin'] = origin
        if rssi:
            res['rssi'] = rssi
        return(res)
            
    def parseDataFrame(self, frame):
        """
        Parses a binary coded BayEOS Data Frame into a Python dictionary.
        @param frame: binary coded BayEOS Data Frame
        @return unpacked tuples of channel indices and values
        """
        if unpack('=b', frame[0:1])[0] != 0x1:
            return False
        valueType = unpack('=b', frame[1:2])[0]
        offsetType = 0xf0 & valueType
        dataType = 0x0f & valueType
        pos = 2
        key = 0
        res = {}
        if offsetType == 0x0:
            key = unpack('=b', frame[2:3])[0] # offset
            pos += 1
        while(pos < len(frame)):
            if offsetType == 0x40:
                key = unpack('=b', frame[pos:pos+1])[0]
                pos += 1
            else:
                key += 1
            if dataType == 0x1:
                value = unpack('=f', frame[pos:pos+4])[0]
                pos += 4
            elif dataType == 0x2:
                value = unpack('=i', frame[pos:pos+4])[0]
                pos += 4 
            elif dataType == 0x3:
                value = unpack('=h', frame[pos:pos+2])[0]
                pos += 2   
            elif dataType == 0x4:
                value = unpack('=b', frame[pos:pos+1])[0]
                pos += 1   
            elif dataType == 0x5:
                value = unpack('=d', frame[pos:pos+4])[0]
                pos += 8      
            res[key] = value
        return res        
    
class BayEOSWriter():
    def __init__(self, path, maxChunk=5000, maxTime=60):
        """ 
        Constructor for a BayEOSWriter instance.
        @param path: path of queue directory
        @param maxChunk: maximum file size when a new file is started
        @param maxTime: maximum time when a new file is started
        """
        self.path = path
        self.maxChunk = maxChunk
        self.maxTime = maxTime
        if not os.path.isdir(self.path):
            try:
                os.mkdir(self.path, 0700)
            except OSError as e:
                print('OSError: ' + str(e))                
        chdir(self.path)
        files = glob.glob('*')
        for eachFile in files:
            if string.find(eachFile, '.act'):    # Rename active file 
                rename(eachFile, eachFile.replace('.act', '.rd'))
        self.startNewFile()
        self.bayeos = BayEOS()
        
    def saveDataFrame(self, values, valueType=0x1, offset=0, ts=0):
        """
        Writes a Data Frame to the buffer.
        @param values: array for values
        @param valueType: defines Offset and Data Types
        @param offset: offset parameter for BayEOS data frames (relevant for some types)
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(self.bayeos.createDataFrame(values, valueType, offset), ts)
    
    def saveCommandFrame(self, cmdType, command, ts=0):
        """
        Saves Command Frame.
        @param cmdType: type of command
        @param command: instruction for receiver
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x2) + pack('b', cmdType) + command, ts)  
        
    def saveCommandResponseFrame(self, cmdType, commandRes, ts=0):
        """
        Saves Command Response Frame.
        @param cmdType: type of command
        @param commandRes: response of receiver
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x3) + pack('b', cmdType) + commandRes, ts)    
        
    def saveMessage(self, string, ts=0):
        """
        Saves message.
        @param sting: message to save
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x4) + string, ts)
        
    def saveErrorMessage(self, string, ts=0):
        """
        Saves error message.
        @param sting: message to save
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x5) + string, ts)         
        
    def saveRoutedFrame(self, myId, panId, frame, ts=0):
        """
        Saves routed frame.
        @param myId: TX-XBee MyId
        @param panId: XBee PANID
        @param frame: must be a valid BayEOS frame
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x6) + pack('h', myId) + pack('h', panId) + frame, ts)

    def saveRoutedFrameRSSI(self, myId, panId, rssi, frame, ts=0):
        """
        Saves routed frame RSSI.
        @param myId: TX-XBee MyId
        @param panId: XBee PANID
        @param rssi: RSSI
        @param frame: must be a valid BayEOS frame
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(pack('b', 0x8) + pack('h', myId) + pack('h', panId) + pack('b', rssi) + frame, ts)     

    def saveOriginFrame(self, origin, frame, ts=0):
        """
        Saves Origin Frame.
        @param origin: name to appear in the gateway
        @param frame: must be a valid BayEOS frame
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        origin = origin[0:255]
        self.saveFrame(pack('b', 0xb) + pack('b', len(origin)) + origin + frame, ts)

    def saveFrame(self, frame, ts=0):
        """Save Timestamp Frame to file. This is a base function.
        @param frame: must be a valid BayEOS Frame
        @param ts: Unix epoch time stamp, if zero system time is used 
        """
        if not ts:
            ts = time.time()
        self.fp.write(pack('d', ts) + pack('h', len(frame)) + frame)
        if self.fp.tell() > self.maxChunk or time.time() - self.currentTs > self.maxTime:
            self.fp.close()
            rename(self.currentName + '.act', self.currentName + '.rd')
            self.startNewFile()
    
    def startNewFile(self):
        """ Opens a new file with ending .act and determines current file name. """ 
        self.currentTs = time.time()
        [sec, usec] = string.split(str(self.currentTs), '.')
        self.currentName = sec + '-' + usec
        self.fp = open(self.currentName + '.act', 'wb')
    
    def save(self, values, valueType=0x1, offset=0, ts=0, origin=''):
        """ Generic frame saving method. """ 
        if not origin:
            self.saveDataFrame(values, valueType, offset, ts)
        else:     
            dataFrame = self.bayeos.createDataFrame(values, valueType, offset)       
            self.saveOriginFrame(origin, dataFrame, ts)
        
class BayEOSSender():
    def __init__(self, path, name, url, pw, user='import', absoluteTime=True, rm=True, gatewayVersion='1.9'):
        """
        Constructor for BayEOSSender instance.
        @param path: path where BayEOSWriter puts files
        @param name: sender name
        @param url: gateway url e.g. http://<gateway>/gateway/frame/saveFlat
        @param pw: password on gateway
        @param user: user on gateway
        @param absoluteTime: if set to false, relative time is used (delay)
        @param rm: if set to false files are kept as .bak file in the BayEOSWriter directory
        @param gatewayVersion: gateway version
        """
        if not pw:
            exit("No gateway password was found.\n")
        self.path = path
        self.name = name
        self.url = url
        self.pw = pw
        self.user = user
        self.absoluteTime = absoluteTime
        self.rm = rm
        self.gatewayVersion = gatewayVersion
        self.lengthOfDouble = len(pack('d', time.time()))
        self.lengthOfShort = len(pack('h', 1))
        self.ref = time.time()-(datetime.datetime(2000,1,1)-datetime.datetime(1970,1,1)).total_seconds()
    
    def send(self):
        """
        Keeps sending until all files are sent or an error occurs.
        @return number of post requests as an integer
        """
        count = 0
        post = self.sendFile()
        while(post):
            count += post
            post = self.sendFile()
        return(count)
    
    def sendFile(self):
        """
        Reads one file from queue and tries to send it to the gateway.
        On success file is deleted or renamed to *.bak ending.
        Always the oldest file is used.
        @return number of post requests as an integer
        """
        chdir(self.path)
        files = glob.glob('*.rd')
        if len(files) == 0:
            return 0
        fp = open(files[0], 'rb')       # opens oldest file
        data = '&sender=' + urllib.quote_plus(self.name)
        frames = ''
        count = 0
        ts = fp.read(self.lengthOfDouble)
        while ts:                       # until end of file
            ts = unpack('=d', ts)[0]
            frameLength = unpack('=h', fp.read(self.lengthOfShort))[0]
            frame = fp.read(frameLength)
            if frame:
                count += 1
                if self.absoluteTime:   # Timestamp Frame
                    if self.gatewayVersion == '1.8':    # second resolution from 2000-01-01
                        timestampFrame = pack('b', 0x9) + pack('l', round(ts - self.ref)) + frame
                    else:                               # millisecond resolution from 1970-01-01
                        timestampFrame = pack('b', 0xc) + pack('q', round(ts * 1000)) + frame
                else:                   # Delayed Frame
                    timestampFrame = pack('b', 0x7) + pack('l', round((time.time() - ts) * 1000)) + frame
                frames += '&bayeosframes[]=' + base64.urlsafe_b64encode(timestampFrame)
            ts = fp.read(self.lengthOfDouble)
        fp.close()
        if frames:              # content found for post request
            res = self.post(data + frames)
            if res == 1:
                if self.rm:
                    os.remove(files[0])
                else:
                    rename(files[0], files[0].replace('.rd', '.bak'))
            elif res == 0:
                rename(files[0], files[0].replace('.rd', '.bak'))
                exit('Error posting. File will be kept as ' + str(files[0].replace('.rd', '.bak')))
            return(count)
        else:                           # empty file
            if os.stat(files[0]).st_size:
                rename(files[0], files[0].replace('.rd', '.bak'))
            else:
                os.remove(files[0])
        return 0
        
    def post(self, data):
        """
        Posts frames to gateway.
        @param postData
        @return success (1) or failure (0)
        """
        passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordManager.add_password(None, self.url, self.user, self.pw)
        handler = urllib2.HTTPBasicAuthHandler(passwordManager)
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(self.url, data)
        req.add_header('Accept', 'text/html')
        req.add_header('User-Agent', 'BayEOS-Python-Gateway-Client/1.0.0')
        try:
            opener.open(req)
            return 1
        except urllib2.HTTPError as e:
            if e.code == 401:
                exit('Authentication failed.\n')    
            elif e.code == 404:
                exit('URL ' + self.url + ' is invalid.\n')  
            else:
                exit('Post error: ' + str(e) + '.\n')
        return 0

class BayEOSGatewayClient():

    def __init__(self, names, options1={}, defaults1={}):
        """
        Creates an instance of BayEOSGatewayClient.
        @param names: name dictionary e.g. 'Fifo.0', 'Fifo.1'...
        Name is used for storage directory e.g. /tmp/Fifo.0.
        @param options: dictionary of options. Three forms are possible.
        """
        print names
        if len(set(names)) < len(names):
            exit('Duplicate names detected.')
        if len(names) == 0:
            exit('No name given.')

        prefix = ''
        if not 'sender' in options1:
            prefix = gethostname() + '/'
        elif not isarray(options1['sender']) and len(names) > 1:
            prefix = options1['sender'] + '/'
            del options1['sender']
        for i in range(0, len(names)):
            senderDefaults = {}
            senderDefaults[i] = prefix + names[i]
            
        defaults = {'writer_sleep_time' : 20,
                    'max_chunk' : 5000,
                    'max_time' : 60,
                    'data_type' : 0x1,
                    'sender_sleep_time' : 15,
                    #'sender' : senderDefaults,
                    'sender' : 'anja',
                    'bayeosgateway_user' : 'import',
                    'bayeosgateway_version' : '1.9',
                    'absolute_time' : True,
                    'rm' : True,
                    'tmp_dir' : tempfile.gettempdir()
                    }
        defaults.update(defaults1)
        options = {}
        
        for default in defaults.items():
            try:
                options1[default[0]]
            except KeyError:
                print "Option '" + default[0] + "' not set using default: " + str(default[1])
                options[default[0]] = default[1]            
        
        options.update(options1)
        
        self.names = names
        self.options = options
        self.pid_w = {}
        self.pid_r = {}
    
    def getOption(self, key, default=''):
        """
        Helper function to get an option value.
        @param key
        @param default
        @return Value of the specified option key as a string.
        """
        try:
            self.options[key]
        except KeyError:
            return default
        finally:
            return self.options[key]
#             if isarray(self.options[key]):
#                 if isset(self.options[key][self.i]):
#                     return self.options[key][self.i]
#                 if isset(self.options[key][self.name]):
#                     return self.options[key][self.name]
        
    def run(self):
        """
        Runs the BayEOSGatewayClient. Forks one BayEOSWrite and one BayEOSSender per name.
        """
        for i in range(0, len(self.names)):
            self.i = i
            self.nameTmp = self.names[i]
            path = self.getOption('tmp_dir') + '/' + re.sub('[-]+|[/]+|[\\\\]+|["]+|[\']+', '_', self.nameTmp)
            self.pid_w[i] = os.fork()
            if self.pid_w[i] == -1:
                exit("Could not fork writer process!")
            elif self.pid_w[i]:     # Parent
                print "Started writer"
            else:                   # Child
                self.initWriter()
                self.writer = BayEOSWriter(path, 
                                           self.getOption('max_chunk'), 
                                           self.getOption('max_time'))
                while True:
                    data = self.readData()
                    if data:
                        self.saveData(data)
                    else:
                        print "readData failed"
                        sleep(self.getOption('writer_sleep_time'))
                exit()
                
            self.pid_r[i] = os.fork()
            if self.pid_r[i] == -1:
                exit("Could not fork sender process!")
            elif self.pid_r[i]:     # Parent
                print "Started sender"
                #sleep(self.getOption('sleep_between_childs'))
            else:                   # Child
                sender = BayEOSSender(path, 
                                      self.getOption('sender'), 
                                      self.getOption('bayeosgateway_url'),
                                      self.getOption('bayeosgateway_pw'),
                                      self.getOption('bayeosgateway_user'),
                                      self.getOption('absolute_time'),
                                      self.getOption('rm'),
                                      self.getOption('bayeosgateway_version'))
                
                while True:
                    res = sender.send()
                    if res > 0:
                        print ('Successfully sent ' + str(res) + ' frames.\n')
                    sleep(self.getOption('sender_sleep_time'))  
                exit()                 

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
        self.writer.saveDataFrame(data, self.getOption('data_type'))  
    
def isset(var):
    return var in locals() or var in globals()

def isarray(var):
    return isinstance(var, (list, tuple))

