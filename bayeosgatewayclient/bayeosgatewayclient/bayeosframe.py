"""Implementation of BayEOS Frame Protocol Specification."""

from struct import pack, unpack
import time

DATA_TYPES = {0x1 : {'format' : 'f', 'length' : 4},  # float32 4 bytes
              0x2 : {'format' : 'i', 'length' : 4},  # int32 4 bytes
              0x3 : {'format' : 'h', 'length' : 2},  # int16 2 bytes
              0x4 : {'format' : 'b', 'length' : 1},  # int8 1 byte
              0x5 : {'format' : 'd', 'length' : 8}}  # double 8 bytes

FRAME_TYPES = {0x1: {'name' : 'Data Frame'},
               0x2: {'name' : 'Command Frame'},
               0x3: {'name' : 'Command Response Frame'},
               0x4: {'name' : 'Message'},
               0x5: {'name' : 'Error Message'},
               0x6: {'name' : 'Routed Frame'},
               0x7: {'name' : 'Delayed Frame'},
               0x8: {'name' : 'Routed RSSI Frame'},
               0x9: {'name' : 'Timestamp Frame'},
               0xa: {'name' : 'Binary'},
               0xb: {'name' : 'Origin Frame'},
               0xc: {'name' : 'Timestamp Frame'}}    

class BayEOSFrame(object):
    """Factory Class for BayEOS Frames."""

    @staticmethod
    def factory(frame_type=0x1):
        try:
            if frame_type == 0x1 : return DataFrame(frame_type)
            if frame_type == 0x2 : return CommandFrame(frame_type)
            if frame_type == 0x3 : return CommandFrame(frame_type)
            if frame_type == 0x4 : return MessageFrame(frame_type)
            if frame_type == 0x5 : return MessageFrame(frame_type)
            if frame_type == 0x6 : return RoutedFrame(frame_type)
            if frame_type == 0x7 : return DelayedFrame(frame_type)
            if frame_type == 0x8 : return RoutedRSSIFrame(frame_type)
            if frame_type == 0x9 : return TimestampFrame(frame_type)
            if frame_type == 0xa : return BinaryFrame(frame_type)
            if frame_type == 0xb : return OriginFrame(frame_type)
            if frame_type == 0xc : return TimestampFrame(frame_type)
        except KeyError as err:
            print "Frame Type " + str(err) + " not found."
    
    def bin_to_frame(self, frame):
        """Initializes a BayEOSFrame object from a binary coded frame."""
        BayEOSFrame(bin=frame)
    
    @staticmethod
    def parse_frame(frame):
        """Parses a binary coded BayEOS Frame into a Python dictionary.
        @param frame (binary coded String)
        @return Python dictionary
        """
        frame_type = unpack('=b', frame[0:1])[0]        
        parse_result = {'type' : FRAME_TYPES[frame_type]['name']}
        parse_result.update(FRAME_TYPES[frame_type]['parse'](frame))
        return parse_result 

    def __init__(self, frame_type=0x1):
        #self.frame_type = frame_type
        #self.name = FRAME_TYPES[frame_type]['name']
        
        # only initialize needed variables
#         variables = {}
#         try:
#             for each_var in FRAME_TYPES[frame_type]['variables']:
#                 setattr(self, each_var, eval(each_var))
#                 variables[str(each_var)] = eval(each_var)
#         except NameError as err:
#             print "Error: " + str(err)
        
        # create binary Frame Type
        self.frame = pack('b', frame_type) 
        
    def to_string(self):
        """Prints a readable form of the BayEOS Frame."""
        #frame = {}
        #frame['name'] = self.name
        #frame['type'] = self.frame_type
        #frame['value'] = self.parse_frame(self.bin)
        #for each_var in FRAME_TYPES[self.frame_type]['variables']:
        #        setattr(self, each_var, eval(each_var))
        print self.parse_frame(self.frame)
        
class DataFrame(BayEOSFrame):    
    def create(self, values=[], value_type=0x1, offset=0):
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
        self.frame += frame
    
    def parse(self):
        """
        Parses a binary coded BayEOS Data Frame into a Python dictionary.
        @param frame: binary coded BayEOS Data Frame
        @return unpacked tuples of channel indices and values
        """
        if unpack('=b', self.frame[0:1])[0] != 0x1:
            print "This is not a Data Frame."
            return False
        value_type = unpack('=b', self.frame[1:2])[0]
        offset_type = 0xf0 & value_type
        data_type = 0x0f & value_type
        val_format = DATA_TYPES[data_type]['format']
        val_length = DATA_TYPES[data_type]['length']
        pos = 2
        key = 0
        payload = {}
        if offset_type == 0x0:
            key = unpack('=b', self.frame[2:3])[0]  # offset
            pos += 1
        while pos < len(self.frame):
            if offset_type == 0x40:
                key = unpack('=b', self.frame[pos:pos + 1])[0]
                pos += 1
            else:
                key += 1
            value = unpack('=' + val_format, self.frame[pos:pos + val_length])[0]
            pos += val_length
            payload[key] = value
        return {'values' : payload}
    
class CommandFrame(BayEOSFrame):
    def create(self, cmd_type, cmd):
        """
        Creates a BayEOS Command or Command Response Frame.
        @param cmd_type: type of command
        @param cmd: instruction for or response from receiver
        """
        self.frame += pack('b', cmd_type) + cmd
    
    def parse(self):
        return {'cmd' : unpack('=b', self.frame[1:2])[0],
                'value' : self.frame[2:]}
    
class MessageFrame(BayEOSFrame):
    def create(self, string):
        """
        Creates a BayEOS Message or Error Message Frame.
        @param string: message to save
        """
        self.frame += string
    
    def parse(self):
        return {'value' : self.frame[1:]}

class RoutedFrame(BayEOSFrame):
    def create(self, my_id, pan_id, frame, rssi=''):
        """
        Creates a BayEOS Routed or a BayEOS Routed RSSI Frame.
        @param my_id: TX-XBee MyId
        @param pan_id: XBee PANID
        @param rssi: RSSI
        @param frame: must be a valid BayEOS Frame
        """
        ids = pack('h', my_id) + pack('h', pan_id)
        if rssi:
            self.frame += ids + pack('b', rssi) + frame
        self.frame += ids + frame

    def parse(self):
        nested_frame = super().parse_frame(self.frame[5:])
        return {'my_id' : unpack('=h', self.frame[1:3])[0],
                'pan_id' : unpack('=h', self.frame[3:5])[0],
                'nested_frame' : nested_frame}
    

        
class RoutedRSSIFrame(BayEOSFrame):
    def create(self, my_id, pan_id, frame, rssi=''):
        """
        Creates a BayEOS Routed or a BayEOS Routed RSSI Frame.
        @param my_id: TX-XBee MyId
        @param pan_id: XBee PANID
        @param rssi: RSSI
        @param frame: must be a valid BayEOS Frame
        """
        ids = pack('h', my_id) + pack('h', pan_id)
        if rssi:
            self.frame += ids + pack('b', rssi) + frame
        self.frame += ids + frame

    def parse(self):
        nested_frame = super().parse_frame(self.frame[6:])
        return {'my_id' : unpack('=h', self.frame[1:3])[0],
                'pan_id' : unpack('=h', self.frame[3:5])[0],
                'rssi' : unpack('=b', self.frame[5:6])[0],
                'nested_frame' : nested_frame}
    
class DelayedFrame(BayEOSFrame):
    def create(self, frame):
        ts = 1
        return pack('l',round((time.time() - ts) * 1000)) + frame
    
class OriginFrame(BayEOSFrame):
    def create(self, origin, frame):
        """
        Saves Origin Frame.
        @param origin: name to appear in the gateway
        @param frame: must be a valid BayEOS frame
        """
        origin = origin[0:255]
        return pack('b', len(origin)) + origin + frame
    
    def parse(self):
        length = unpack('=b', self.frame[1:2])[0]
        nested_frame = BayEOSFrame.parse_frame(self.frame[length+2:])
        return {'origin' : self.frame[2:length+2],
                'nested' : nested_frame}
        
class BinaryFrame(BayEOSFrame):
    def create(self, string):
        """
        Creates a BayEOS Frame including a binary coded String
        @param: string: message to pack
        """
        length = len(string)
        return pack('f', length) + pack(str(length) + 's', string)
    
    def parse(self):
        return {'pos' : unpack('=f', self.frame[1:5])[0],
                'value' : self.frame[5:]}
    
class TimestampFrame(BayEOSFrame):
    def create_timestamp_frame_sec(self, frame):
        ts=1
        timestampFrame = pack('b', 0x9) + pack('l', round(ts - self.ref)) + frame
        return pack('l', ) + frame
    
    def create_timestamp_frame(self, frame):
        ts=1
        return pack('q', round(ts * 1000)) + frame
    
    @staticmethod
    def parse_timestamp_frame_sec(frame):
        return {'ts' : unpack('=d', frame[1:9])[0]}
                #, self.parse_frame(frame[9:], ts, origin, rssi)
        
    @staticmethod
    def parse_timestamp_frame(frame):
        return {'ts' : unpack('=d', frame[1:9])[0]}
                #, self.parse_frame(frame[9:], ts, origin, rssi)    