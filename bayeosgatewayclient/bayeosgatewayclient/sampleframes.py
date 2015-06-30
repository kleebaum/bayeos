"""Creates example BayEOS Frames."""

from bayeosgatewayclient import BayEOSFrame

data_frame = BayEOSFrame(values=[1,2,3], value_type=0x1, offset=0)
print "Values: " + str(data_frame.values)
print "Value Type: " + str(data_frame.value_type)
data_frame.to_string()

message_frame = BayEOSFrame(frame_type=0x4, string="This is an important message.")
message_frame.to_string()

error_message_frame = BayEOSFrame(frame_type=0x5, string="This is an ERROR message.")
error_message_frame.to_string()

origin_frame = BayEOSFrame(frame_type=0xb, origin="Herkunft", frame=data_frame.bin)
origin_frame.to_string()