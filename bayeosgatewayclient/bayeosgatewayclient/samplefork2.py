"""Creates an example writer and sender using Unix fork.
One main process forks first writer and then sender for each name. 
Here is a problem if the Writer is not instantiated yet.
"""

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from os import fork

TEMP = '/tmp/'
SENDER = 'Sender'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

NAMES = ['Dev 1', 'Dev 2', 'Dev 3']

for each_name in NAMES:
    PATH = TEMP + each_name + '/'
    NAME = SENDER + '/' + each_name
    #finished_writer = False
    pid_writer = fork()
    if pid_writer > 0: # Parent
        print "Started writer for " + each_name + " with pid " + str(pid_writer)
        #sleep(2)
        #finished_writer = True
    elif pid_writer == 0: # Child
        writer = BayEOSWriter(PATH, max_chunk=100)
        writer.save_msg('Writer was started.')
#         while True:
#             #print 'adding frame\n'
#             writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2)
#             sleep(2)
    else:
        exit("Writer fork error.")
    
#     while not finished_writer:
#         print "waited"
#         sleep(0.25)

    pid_sender = fork()
    if pid_sender > 0: # Parent
        print "Started sender for " + each_name + " with pid " + str(pid_sender) 
    elif pid_sender == 0: # Child
#         try:
#             chdir(PATH)
#         except OSError:
#             mkdir(PATH, 0700)
        sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')
        while True:
            res = sender.send()
            #if res > 0:
                #print 'Successfully sent ' + str(res) + ' frames.\n'
            sleep(5)
    else:
        exit("Sender fork error.")