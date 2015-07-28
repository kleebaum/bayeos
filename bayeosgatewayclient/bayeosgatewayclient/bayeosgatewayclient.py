"""bayeosgatewayclient"""
import os, string, urllib, urllib2, base64, re, sys
#from os import fork
from posix import chdir, rename
from tempfile import gettempdir
from struct import pack, unpack
from _socket import gethostname
from time import sleep, time
from glob import glob
from bayeosframe import BayEOSFrame
from abc import abstractmethod
from multiprocessing import Process

DEFAULTS = {'path' : gettempdir(),
            'writer_sleep_time' : 15,
            'max_chunk' : 2500,
            'max_time' : 60,
            'value_type' : 0x41,
            'sender_sleep_time' : 5,
            'bayeosgateway_user' : 'import',
            'absolute_time' : True,
            'remove' : True,
            'sleep_between_children' : 0}

class BayEOSWriter(object):
    """Writes BayEOSFrames to file."""
    def __init__(self, path=DEFAULTS['path'], max_chunk=DEFAULTS['max_chunk'],
                 max_time=DEFAULTS['max_time']):
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
                exit('OSError: ' + str(err))
        chdir(self.path)
        files = glob('*')
        for each_file in files:
            if string.find(each_file, '.act'):  # Rename old active file
                try:
                    rename(each_file, each_file.replace('.act', '.rd'))
                except OSError as err:
                    print 'OSError: ' + str(err)
        self.__start_new_file()

    def __save_frame(self, frame, timestamp=0):
        """Saves frames to file.
        @param frame: must be a valid BayEOS Frame as a binary coded String
        @param timestamp: Unix epoch time stamp, if zero system time is used
        """
        if not timestamp:
            timestamp = time()
        frame_length = len(frame)         
        if self.file.tell() + frame_length + 10 > self.max_chunk or time() - self.current_timestamp > self.max_time:
            self.file.close()
            rename(self.current_name + '.act', self.current_name + '.rd')
            self.__start_new_file()
        self.file.write(pack('<d', timestamp) + pack('<h', frame_length) + frame) 

    def __start_new_file(self):
        """Opens a new file with ending .act and determines current file name."""
        self.current_timestamp = time()
        [sec, usec] = string.split(str(self.current_timestamp), '.')
        self.current_name = sec + '-' + usec
        self.file = open(self.current_name + '.act', 'wb')

    def save(self, values, value_type=0x41, offset=0, timestamp=0, origin=None):
        """Generic frame saving method.
        @param values: list with [channel index, value] tuples or just values (..,..) or [..,..]
        @param value_type: defines Offset and Data Type
        @param offset: defines Channel Offset
        @param timestamp: Unix epoch time stamp, if zero system time is used
        @param origin: if defined, it is used as a name
        """
        data_frame = BayEOSFrame.factory(0x1)
        data_frame.create(values, value_type, offset)
        if not origin:
            self.__save_frame(data_frame.frame, timestamp)
        else:
            origin_frame = BayEOSFrame.factory(0xb)
            origin_frame.create(origin=origin, nested_frame=data_frame.frame)
            self.__save_frame(origin_frame.frame, timestamp)
            print 'Origin Frame saved.'

    def save_msg(self, message, error=False, timestamp=0, origin=None):
        """Saves Messages or Error Messages to Gateway.
        @param message: String to send
        @param error: when true, an Error Message is sent
        @param timestamp: Unix epoch time stamp, if zero system time is used
        """
        if error:
            msg_frame = BayEOSFrame.factory(0x5)  # instantiate ErrorMessage Frame
        else:
            msg_frame = BayEOSFrame.factory(0x4)  # instantiate Message Frame
        msg_frame.create(message)
        if not origin:
            self.__save_frame(msg_frame.frame, timestamp)
        else:
            origin_frame = BayEOSFrame.factory(0xb)
            origin_frame.create(origin=origin, nested_frame=msg_frame.frame)
            self.__save_frame(origin_frame.frame, timestamp)
            # print 'Origin Frame saved.'

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
    def __init__(self, path=DEFAULTS['path'], name='', url='', password='',
                 user=DEFAULTS['bayeosgateway_user'],
                 absolute_time=DEFAULTS['absolute_time'],
                 remove=DEFAULTS['remove']):
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
        timestamp = current_file.read(8)
        while timestamp:  # until end of file
            timestamp = unpack('<d', timestamp)[0]
            frame_length = unpack('<h', current_file.read(2))[0]
            frame = current_file.read(frame_length)
            if frame:
                count_frames += 1
                if self.absolute_time:  # Timestamp Frame
                    # millisecond resolution from 1970-01-01
                    wrapper_frame = BayEOSFrame.factory(0xc)
                else:  # Delayed Frame
                    wrapper_frame = BayEOSFrame.factory(0x7)
                wrapper_frame.create(frame, timestamp)
                frames += '&bayeosframes[]=' + base64.urlsafe_b64encode(wrapper_frame.frame)
            timestamp = current_file.read(8)
        current_file.close()
        if frames:  # content found for post request
            res = self.__post(post_request + frames)
            if res == 1:
                if self.remove:
                    try:
                        os.remove(files[0])
                    except OSError as err:
                        exit('OSError: ' + str(err))
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
                sys.stderr.write('Authentication failed.')
            elif err.code == 404:
                sys.stderr.write('URL ' + self.url + ' is invalid.')
            else:
                sys.stderr.write('Post error: ' + str(err))
        except urllib2.URLError as err:
            sys.stderr.write('URLError: ' + str(err))
        return 0

    def run(self, sleep_sec):
        """Tries to send frames within a certain interval.
        @param sleep_sec: specifies the sleep time
        """
        while True:
            res = self.send()
            if res > 0:
                print 'Successfully sent ' + str(res) + ' frames.'
            sleep(sleep_sec)

class BayEOSGatewayClient(object):
    """Combines writer and sender for every device."""

    def __init__(self, names, options):
        """Creates an instance of BayEOSGatewayClient.
        @param names: list of device names e.g. 'Fifo.0', 'Fifo.1', ...
        The names are used to determine storage directories e.g. /tmp/Fifo.0.
        @param options: dictionary of options.
        """
        # check whether a valid list of device names is given
        if not isinstance(names, list):
            names = names.split(', ')
        if len(set(names)) < len(names):
            exit('Duplicate names detected.')
        if len(names) == 0:
            exit('No name given.')

        # if more than one device name is given, use sender name as prefix
        prefix = ''
        try:
            if isinstance(options['sender'], list):
                exit('Sender needs to be given as a String, not a list.')
                # options['sender'] = '_'.join(options['sender'])
            if len(names) > 1:
                prefix = options['sender'] + '/'
        except KeyError:
            prefix = gethostname() + '/'  # use host name if no sender specified

        options['sender'] = {}
        for each_name in names:
            options['sender'][each_name] = prefix + each_name

        # Set missing options on default values
        for each_default in DEFAULTS.items():
            try:
                options[each_default[0]]
            except KeyError:
                print 'Option "' + each_default[0] + '" not set using default: ' + str(each_default[1])
                options[each_default[0]] = each_default[1]

        self.names = names
        self.options = options

    def __init_folder(self, name):
        """Initializes folder to save data in.
        @param name: will be the folder name
        """
        path = self.__get_option('path') + '/' + re.sub('[-]+|[/]+|[\\\\]+|["]+|[\']+', '_', name)
        if not os.path.isdir(path):
            try:
                os.mkdir(path, 0700)
            except OSError as err:
                exit('OSError: ' + str(err))
        return path

    def __get_option(self, key, default=''):
        """Helper function to get an option value.
        @param key: key in options dictionary
        @param default: default value to return if key is not specified
        @return value of the given option key or default value
        """
        try:
            self.options[key]
        except KeyError:
            return default
        if isinstance(self.options[key], dict):
            try:
                self.options[key][self.name]
            except AttributeError:
                return default
            except KeyError:
                return default
            return self.options[key][self.name]
        return self.options[key]
    
    def __start_writer(self, path):
        self.init_writer()
        self.writer = BayEOSWriter(path, self.__get_option('max_chunk'),
                                    self.__get_option('max_time'))
        self.writer.save_msg('Started writer for ' + self.name)
        while True:
            data = self.read_data()
            if data:
                self.save_data(data)
            sleep(self.__get_option('writer_sleep_time'))
            
    def __start_sender(self, path):
        self.sender = BayEOSSender(path,
                                   self.__get_option('sender'),
                                   self.__get_option('bayeosgateway_url'),
                                   self.__get_option('bayeosgateway_password'),
                                   self.__get_option('bayeosgateway_user'),
                                   self.__get_option('absolute_time'),
                                   self.__get_option('remove'))
        while True:
            self.sender.send()
            sleep(self.__get_option('sender_sleep_time'))
        

#     def run(self):
#         """Runs the BayEOSGatewayClient.
#         Forks one BayEOSWrite and one BayEOSSender per device name.
#         """
#         for each_name in self.names:
#             self.name = each_name  # will be forked and then overwritten
#             path = self.__init_folder(each_name)
#             pid_writer = fork()
#             if pid_writer > 0:  # Parent
#                 print 'Started writer for ' + each_name + ' with pid ' + str(pid_writer)
#             elif pid_writer == 0:  # Child
#                 self.__start_writer(path)
#             else:
#                 exit("Could not fork writer process!")
# 
#             pid_sender = fork()
#             if pid_sender > 0:  # Parent
#                 print 'Started sender for ' + each_name + ' with pid ' + str(pid_writer)
#             elif pid_sender == 0:  # Child
#                 self.__start_sender(path)
#             else:
#                 exit("Could not fork sender process!")
                
    def run(self):
        """Runs the BayEOSGatewayClient.
        Forks one BayEOSWrite and one BayEOSSender per device name.
        """
        for each_name in self.names:
            self.name = each_name  # will be forked and then overwritten
            path = self.__init_folder(each_name)
            process_writer = Process(target=self.__start_writer, args=(path,))
            process_writer.start()
            
            process_sender = Process(target=self.__start_sender, args=(path,))
            process_sender.start()

    @abstractmethod
    def init_writer(self):
        """Method called by run(). Can be overwritten by implementation."""
        return

    @abstractmethod
    def read_data(self):
        """Method called by run(). Must be overwritten by implementation."""
        exit("No read data method found. Method has to be implemented.")

    def save_data(self, *args):
        """Method called by run(). 
        Can be overwritten by implementation (e.g. to store message frames).
        @param *args: list of arguments for writer's save methods
        """
        self.writer.save(args[0], self.__get_option('value_type'))
