import os
from optparse import OptionParser
import subprocess
import matplotlib
if os.uname()[0] == 'Darwin': matplotlib.use('macosx')
#import matplotlib.pyplot as p
#import numpy

def runonce(gw, buffersize,outfname,topo,tr_fname):
    global conffile

    runstr = './kemy4.tcl %s -gw %s -topo %s -maxq %d -tr %s' % (conffile, gw, topo, buffersize, tr_fname)

    print runstr
    fout = open(outfname, "ab")
    output = subprocess.call(runstr, stdout=fout, shell=True)
    return

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--conffile", type="string", dest="kemyconf",
                      default = "", help = "kemy config file (Tcl)")
    parser.add_option("-d", "--dirresults", type="string", dest="resdir",
                      default = "./tmpres", help = "directory for results")
    parser.add_option("-q", "--queue",type="string", dest="queue_proto",
                      default = "DropTail", help= "queue protocol")
    parser.add_option("-a", "--iteration",type="int", dest="iterations",
                      default = "1", help= "iterations")
    parser.add_option("--topo",type="string",dest="topo",
                      default = "Dumbbell",help = "topology")
    parser.add_option("-b", type ="int", dest = "buffersize",default = 1000, help = "buffer size")

    (config, args) = parser.parse_args()

    if not os.path.exists(config.resdir):
        os.mkdir(config.resdir)

    tr_dir = os.path.join(config.resdir,"tr")
    if not os.path.exists(tr_dir):
        os.mkdir(tr_dir)

    conffile = config.kemyconf
    queue_proto = config.queue_proto
    #simtime = 100
    iterations = config.iterations
    topo = config.topo
    #src_proto = config.src_proto
    buffersize = config.buffersize
    #onofftimes = [0.5]
    #avg_byte_list = [16000, 96000, 192000]
    #avgbytes = 100000 # from Allman's March 2012 data and 2013 CCR paper
    #worktypes = ['Exponential']
    #wrk = 'Exponential'
    #numsrcs = config.nsrc
    for i in xrange(iterations):
        outfname = '%s/%s.buffersize%d.topo%s' % (config.resdir, queue_proto, config.buffersize,config.topo )
        tr_fname = "%s/%s.buffersize%d.topo%s" % (tr_dir, queue_proto, config.buffersize, config.topo)
        runonce( queue_proto, buffersize, outfname,topo, tr_fname)
        print outfname
        print tr_fname
