#!/usr/bin/env python
# encoding: utf-8
import sys
from optparse import OptionParser
import os
import subprocess
cwd = os.getcwd()

parser = OptionParser()
parser.add_option("-n", type="int", dest="iterations",
                  default = 1, help = "iterations")
parser.add_option("-f", action = "store_true", dest="Force", default = False)
parser.add_option("--result", type="string",dest="result_name",default="Dumbbell")
parser.add_option("--topo", type="string", dest="topo",default="Dumbbell")
parser.add_option("-w","--whiskers",  type="string",dest="whiskers", default="./jrats/delta1-alpha0.5-1d-gen.78")
(config, args) = parser.parse_args()
#===config=====================================================
whiskers_dir = config.whiskers
results_basedir = os.path.join(cwd,'results')

iterations = config.iterations
result_name = config.result_name
src_proto = "TCP"
topo = config.topo
nsrc = 8
qlens = [10, 20, 30, 40, 50,75,100, 150, 200, 300]
#qlens = [1000]
topos = ['Dumbbell','adhoc','datacenter','4g','square']

if topo == 'Dumbbell':
    conffile = "./kemyconf/dumbbell-compare-buf.tcl"
    MIN_RTT = 149.5
elif topo == 'adhoc':
    conffile = "./kemyconf/adhoc-conf.tcl"
    MIN_RTT = 0
elif topo == 'datacenter':
    conffile = './kemyconf/datacenter.tcl'
elif topo == '4g':
    conffile = "./kemyconf/vz4gdown.tcl"
elif topo == 'square':
    conffile = "./kemyconf/square.tcl"
    MIN_RTT = 150
else:
    print "not such topo suported"
    sys.exit()

results_dir = os.path.join(results_basedir, result_name)
#==============================================================


print "=================================================\n"
if config.Force == True:
    print "execing shell cmd: rm %s -rf\n" % (results_dir)
    subprocess.call(['rm %s -rf' % (results_dir)],shell=True)


if not os.path.exists(results_basedir):
    os.mkdir(results_basedir)

if  os.path.exists(results_dir):
    print "resulst already existed .\n"

else:
    os.mkdir(results_dir)
    os.mkdir(os.path.join(results_dir, "tr"))
    print "saving results to %s\n" % results_dir

    print "=================================================\n"
    childs = []
    for qlen in qlens:
        childs.append(subprocess.Popen('python runkemy2.py -c %s -d %s -q DropTail  -a %d --topo=%s -b %d' % \
                (conffile,results_dir,iterations,topo,qlen),shell=True))
        if not topo == 'adhoc':
            childs.append(subprocess.Popen('python runkemy2.py -c %s -d %s -q Blue  -a %d --topo=%s -b %d' % \
                (conffile,results_dir,iterations,topo,qlen),shell=True))
        childs.append(subprocess.Popen('python runkemy2.py -c %s -d %s -q RED  -a %d --topo=%s -b %d' % \
                (conffile,results_dir,iterations,topo,qlen),shell=True))

        childs.append(subprocess.Popen('python runkemy2.py -c %s -d %s -q CoDel  %d --topo=%s -b %d' % \
                (conffile,results_dir,iterations,topo,qlen),shell=True))
        os.environ['WHISKERS'] = config.whiskers
        childs.append(subprocess.Popen('python runkemy2.py -c %s -d %s -q KEMY  %d --topo=%s -b %d' % \
                (conffile,results_dir,iterations,topo,qlen),shell=True))

        for child in childs:
            child.wait()

print "================generating graph=================================\n"
############ make graph #####################
pre_graph_name = "graph-compare-bufferbloat"
os.chdir("./graphing-scripts")
subprocess.call("./graphmaker-bufferbloat %s %s %f" % (results_dir,pre_graph_name,MIN_RTT), shell=True)
os.chdir(cwd)
#subprocess.Popen("display %s" % os.path.join(results_dir,'graphdir','%s.svg' % (pre_graph_name)),shell=True)
#############################################

