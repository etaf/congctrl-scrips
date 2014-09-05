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
parser.add_option("-w","--whiskers",  type="string",dest="whiskers")
(config, args) = parser.parse_args()
#===config=====================================================
whiskers_dir = config.whiskers
results_basedir = os.path.join(cwd,'results')

iterations = config.iterations
result_name = config.result_name+"-"+str(iterations)
src_proto = "TCP"
topo = config.topo
nsrcs = [ 8 ]
topos = ['Dumbbell','adhoc','datacenter','4g']

if topo == 'Dumbbell':
    conffile = "./kemyconf/dumbbell-buf1000-rtt150-bneck15.tcl"
elif topo == 'adhoc':
    conffile = "./kemyconf/adhoc-conf.tcl"
elif topo == 'datacenter':
    conffile = './kemyconf/datacenter.tcl'
elif topo == '4g':
    conffile = "./kemyconf/vz4gdown.tcl"
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
    print "saving results to %s\n" % results_dir

    print "=================================================\n"
    childs = []
    for nsrc in nsrcs:
        childs.append(subprocess.Popen('python runkemy.py -c %s -d %s -q DropTail -p %s -n %d -a %d --topo=%s' % \
                (conffile,results_dir,src_proto,nsrc,iterations,topo),shell=True))
        if not topo == 'adhoc':
            childs.append(subprocess.Popen('python runkemy.py -c %s -d %s -q Blue -p %s -n %d -a %d --topo=%s' % \
                (conffile,results_dir,src_proto,nsrc,iterations,topo),shell=True))
        childs.append(subprocess.Popen('python runkemy.py -c %s -d %s -q RED -p %s -n %d -a %d --topo=%s' % \
                (conffile,results_dir,src_proto,nsrc,iterations,topo),shell=True))

        childs.append(subprocess.Popen('python runkemy.py -c %s -d %s -q CoDel -p %s -n %d -a %d --topo=%s' % \
                (conffile,results_dir,src_proto,nsrc,iterations,topo),shell=True))
        os.environ['WHISKERS'] = config.whiskers
        childs.append(subprocess.Popen('python runkemy.py -c %s -d %s -q KEMY -p %s -n %d -a %d --topo=%s' % \
                (conffile,results_dir,src_proto,nsrc,iterations,topo),shell=True))

        for child in childs:
            child.wait()

print "================generating graph=================================\n"
############ make graph #####################
pre_graph_name = "graph-%d" % iterations
os.chdir("./graphing-scripts")
subprocess.call("./graphmaker %s %s" % (results_dir,pre_graph_name), shell=True)
os.chdir(cwd)
for nsrc in nsrcs:
    subprocess.Popen("display %s" % os.path.join(results_dir,'graphdir','%s-%d.png' % (pre_graph_name,nsrc)),shell=True)
#############################################

