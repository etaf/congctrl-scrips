#!/usr/bin/env python
# encoding: utf-8
import os
import subprocess

os.environ['WHISKERS'] = "./jrats/delta1-alpha0.5-1d-gen.78"
child = subprocess.Popen('./kemy4.tcl ./kemyconf/dumbbell-compare-buf.tcl -tcp TCP -sink TCPSink -gw DropTail -ontype bytes -onrand Exponential -avgbytes 100000 -offrand Exponential -offavg 0.5 -nsrc 8 -topo Dumbbell -nam true -tr test -maxq 20',shell=True )
child.wait()


