from struct import *
import pycurl
import time
import urllib.parse
import base64

""" First writer methods """

""" creates a new BayEOS data frame including values given as a list """
def createDataFrame(values, type=0x1, offset=0):
    bayeosFrame = pack('bb', 0x1, type)
    # print('Frame start: ', bayeosFrame)
    offsetType = (0xf0 & type)
    # print('Offset type: ', offsetType)
    dataType = (0x0f & type)
    # print('Data type: ', dataType)    
    if offsetType == 0x0:
        bayeosFrame += pack('b', offset)
        # print('Frame with offset: ', bayeosFrame)        
    for each_value in values:
        bayeosFrame += pack('f', each_value)
    # print('Value frame created: ', bayeosFrame)
    return(bayeosFrame)
    
""" writes a data frame to file according to a time stamp """
def saveDataFrame(values, type=0x1, offset=0, ts=0):
    tmpDir = '/home/anja/tmp/bayeos-device1'
    bayeosFrame = createDataFrame(values, type, offset)
    if not ts:
        ts = time.time()
    bayeosFrameHeaderTs = pack('d', ts)
    # print('Time stamp (binary): ', bayeosFrameHeaderTs)
    bayeosFrameHeaderLength = pack('h', len(bayeosFrame))
    # print('Frame length (decimal): ', len(bayeosFrame))
    # print('Frame length (binary): ', bayeosFrameHeaderLength)
    bayeosWriterFrame = bayeosFrameHeaderTs + bayeosFrameHeaderLength + bayeosFrame
    currentName = tmpDir + '/'+ str(time.time()) + '.rd'
    print('File created: ', currentName)
    f = open(currentName, 'wb')    
    f.write(bayeosWriterFrame)
    f.close()
    sendFile(bayeosFrameHeaderTs, bayeosFrameHeaderLength, bayeosFrame)
    # print('Frame with header (binary): ', bayeosWriterFrame)
    print('Frame with header (decimal): ', toString(bayeosWriterFrame, header=True))

""" unpacks the BayEOS data frame """
def toString(bayeosFrame, header=False):
    frameLength = len(bayeosFrame)
    # print('Frame length: ', frameLength)
    if header == True:
        valueLength = (frameLength - 13) / 4
        fmt = '=dhbbb'        
    else:
        valueLength = (frameLength - 3) / 4        
        fmt = '=bbb'
        
    # print('Number of Values: ', valueLength)
    for i in range(0, int(valueLength)):
        fmt += 'f'
    return(unpack(fmt, bayeosFrame))

def sendFile(ts, length, data):
    name = 'Python-Test-Device'
    pw = 'xbee'
    gatewayVersion = '1.9'
    curl = pycurl.Curl()
    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.TIMEOUT, 120)
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.HEADER, 1)
    curl.setopt(pycurl.USERAGENT, 'BayEOS-PHP/1.0.8')
    curl.setopt(pycurl.NOBODY, 1)
    curl.setopt(pycurl.URL, 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat')
    curl.setopt(pycurl.USERPWD, 'admin:xbee')
    print(pack('Q',round(unpack('=d', ts)[0]*1000)))
    ts = pack('Q',round(unpack('=d', ts)[0]*1000))
    data = pack("b",0xc)+ts+data
    print(data)
    data2="sender="+urllib.parse.quote_plus(name)+"&password="+urllib.parse.quote_plus(pw)+"&bayeosframes[]="+urllib.parse.quote_plus(str(base64.standard_b64encode(data)))
    print(data2)
    curl.setopt(pycurl.POSTFIELDS, data2)
    #curl.setopt(pycurl.RETURNTRANSFER, 1)
    curl.perform()
    
#     $tmp=fread($fp,$size_of_double);
#             if(strlen($tmp)==0) break;
#             $tmp=unpack('d',$tmp);
#             $ts=$tmp[1];
#             $tmp=unpack('s',fread($fp,$size_of_short));
#             $length=$tmp[1];
#             $bayeos_frame=fread($fp,$length);
#             if($bayeos_frame){
#                 $count++;
#                 if($this->absolute_time){
#                     if($this->gateway_version=='1.8') $bayeos_frame=pack("C",0x9).BayEOSType::UINT32(round($ts-$ref)).$bayeos_frame;
#                     else $bayeos_frame=pack("C",0xc).BayEOSType::UINT64(round($ts*1000)).$bayeos_frame;
#                 }else
#                     $bayeos_frame=pack("C",0x7).BayEOSType::UINT32(round((microtime(TRUE)-$ts)*1000)).$bayeos_frame;
#                 $frames.="&bayeosframes[]=".($this->gateway_version=='1.8'?
#                         base64_encode($bayeos_frame):urlencode(base64_encode($bayeos_frame)));
#             }

