import os
import sys
from optparse import OptionParser
import subprocess
import matplotlib
if os.uname()[0] == 'Darwin': matplotlib.use('macosx')
#import matplotlib.pyplot as p
#import numpy

def runonce(fullname, src_proto, w, gateway, nsrc, type,  on, off, outfname,topo):
    global conffile
    gw = gateway
    if src_proto.find("XCP") != -1:
        sink = 'TCPSink/XCPSink'
        #gw = 'XCP'              # overwrite whatever was given
    elif src_proto.find("Linux") != -1:
        sink = 'TCPSink/Sack1'
    else:
        sink = 'TCPSink'

    if fullname.find("CoDel") != -1:
        gw = "sfqCoDel"

    if type == "bytes":
        #runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -onrand %s -avgbytes %d -offrand %s -offavg %s -nsrc %d -simtime %d -topo %s' % (conffile, src_proto, sink, gw, type, w, on, w, off, nsrc, simtime,topo)
        runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -onrand %s -avgbytes %d -offrand %s -offavg %s -nsrc %d  -topo %s' % (conffile, src_proto, sink, gw, type, w, on, w, off, nsrc,topo)
    elif type == "time":
        runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -onrand %s -onavg %d -offrand %s -offavg %s -nsrc %d  -topo %s' % (conffile, src_proto, sink, gw, type, w, on, w, off, nsrc,topo)
        #runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -onrand %s -onavg %d -offrand %s -offavg %s -nsrc %d -simtime %d -topo %s' % (conffile, src_proto, sink, gw, type, w, on, w, off, nsrc, simtime,topo)
    else:
        runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -offrand %s -offavg %s -nsrc %d -topo' % (conffile, src_proto, sink, gw, type, w, off, nsrc, topo)
        #runstr = './kemy3.tcl %s -tcp %s -sink %s -gw %s -ontype %s -offrand %s -offavg %s -nsrc %d -simtime %d -topo' % (conffile, src_proto, sink, gw, type, w, off, nsrc, simtime,topo)


    print runstr
    fnull = open(os.devnull, "w")
    fout = open(outfname, "ab")
    output = subprocess.call(runstr, stdout=fout, shell=True)
    return

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--conffile", type="string", dest="kemyconf",
                      default = "", help = "kemy config file (Tcl)")
    parser.add_option("-d", "--dirresults", type="string", dest="resdir",
                      default = "./tmpres", help = "directory for results")
    parser.add_option("-p", "--src_proto", type="string", dest="src_proto",
                      default = "TCP", help = "src protocol")
    parser.add_option("-t", "--type", type="string", dest="ontype",
                      default = "bytes", help = "by bytes or by seconds")
    parser.add_option("-n", "--nsrc", type="int", dest="nsrc",
                      default = 1, help = "nsrc"),
    parser.add_option("-q", "--queue",type="string", dest="queue_proto",
                      default = "DropTail", help= "queue protocol")
    parser.add_option("-a", "--iteration",type="int", dest="iterations",
                      default = "128", help= "iterations")
    parser.add_option("--topo",type="string",dest="topo",
                      default = "Dumbbell",help = "topology")

    (config, args) = parser.parse_args()

    if not os.path.exists(config.resdir):
        os.mkdir(config.resdir)

    conffile = config.kemyconf
    queue_proto = config.queue_proto
    #simtime = 100
    iterations = config.iterations
    topo = config.topo
    src_proto = config.src_proto
    onofftimes = [0.5]
#    avg_byte_list = [16000, 96000, 192000]
    avgbytes = 100000 # from Allman's March 2012 data and 2013 CCR paper
    worktypes = ['Exponential']

    fullname = src_proto
    for wrk in worktypes:
        for onoff in onofftimes:
            numsrcs = config.nsrc
            while numsrcs <= config.nsrc:
                for i in xrange(iterations):
                    if config.ontype == "bytes":
                        #outfname = '%s/%s.%s.%s.nconn%d.%son%d.off%d.simtime%d' % (config.resdir, fullname.replace('/','-'),queue_proto, wrk, numsrcs, config.ontype, avgbytes, onoff, simtime)
                        outfname = '%s/%s.%s.%s.nconn%d.%son%d.off%d.s' % (config.resdir, fullname.replace('/','-'),queue_proto, wrk, numsrcs, config.ontype, avgbytes, onoff)
                        #runonce(fullname, src_proto, wrk, queue_proto, numsrcs, config.ontype, simtime, avgbytes, onoff, outfname,topo)
                        runonce(fullname, src_proto, wrk, queue_proto, numsrcs, config.ontype,  avgbytes, onoff, outfname,topo)
                    else:
                        #outfname = '%s/%s.%s.%s.nconn%d.%son%d.off%d.simtime%d' % (config.resdir, fullname.replace('/','-'), queue_proto, wrk, numsrcs, config.ontype, onoff, onoff, simtime)
                        outfname = '%s/%s.%s.%s.nconn%d.%son%d.off%d.s' % (config.resdir, fullname.replace('/','-'), queue_proto, wrk, numsrcs, config.ontype, onoff, onoff)
                        runonce(fullname, src_proto, wrk, queue_proto, numsrcs, config.ontype, onoff, onoff, outfname,topo)
                    print outfname
                numsrcs = 2*numsrcs
