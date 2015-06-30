"""bayeosgatewayclient"""

import os, time, datetime, string, urllib, urllib2, base64, glob, tempfile, re
from posix import chdir, rename
from struct import pack, unpack
from _socket import gethostname
from time import sleep

class BayEOSFrame:
    """Implementation of BayEOS Frame Protocol Specification."""
    global DATA_TYPES, FRAME_TYPES

    def create_data_frame(self, values=[], value_type=0x1, offset=0):
        """
        Creates a BayEOS Data Frame.
        @param values: list with [channel index, value] tuples
        @param value_type: defines Offset and Data Types
        @param offset: length of Channel Offset (if Offset Type is 0x0)
        @return Data Frame as a binary String
        """
        value_type = int(value_type)
        frame = pack('b', value_type)
        offset_type = (0xf0 & value_type)  # first four bits of the Value Type
        data_type = (0x0f & value_type)  # last four bits of the Value Type
        val_format = DATA_TYPES[data_type]['format']  # search DATA_TYPES Dictionary

        if offset_type == 0x0:  # Data Frame with channel offset
            frame += pack('b', offset)  # 1 byte channel offset

        try:
            for [key, each_value] in values:
                if offset_type == 0x4:  # Data Frame with channel indices
                    frame += pack('b', key)
                frame += pack(val_format, each_value)
        except TypeError:
            for each_value in values:  # simple Data Frame, Offset Type is 0x2
                frame += pack(val_format, each_value)
        return frame

    def create_command_frame(self, cmd_type, cmd):
        """
        Creates a BayEOS Command or Command Response Frame.
        @param cmd_type: type of command
        @param cmd: instruction for or response from receiver
        """
        return pack('b', cmd_type) + cmd

    def create_message_frame(self, string):
        """
        Creates a BayEOS Message or Error Message Frame.
        @param string: message to save
        """
        return string

    def create_routed_frame(self, my_id, pan_id, frame, rssi=''):
        """
        Creates a BayEOS Routed or a BayEOS Routed RSSI Frame.
        @param my_id: TX-XBee MyId
        @param pan_id: XBee PANID
        @param rssi: RSSI
        @param frame: must be a valid BayEOS Frame
        """
        ids = pack('h', my_id) + pack('h', pan_id)
        if rssi:
            return  ids + pack('b', rssi) + frame
        return ids + frame

    def create_origin_frame(self, origin, frame):
        """
        Saves Origin Frame.
        @param origin: name to appear in the gateway
        @param frame: must be a valid BayEOS frame
        """
        origin = origin[0:255]
        return pack('b', len(origin)) + origin + frame

    DATA_TYPES = {0x1 : {'format' : 'f', 'valueLength' : 4},  # float32 4 bytes
                  0x2 : {'format' : 'i', 'valueLength' : 4},  # int32 4 bytes
                  0x3 : {'format' : 'h', 'valueLength' : 2},  # int16 2 bytes
                  0x4 : {'format' : 'b', 'valueLength' : 1},  # int8 1 byte
                  0x5 : {'format' : 'd', 'valueLength' : 8}}  # double 8 bytes

    FRAME_TYPES = {0x1: {'name' : 'Data Frame',
                         'create' : create_data_frame,
                         'variables' : ['values', 'value_type', 'offset']},
                   0x2: {'name' : 'Command',
                         'create' : create_command_frame,
                         'variables' : ['cmd_type', 'cmd']},
                   0x3: {'name' : 'Command Response',
                         'create' : create_command_frame,
                         'variables' : ['cmd_type', 'cmd']},
                   0x4: {'name' : 'Message',
                         'create' : create_message_frame,
                         'variables' : ['string']},
                   0x5: {'name' : 'Error Message',
                         'create' : create_message_frame,
                         'variables' : ['string']},
                   0x6: {'name' : 'Routed Frame',
                         'create' : create_routed_frame,
                         'variables' : ['my_id', 'pan_id', 'frame']},
                   0x7: {'name' : 'Delayed Frame'},
                   0x8: {'name' : 'Routed RSSI Frame',
                         'create' : create_routed_frame,
                         'variables' : ['my_id', 'pan_id', 'frame', 'rssi']},
                   0x9: {'name' : 'Timestamp Frame'},
                   0xa: {'name' : 'Binary'},
                   0xb: {'name' : 'Origin Frame',
                         'create' : create_origin_frame,
                         'variables' : ['origin', 'frame']},
                   0xc: {'name' : 'Timestamp Frame'}}

    def __init__(self, values=[], value_type=0x1, 
                 offset=0, ts=0, frame_type=0x1, origin='', string='', my_id='', 
                 pan_id='', frame='', rssi='', cmd_type='', cmd=''):
        #self.frame_type = frame_type
        #self.name = FRAME_TYPES[frame_type]['name']
        
        # only initialize needed variables
        variables = {}
        try:
            for each_var in FRAME_TYPES[frame_type]['variables']:
                setattr(self, each_var, eval(each_var))
                variables[str(each_var)] = eval(each_var)
        except NameError as err:
            print "Error: " + str(err)
        
        # create frame
        self.bin = pack('b', frame_type) + FRAME_TYPES[frame_type]['create'](self, **variables)
        
    def to_string(self):
        """Prints a readable form of the BayEOS Frame."""
        #frame = {}
        #frame['name'] = self.name
        #frame['type'] = self.frame_type
        #frame['value'] = self.parse_frame(self.bin)
        #for each_var in FRAME_TYPES[self.frame_type]['variables']:
        #        setattr(self, each_var, eval(each_var))
        print self.parse_frame(self.bin)

    @classmethod
    def parse_frame(self, frame, ts=False, origin='', rssi=False):
        """
        Parses a binary coded BayEOS Frame into a Python dictionary.
        @param frame (binary coded String)
        @param ts
        @param origin
        @param rssi
        @return array
        """
        if not ts:
            ts = time.time()
        frameType = unpack('=b', frame[0:1])[0]
        res = {}
        res['type'] = FRAME_TYPES[frameType]['name']
        if frameType == 0x1:
            res['value'] = self.parse_data_frame(frame)
        elif frameType == 0x2:
            res['cmd'] = unpack('=b', frame[1:2])[0]
            res['value'] = frame[2:]
        elif frameType == 0x3:
            res['cmd'] = unpack('=b', frame[1:2])[0]
            res['value'] = frame[2:]
        elif frameType == 0x4:
            res['value'] = frame[1:]
        elif frameType == 0x5:
            res['value'] = frame[1:]
        elif frameType == 0xa:
            res['pos'] = unpack('=f', frame[1:5])[0]
            res['value'] = frame[5:]
        elif frameType == 0xc:
            ts = unpack('=d', frame[1:9])[0]
            return self.parse_frame(frame[9:], ts, origin, rssi)
        else:
            res['value'] = frame
        if ts:
            res['ts'] = ts
        if origin:
            res['origin'] = origin
        if rssi:
            res['rssi'] = rssi
        return res
    
    @classmethod
    def parse_data_frame(self, frame):
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
        val_format = DATA_TYPES[dataType]['format']
        vl = DATA_TYPES[dataType]['valueLength']
        pos = 2
        key = 0
        res = {}
        if offsetType == 0x0:
            key = unpack('=b', frame[2:3])[0]  # offset
            pos += 1
        while pos < len(frame):
            if offsetType == 0x40:
                key = unpack('=b', frame[pos:pos + 1])[0]
                pos += 1
            else:
                key += 1
            value = unpack('=' + val_format, frame[pos:pos + vl])[0]
            pos += vl
            res[key] = value
        return res

class BayEOSWriter:
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
                print 'OSError: ' + str(e)
        chdir(self.path)
        files = glob.glob('*')
        for eachFile in files:
            if string.find(eachFile, '.act'):  # Rename active file
                rename(eachFile, eachFile.replace('.act', '.rd'))
        self.__start_new_file()
        #self.bayeos = BayEOSFrame()

#     def saveDataFrame(self, values, valueType=0x1, offset=0, ts=0):
#         """
#         Writes a Data Frame to the buffer.
#         @param values: array for values
#         @param valueType: defines Offset and Data Types
#         @param offset: offset parameter for BayEOS data frames (relevant for some types)
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(self.bayeos.createDataFrame(values, valueType, offset), ts)
#
#     def saveCommandFrame(self, cmdType, command, ts=0):
#         """
#         Saves Command Frame.
#         @param cmdType: type of command
#         @param command: instruction for receiver
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x2) + pack('b', cmdType) + command, ts)
#
#     def saveCommandResponseFrame(self, cmdType, commandRes, ts=0):
#         """
#         Saves Command Response Frame.
#         @param cmdType: type of command
#         @param commandRes: response of receiver
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x3) + pack('b', cmdType) + commandRes, ts)
#
#     def saveMessage(self, string, ts=0):
#         """
#         Saves message.
#         @param sting: message to save
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x4) + string, ts)
#
#     def saveErrorMessage(self, string, ts=0):
#         """
#         Saves error message.
#         @param sting: message to save
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x5) + string, ts)
#
#     def saveRoutedFrame(self, myId, panId, frame, ts=0):
#         """
#         Saves routed frame.
#         @param myId: TX-XBee MyId
#         @param panId: XBee PANID
#         @param frame: must be a valid BayEOS frame
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x6) + pack('h', myId) + pack('h', panId) + frame, ts)
#
#     def saveRoutedFrameRSSI(self, myId, panId, rssi, frame, ts=0):
#         """
#         Saves routed frame RSSI.
#         @param myId: TX-XBee MyId
#         @param panId: XBee PANID
#         @param rssi: RSSI
#         @param frame: must be a valid BayEOS frame
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         self.saveFrame(pack('b', 0x8) +
#                        pack('h', myId) +
#                        pack('h', panId) +
#                        pack('b', rssi) +
#                        frame, ts)
#
#     def saveOriginFrame(self, origin, frame, ts=0):
#         """
#         Saves Origin Frame.
#         @param origin: name to appear in the gateway
#         @param frame: must be a valid BayEOS frame
#         @param ts: Unix epoch time stamp, if zero system time is used
#         """
#         origin = origin[0:255]
#         self.saveFrame(pack('b', 0xb) + pack('b', len(origin)) + origin + frame, ts)

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
            self.__start_new_file()

    def __start_new_file(self):
        """Opens a new file with ending .act and determines current file name."""
        self.currentTs = time.time()
        [sec, usec] = string.split(str(self.currentTs), '.')
        self.currentName = sec + '-' + usec
        self.fp = open(self.currentName + '.act', 'wb')

    def save(self, values, value_type=0x1, offset=0, ts=0, origin=''):
        """Generic frame saving method."""
        data_frame = BayEOSFrame(values, value_type, offset)
        if not origin:
            self.saveFrame(data_frame.bin, ts)
        else:
            origin_frame = BayEOSFrame(frame_type=0xb, origin=origin, frame=data_frame.bin)
            self.saveFrame(origin_frame.bin, ts)
            print "Origin Frame saved."

class BayEOSSender:
    def __init__(self, path, name, url, pw, user='import',
                 absoluteTime=True, rm=True, gatewayVersion='1.9'):
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
        self.ref = time.time() - (datetime.datetime(2000, 1, 1) -
                                  datetime.datetime(1970, 1, 1)).total_seconds()

    def send(self):
        """
        Keeps sending until all files are sent or an error occurs.
        @return number of post requests as an integer
        """
        count = 0
        post = self.sendFile()
        while post:
            count += post
            post = self.sendFile()
        return count

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
        fp = open(files[0], 'rb')  # opens oldest file
        data = '&sender=' + urllib.quote_plus(self.name)
        frames = ''
        count = 0
        ts = fp.read(self.lengthOfDouble)
        while ts:  # until end of file
            ts = unpack('=d', ts)[0]
            frameLength = unpack('=h', fp.read(self.lengthOfShort))[0]
            frame = fp.read(frameLength)
            if frame:
                count += 1
                if self.absoluteTime:  # Timestamp Frame
                    if self.gatewayVersion == '1.8':  # second resolution from 2000-01-01
                        timestampFrame = pack('b', 0x9) + pack('l', round(ts - self.ref)) + frame
                    else:  # millisecond resolution from 1970-01-01
                        timestampFrame = pack('b', 0xc) + pack('q', round(ts * 1000)) + frame
                else:  # Delayed Frame
                    timestampFrame = pack('b', 0x7) + pack('l',
                                                           round((time.time() - ts) * 1000)) + frame
                frames += '&bayeosframes[]=' + base64.urlsafe_b64encode(timestampFrame)
            ts = fp.read(self.lengthOfDouble)
        fp.close()
        if frames:  # content found for post request
            res = self.post(data + frames)
            if res == 1:
                if self.rm:
                    os.remove(files[0])
                else:
                    rename(files[0], files[0].replace('.rd', '.bak'))
            elif res == 0:
                rename(files[0], files[0].replace('.rd', '.bak'))
                exit('Error posting. File will be kept as ' + str(files[0].replace('.rd', '.bak')))
            return count
        else:  # empty file
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
        except urllib2.URLError as e:
            exit('URLError: ' + str(e))
        return 0

class BayEOSGatewayClient:

    def __init__(self, names, options1={}, defaults1={}):
        """
        Creates an instance of BayEOSGatewayClient.
        @param names: name dictionary e.g. 'Fifo.0', 'Fifo.1'...
        Name is used for storage directory e.g. /tmp/Fifo.0.
        @param options: dictionary of options. Three forms are possible.
        """
        if not isinstance(names, list):
            names = names.split(', ')
        if len(set(names)) < len(names):
            exit('Duplicate names detected.')
        if len(names) == 0:
            exit('No name given.')

        prefix = ''
        try:
            options1['sender']
            if isinstance(options1['sender'], list):
                options1['sender'] = '_'.join(options1['sender'])
            if len(names) > 1:
                prefix = options1['sender'] + '/'
                del options1['sender']

        except KeyError:
            prefix = gethostname() + '/'  # use hostname if no sender specified
        print prefix
        senderDefaults = {}
        for i in range(0, len(names)):
            senderDefaults[i] = prefix + names[i]

        defaults = {'writer_sleep_time' : 15,
                    'max_chunk' : 5000,
                    'max_time' : 60,
                    'data_type' : 0x1,
                    'sender_sleep_time' : 5,
                    'sender' : senderDefaults,
                    'bayeosgateway_user' : 'import',
                    'bayeosgateway_version' : '1.9',
                    'absolute_time' : True,
                    'rm' : True,
                    'sleep_between_children' : 0,
                    'tmp_dir' : tempfile.gettempdir()}
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
        if isinstance(self.options[key], dict):
            try:
                self.options[key][self.i]
            except AttributeError or KeyError:
                return default
            return self.options[key][self.i]
        return self.options[key]

    def run(self):
        """
        Runs the BayEOSGatewayClient. Forks one BayEOSWrite and one BayEOSSender per name.
        """
        for i in range(0, len(self.names)):
            self.i = i
            self.name = self.names[i]
            path = self.getOption('tmp_dir') + '/' + re.sub('[-]+|[/]+|[\\\\]+|["]+|[\']+',
                                                            '_', self.name)
            self.pid_w[i] = os.fork()
            if self.pid_w[i] == -1:
                exit("Could not fork writer process!")
            elif self.pid_w[i]:  # Parent
                print "Started writer"
            else:  # Child
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
            elif self.pid_r[i]:  # Parent
                print "Started sender"
                sleep(self.getOption('sleep_between_children'))
            else:  # Child
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
                        print 'Successfully sent ' + str(res) + ' frames.\n'
                    sleep(self.getOption('sender_sleep_time'))
                exit()


    def initWriter(self):
        """
        Method called by run(). Can be overwritten by implementation.
        """
        pass

    def readData(self):
        """
        Method called by run(). Must be overwritten by implementation.
        """
        exit("No readData() found! Method has to be implemented.\n")
        return False

    def saveData(self, data, origin=''):
        """
        Method called by run(). Can be overwritten by implementation (e.g. to store routed frames).
        """
        self.writer.save(data, self.getOption('data_type'), origin=origin)
