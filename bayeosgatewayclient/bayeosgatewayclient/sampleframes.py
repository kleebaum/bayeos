"""Creates example BayEOS Frames."""

from bayeosframe import BayEOSFrame
from bayeosframe import DataFrame
# Data Frames
#data_frame_simple = BayEOSFrame(values=(2,4), value_type=0x22)
data_frame_simple = BayEOSFrame.factory(0x1)
print data_frame_simple.create([2,4])
#print data_frame_simple.parse()
#print data_frame_simple.name

test = BayEOSFrame.to_object(data_frame_simple.frame)
print test.create([2,3])
print test.parse()
test.to_string()

command_frame = BayEOSFrame.factory(0x3)
command_frame.create(1, "cmd")
print command_frame.parse()
#command_frame.create(1, "test")
#command_frame.frame_type=2
#print command_frame.frame_type
# print data_frame_simple.name



# print "Values: " + str(data_frame_simple.values)
# print "Value Type: " + str(data_frame_simple.value_type)
# data_frame_simple.to_string()

# data_frame_offset = BayEOSFrame([2,4], value_type=0x01, offset=2)
# data_frame_offset.to_string()
# 
# # Message Frames
# message_frame = BayEOSFrame(frame_type=0x4, string="This is an important message.")
# print "Message: " + message_frame.string
# message_frame.to_string()
#  
# error_message_frame = BayEOSFrame(frame_type=0x5, string="This is an ERROR message.")
# error_message_frame.to_string()
#  
# # Origin Frame
# origin_frame = BayEOSFrame(frame_type=0xb, origin="My Origin", frame=data_frame_simple.bin)
# print "Origin: " + origin_frame.origin
# print "Nested frame: " + str(BayEOSFrame.parse_frame(origin_frame.frame))
# origin_frame.to_string()
# 
# # Binary Frame
# binary_frame = BayEOSFrame(frame_type=0xa, string="This a message to be packed as binary data.")
# binary_frame.to_string()
# 
# # Command Frame
# command_frame = BayEOSFrame(frame_type=0x2, cmd="test", cmd_type=0x1)