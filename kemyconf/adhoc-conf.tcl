# config file for adhoc simulations
# this one is where all the sources are identical
global opt

# source, sink, and app types
set opt(nsrc) 8;                # number of sources in experiment
set opt(tcp) TCP/Rational
set opt(sink) TCPSink
set opt(cycle_protocols) false

# topology parameters
set opt(gw) DropTail;           # queueing at bottleneck
set opt(bneck) 15Mb;             # bottleneck bandwidth (for some topos)
set opt(maxq) 1000;             # max queue length at bottleneck
set opt(rcvwin) 65536
set opt(delay) 74ms;            # total one-way delay in topology
set opt(link) None

# app parameters
set opt(app) FTP/OnOffSender
set opt(pktsize) 1210;          # doesn't include proto headers

# random on-off times for sources
set opt(seed) 0
set opt(onrand) Exponential
set opt(offrand) Exponential
set opt(onavg) 5.0;              # mean on and off time
set opt(offavg) 0.2;              # mean on and off time
set opt(avgbytes) 100000;          # 16 KBytes flows on avg (too low?)
set opt(ontype) "bytes";           # valid options are "bytes" and "flowcdf"
set opt(reset) "false";             # reset TCP on end of ON period

# simulator parameters
#set opt(simtime) 100.0;        # total simulated time
set opt(simtime) 1000.0;        # total simulated time
#set opt(tr) remyout;            # output trace in opt(tr).out
set opt(partialresults) false;   # show partial throughput, delay, and utility?
set opt(verbose) false;          # verbose printing for debugging (esp stats)
set opt(checkinterval) 0.005;        # check stats every 5 ms

# utility and scoring
set opt(alpha) 1.0
set opt(tracewhisk) "none";     # give a connection ID to print for that flow, or give "all"

proc set_access_params { nsrc } {
    global accessdelay
    for {set i 0} {$i < $nsrc} {incr i} {
        set accessdelay($i) 1ms;       # latency of access link
    }
    global accessrate
    for {set i 0} {$i < $nsrc} {incr i} {
        set accessrate($i) 1000Mb;       # speed of access link
    }
}
set wireless_config(chan)           Channel/WirelessChannel    ;#Channel Type
set wireless_config(prop)           Propagation/TwoRayGround   ;# radio-propagation model
set wireless_config(netif)          Phy/WirelessPhy            ;# network interface type
set wireless_config(mac)            Mac/802_11                 ;# MAC type
set wireless_config(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
set wireless_config(ll)             LL                         ;# link layer type
set wireless_config(ant)            Antenna/OmniAntenna        ;# antenna model
set wireless_config(ifqlen)         1000                         ;# max packet in ifq
set wireless_config(rp)             DSDV                       ;# routing protocol
#set wireless_config(rp)             DSR                       ;# routing protocol
set wireless_config(x)		500
set wireless_config(y)		500


set windowVsTime2 [open win.tr w]
Queue/RED set thresh_ 20 
#Queue/RED set maxthresh_ 40 
#Queue/RED set mean_pktsize_ 1000 
Queue/RED set q_weight_ 0.002
