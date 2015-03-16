from requests.api import post
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
	
	"""
	keeps sending as long as all files are send or an error occures
	@return int
	number of post requests
	"""
	def send(self):
		count = 0
		while(post == self.sendFile()):
			count += post
		return(count)
	
	"""
	read one file from the queue and try to send it to the gateway
	on success file is deleted or renamed to *.bak
	takes always the oldest file
	"""
	def sendFile(self):
		pass
		#chdir(self.path)
		
	"""
	@param data
	@return success
	"""
	def post(self, data):
		
	
	
	
		