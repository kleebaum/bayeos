"""Script to test the time delay during writing."""

from time import time, sleep, strptime, strftime, mktime
from bayeosgatewayclient import BayEOSWriter, BayEOSSender, bayeos_argparser

# Fetch input arguments
args = bayeos_argparser('Measures time delay between two frames.')

WRITER_SLEEP = float(args.writer_sleep)
MAX_CHUNK = float(args.max_chunk)
SENDER_SLEEP = WRITER_SLEEP * float(MAX_CHUNK/20)

NAME = args.name + '-WS' + str(WRITER_SLEEP) + '-M' + str(MAX_CHUNK)
PATH = args.path + '/' + NAME + '/'
if args.url:
    URL = args.url
else:
    URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

print 'name to appear in Gateway is', NAME
print 'max-chunk is', MAX_CHUNK, 'byte'
print 'writer sleep time is', WRITER_SLEEP, 'sec'
print 'path to store writer files is', PATH


# init writer and sender
writer = BayEOSWriter(PATH, MAX_CHUNK)
writer.save_msg('Writer was started.')

sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')

# start measurement
today = mktime(strptime(strftime('%Y-%m-%d'), '%Y-%m-%d'))
start = time()
t_run = time() - start

while t_run <= 1000:
    t = time()
    t_run = t - start
    writer.save([t_run, t - today], value_type=0x21)
    sleep(WRITER_SLEEP)

# start sender
while True:
    res = sender.send()
    if res > 0:
        print 'Successfully sent ' + str(res) + ' frames.\n'
        break
