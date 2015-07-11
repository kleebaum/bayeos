"""bayeosgatewayclient"""
import os, string, urllib, urllib2, base64, tempfile, re
from posix import chdir, rename
from struct import pack, unpack
from _socket import gethostname
from time import sleep, time
from glob import glob
from bayeosframe import BayEOSFrame#, FRAME_NAMES

# Frame Types of BayEOS Frames
ORIGIN = 0xb #FRAME_NAMES['Origin Frame']
MSG = 0x4 #FRAME_NAMES['Message Frame']
ERR_MSG = 0x5 #FRAME_NAMES['Error Message Frame']

# Length
LENGTH_OF_DOUBLE = 8
LENGTH_OF_SHORT = 2

class BayEOSWriter(object):
    """Writes BayEOSFrames to file."""
    def __init__(self, path, max_chunk=2500, max_time=60):
        """Constructor for a BayEOSWriter instance.
        @param path: path of queue directory
        @param max_chunk: maximum file size in Bytes, when reached a new file is started
        @param max_time: maximum time when a new file is started
        """
        self.path = path
        self.max_chunk = max_chunk
        self.max_time = max_time
        if not os.path.isdir(self.path):
            try:
                os.mkdir(self.path, 0700)
            except OSError as err:
                print 'OSError: ' + str(err)
                exit()
        chdir(self.path)
        files = glob('*')
        for each_file in files:
            if string.find(each_file, '.act'):  # Rename old active file
                rename(each_file, each_file.replace('.act', '.rd'))
        self.__start_new_file()

    def __save_frame(self, frame, timestamp=0):
        """Saves frames to file.
        @param frame: must be a valid BayEOS Frame as a binary coded String
        @param timestamp: Unix epoch time stamp, if zero system time is used
        """
        if not timestamp:
            timestamp = time()
        self.file.write(pack('<d', timestamp) + pack('<h', len(frame)) + frame)
        if self.file.tell() >= self.max_chunk or time() - self.current_timestamp >= self.max_time:
            self.file.close()
            rename(self.current_name + '.act', self.current_name + '.rd')
            self.__start_new_file()

    def __start_new_file(self):
        """Opens a new file with ending .act and determines current file name."""
        self.current_timestamp = time()
        [sec, usec] = string.split(str(self.current_timestamp), '.')
        self.current_name = sec + '-' + usec
        self.file = open(self.current_name + '.act', 'wb')

    def save(self, values, value_type=0x1, offset=0, timestamp=0, origin=None):
        """Generic frame saving method.
        @param values: list with [channel index, value] tuples or just values (..,..) or [..,..]
        @param value_type: defines Offset and Data Type
        @param offset: defines Channel Offset
        @param timestamp: Unix epoch time stamp, if zero system time is used
        @param origin: if defined, it is used as a name
        """
        data_frame = BayEOSFrame.factory()
        data_frame.create(values, value_type, offset)
        if not origin:
            self.__save_frame(data_frame.frame, timestamp)
        else:
            origin_frame = BayEOSFrame.factory(ORIGIN)
            origin_frame.create(origin=origin, nested_frame=data_frame.frame)
            self.__save_frame(origin_frame.frame, timestamp)
            print 'Origin Frame saved.'

    def save_msg(self, message, error=False, timestamp=0, origin=None):
        """Saves Messages or Error Messages to Gateway.
        @param message: String to send
        @param error: when true, an Error Message is sent
        @param timestamp: Unix epoch time stamp, if zero system time is used
        """
        msg_frame = BayEOSFrame.factory(MSG)
        if error:
            msg_frame = BayEOSFrame.factory(ERR_MSG)
        msg_frame.create(message)
        if not origin:
            self.__save_frame(msg_frame.frame, timestamp)
        else:
            origin_frame = BayEOSFrame.factory(ORIGIN)
            origin_frame.create(origin=origin, nested_frame=msg_frame.frame)
            self.__save_frame(origin_frame.frame, timestamp)
            print 'Origin Frame saved.'
            
    def flush(self):
        """Close the current used file and renames it from .act to .rd.
        Starts a new file.
        """
        self.save_msg('Flushed writer.')
        self.file.close()
        rename(self.current_name + '.act', self.current_name + '.rd')
        self.__start_new_file()
        

class BayEOSSender(object):
    """Sends content of BayEOS writer files to Gateway."""
    def __init__(self, path, name, url, password='', user='import',
                 absolute_time=True, remove=True, gateway_version='1.9'):
        """Constructor for BayEOSSender instance.
        @param path: path where BayEOSWriter puts files
        @param name: sender name
        @param url: gateway url e.g. http://<gateway>/gateway/frame/saveFlat
        @param password: password on gateway
        @param user: user on gateway
        @param absolute_time: if set to false, relative time is used (delay)
        @param remove: if set to false files are kept as .bak file in the BayEOSWriter directory
        @param gateway_version: gateway version
        """
        if not password:
            exit('No gateway password was found.')
        self.path = path
        self.name = name
        self.url = url
        self.password = password
        self.user = user
        self.absolute_time = absolute_time
        self.remove = remove
        self.gateway_version = gateway_version

    def send(self):
        """Keeps sending until all files are sent or an error occurs.
        @return number of post requests (i.e. posted frames) as an integer
        """
        count_frames = 0
        post = self.__send_file()
        while post:
            count_frames += post
            post = self.__send_file()
        return count_frames

    def __send_file(self):
        """Reads one file from queue and tries to send it to the gateway.
        On success the file is deleted or renamed to *.bak ending.
        Always the oldest file is used.
        @return number of post requests as an integer
        """
        try:
            chdir(self.path)
        except OSError as err:
            exit('OSError: ' + str(err) + '. Start BayEOSWriter first.')
        files = glob('*.rd')
        if len(files) == 0:
            return 0
        current_file = open(files[0], 'rb')  # opens oldest file
        post_request = '&sender=' + urllib.quote_plus(self.name)
        frames = ''
        count_frames = 0
        timestamp = current_file.read(LENGTH_OF_DOUBLE)
        while timestamp:  # until end of file
            timestamp = unpack('<d', timestamp)[0]
            frame_length = unpack('<h', current_file.read(LENGTH_OF_SHORT))[0]
            frame = current_file.read(frame_length)
            if frame:
                count_frames += 1
                if self.absolute_time:  # Timestamp Frame
                    if self.gateway_version == '1.8':  # second resolution from 2000-01-01
                        timestamp_frame = BayEOSFrame.factory(0x9)
                        timestamp_frame.create(frame, timestamp)
                    else:  # millisecond resolution from 1970-01-01
                        timestamp_frame = BayEOSFrame.factory(0xc)
                        timestamp_frame.create(frame, timestamp)
                else:  # Delayed Frame
                    timestamp_frame = BayEOSFrame.factory(0x7)
                    timestamp_frame.create(frame, timestamp)
                frames += '&bayeosframes[]=' + base64.urlsafe_b64encode(timestamp_frame.frame)
            timestamp = current_file.read(LENGTH_OF_DOUBLE)
        current_file.close()
        if frames:  # content found for post request
            res = self.__post(post_request + frames)
            if res == 1:
                if self.remove:
                    os.remove(files[0])
                else:
                    rename(files[0], files[0].replace('.rd', '.bak'))
            elif res == 0:
                rename(files[0], files[0].replace('.rd', '.bak'))
                exit('Error posting. File will be kept as ' + str(files[0].replace('.rd', '.bak')))
            return count_frames
        else:  # empty file
            if os.stat(files[0]).st_size:
                rename(files[0], files[0].replace('.rd', '.bak'))
            else:
                os.remove(files[0])
        return 0

    def __post(self, post_request):
        """Posts frames to gateway.
        @param post_request: query string for HTML POST request
        @return success (1) or failure (0)
        """
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, self.url, self.user, self.password)
        handler = urllib2.HTTPBasicAuthHandler(password_manager)
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(self.url, post_request)
        req.add_header('Accept', 'text/html')
        req.add_header('User-Agent', 'BayEOS-Python-Gateway-Client/1.0.0')
        try:
            opener.open(req)
            return 1
        except urllib2.HTTPError as err:
            if err.code == 401:
                exit('Authentication failed.\n')
            elif err.code == 404:
                exit('URL ' + self.url + ' is invalid.\n')
            else:
                exit('Post error: ' + str(err) + '.\n')
        except urllib2.URLError as err:
            exit('URLError: ' + str(err))
        return 0
    
    def run(self, sleep_sec):
        """Tries to send frames within a certain interval.
        @param sleep_sec: specifies the sleep time
        """
        while True:
            res = self.send()
            if res > 0:
                print 'Successfully sent ' + str(res) + ' frames.\n'
            sleep(sleep_sec)

class BayEOSGatewayClient(object):
    """Combines writer and sender for every device."""

    def __init__(self, names, options1={}, defaults1={}):
        """Creates an instance of BayEOSGatewayClient.
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
        """Helper function to get an option value.
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
        """Runs the BayEOSGatewayClient. Forks one BayEOSWrite and one BayEOSSender per name."""
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
                                      self.getOption('bayeosgateway_password'),
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
