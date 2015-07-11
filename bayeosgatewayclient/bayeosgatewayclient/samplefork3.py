"""Creates an example writer and sender using Unix fork.
One parent process forks child processes for every name.
Each of this child processes is forked again. The parent becomes a writer, the child a sender.
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
    
    pid_main = fork()
    if pid_main > 0: # Parent, main process
        print "One writer-sender pair was forked."
    elif pid_main == 0: # Child process
        pid = fork()
        if pid > 0:
            print "Hello from Parent Writer "
            writer = BayEOSWriter(PATH, max_chunk=100)
            writer.save_msg('Writer was started.')
            while True:
                #print 'adding frame\n'
                writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2)
                sleep(1)
        elif pid == 0:
            print "Hello from Child Sender "
            sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')
            while True:
                sender.send()
                sleep(5)
        else:
            exit("Writer-Sender fork error.")
    else:
        exit("Main process fork error.")