from struct import *
from _dbus_bindings import Array
from mutagen.id3._frames import Frame
class BayEOS():
	"""
	create BayEOS data frame
	@param values
	@param type
	@param offset
	@return string (binary)
	"""
	def createDataFrame(self, values, type=0x1, offset=0):
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
		 	print(each_value)
	
	  	print('Frame created: ', bayeosFrame)
	   	print('Frame unpacked: ', unpack('=bbbff', bayeosFrame))
		return(bayeosFrame)
			
	"""
	parse a binary BayEOS frame into a Python Array
	@param frame
	@param ts
	@param origin
	@param rssi
	@return array
	"""
	def parseFrame(self, frame, ts=False, origin='', rssi=False):
		if not ts:
			ts = 0
			
	"""
	parse a BayEOS data frame into a PHP Array
	@param Frame
	@return Array
	"""
	def parseDataFrame(self, frame):
		pass
	
	
