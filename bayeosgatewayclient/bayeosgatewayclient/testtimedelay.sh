#!/bin/sh

for m in 20 40 80 160 320 640 1280 2560
do
    python2.7 testtimedelay.py -m $m -ws 1
done

for ws in 1 0.5 0.25 0.125 0.1 0.0625 0.05 0.01 
do
    python2.7 testtimedelay.py -m 20 -ws $ws
done
