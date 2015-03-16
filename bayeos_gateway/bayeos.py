from _struct import pack
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
		bayeosFrame = pack("C2", 0x1)
		# Extract offset and data type
		offsetType = 0xf0 & type
		dataType = 0x0f & type
		if offsetType == 0x0:
			# simple offset frame
			bayeosFrame += pack("C", offset)
		for (key, value) in values:
			if offsetType == 0x04:
				# Offset-value frame
				bayeosFrame += pack("C", key)
			#switch(dataType): 
			
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
	
	