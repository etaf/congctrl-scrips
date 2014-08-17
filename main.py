#!/usr/bin/env python
# encoding: utf-8

from optparse import OptionParser
import os
import subprocess
cwd = os.getcwd()
#===config=====================================================
whisker_basedir = os.path.join(cwd,"./jrats")
results_basedir = os.path.join(cwd,'results')
result_name = 'Dumbbell'
iterations = 1
src_proto = "TCP"
topo ="Dumbbell"
nsrcs = [ 8 ]
#conffile = "./kemyconf/adhoc-conf.tcl"
#conffile = "./kemyconf/datacenter.tcl"
conffile = "./kemyconf/dumbbell-buf1000-rtt150-bneck15.tcl"
results_dir = os.path.join(results_basedir, result_name)
Force = False
#debugg = True
#==============================================================


parser = OptionParser()
parser.add_option("-n", type="int", dest="iterations",
                  default = iterations, help = "iterations")
parser.add_option("-f", action = "store_true", dest="Force", default = False)
(config, args) = parser.parse_args()

iterations = config.iterations
print "=================================================\n"
if config.Force == True:
    print "execing shell cmd: rm %s/results/* -rf\n" % cwd
    subprocess.call(['rm ./results/* -rf'],shell=True)


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
        os.environ['WHISKERS'] = os.path.join(whisker_basedir, 'delta1-alpha0.5-1d-gen.78')
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

