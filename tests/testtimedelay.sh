#!/bin/sh

NAME="Delay-Test-process-ultrabook"
URL="http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveMatrix"
PATHW="/home/anja/tmp"

for m in 20 40 80 160 320 640 1280 2560
do
    python2.7 testtimedelay_process.py -m $m -ws 1 -n $NAME -u $URL -p $PATHW
done

for ws in 1.0 0.5 0.25 0.125 0.1 0.0625 0.05 0.01 
do
    python2.7 testtimedelay_process.py -m 20 -ws $ws -n $NAME -u $URL -p $PATHW
done

NAME="Delay-Test-thread-ultrabook"
URL="http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveMatrix"
PATHW="/home/anja/tmp"

for m in 20 40 80 160 320 640 1280 2560
do
    python2.7 testtimedelay_thread.py -m $m -ws 1 -n $NAME -u $URL -p $PATHW
done

for ws in 1.0 0.5 0.25 0.125 0.1 0.0625 0.05 0.01 
do
    python2.7 testtimedelay_thread.py -m 20 -ws $ws -n $NAME -u $URL -p $PATHW
done

NAME="Delay-Test-serial-ultrabook"
URL="http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveMatrix"
PATHW="/home/anja/tmp"

for m in 20 40 80 160 320 640 1280 2560
do
    python2.7 testtimedelay_serial.py -m $m -ws 1 -n $NAME -u $URL -p $PATHW
done

for ws in 1.0 0.5 0.25 0.125 0.1 0.0625 0.05 0.01 
do
    python2.7 testtimedelay_serial.py -m 20 -ws $ws -n $NAME -u $URL -p $PATHW
done
#python2.7 testtimedelay_thread.py -m 20 -ws 0.0 -n $NAME
