#!/usr/bin/env python
# encoding: utf-8
import os
import subprocess

os.environ['WHISKERS'] = "./jrats/delta1-alpha0.5-1d-gen.78"
child = subprocess.Popen('./kemy4.tcl ./kemyconf/test-square.tcl -tcp TCP -sink TCPSink -gw KEMY -ontype bytes -onrand Exponential -avgbytes 100000 -offrand Exponential -offavg 0.5 -nsrc 16 -topo square > kemy4.log ',shell=True )
child.wait()


