from struct import *
import time

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
    tmpDir = '/tmp/bayeos-device1'
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
