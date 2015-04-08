from struct import *

from _dbus_bindings import Array
from mutagen.id3._frames import Frame


class BayEOS():
	"""
	create BayEOS data frame
	@param values
	@param valueType
	@param offset
	@return string (binary)
	"""
	def createDataFrame(self, values, valueType=0x1, offset=0):
		bayeosFrame = pack('bb', 0x1, valueType) 	# 0x1 represents data frame 
	  	offsetType = (0xf0 & valueType) 			# first four bits of frame type
	   	dataType = (0x0f & valueType) 				# last four bits of frame type	
		if offsetType == 0x0:						# data frame with channel offset
	   	 	bayeosFrame += pack('b', offset) 		# 1 byte channel offset
		
		for [key, each_value] in values:
			if offsetType == 0x40:  				# data frame with channel indices
				bayeosFrame += pack('b', key)
			if dataType == 0x1:	 					# float32 4 bytes
				bayeosFrame += pack('f', each_value)
			elif dataType == 0x2:   				# int32 4 bytes
				bayeosFrame += pack('i', each_value)   
			elif dataType == 0x3:   				# int16 2 bytes
				bayeosFrame += pack('h', each_value)  
			elif dataType == 0x4:   				# int8 1 byte
				bayeosFrame += pack('b', each_value)  
			elif dataType == 0x5:   				# double 8 bytes
				bayeosFrame += pack('d', each_value)  
	
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
	
	
