"""Creates example BayEOS Frames."""

from bayeosgatewayclient import BayEOSFrame

# Data Frames
data_frame_simple = BayEOSFrame(values=(2,4), value_type=0x22)
print "Values: " + str(data_frame_simple.values)
print "Value Type: " + str(data_frame_simple.value_type)
data_frame_simple.to_string()

data_frame_offset = BayEOSFrame([2,4], value_type=0x01, offset=2)
data_frame_offset.to_string()

# Message Frames
message_frame = BayEOSFrame(frame_type=0x4, string="This is an important message.")
print "Message: " + message_frame.string
message_frame.to_string()
 
error_message_frame = BayEOSFrame(frame_type=0x5, string="This is an ERROR message.")
error_message_frame.to_string()
 
# Origin Frame
origin_frame = BayEOSFrame(frame_type=0xb, origin="My Origin", frame=data_frame_simple.bin)
print "Origin: " + origin_frame.origin
print "Nested frame: " + str(BayEOSFrame.parse_frame(origin_frame.frame))
origin_frame.to_string()