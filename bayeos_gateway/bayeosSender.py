class BayEOSSender():
	"""
	Constructor for BayEOS-Sender
	@param path: path where BayEOSWriter puts files
	@param name: sender name
	@param url: gateway url e.g. http://<gateway>/gateway/frame/saveFlat
	@param pw: password on gateway
	@param user: user on gateway
	@param absoluteTime: if set to false, relative time is used (delay)
	@param rm: if set to false files are kept as .bak file in the BayEOSWriter directory
	@param gatewayVersion: gateway version
	"""
	def __init__(self, name, url, pw, user='import', absoluteTime=True, rm=True, gatewayVersion='1,9'):
		pass
	
	"""number of post requests"""
	def send(self):
		pass
	
	
	
	
		