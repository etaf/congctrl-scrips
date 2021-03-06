# Experiments with on-off sources that transmit data for a certain
# "on" time and then are silent for a certain "off" time. The on and
# off times come from exponential distributions at specifiable rates.
# During the "on" period, the data isn't sent at a constant bit rate
# as in the existing exponential on-off traffic model in
# tools/expoo.cc but is instead sent according to the underlying
# transport (agent) protocol, such as TCP.  The "off" period is the
# same as in that traffic model.

#!/bin/sh
# the next line finds ns \
nshome=`dirname $0`; [ ! -x $nshome/ns ] && [ -x ../../../ns ] && nshome=../../..
# the next line starts ns \
export nshome; exec $nshome/ns "$0" "$@"

if [info exists env(nshome)] {
	set nshome $env(nshome)
} elseif [file executable ../../../ns] {
	set nshome ../../..
} elseif {[file executable ./ns] || [file executable ./ns.exe]} {
	set nshome "[pwd]"
} else {
	puts "$argv0 cannot find ns directory"
	exit 1
}

source sender-app.tcl
source logging-app2.tcl
source stats.tcl

set conffile ./kemyconf/adhoc-conf.tcl

proc Usage {} {
    global opt argv0
    puts "Usage: $argv0 \[-simtime seconds\] \[-seed value\] \[-nsrc numSources\]"
    puts "\t\[-tr tracefile\]"
    puts "\t\[-bw $opt(bneck)] \[-delay $opt(delay)\]"
    exit 1
}
proc Getopt {} {
    global opt argc argv
#    if {$argc == 0} Usage
    for {set i 1} {$i < $argc} {incr i} {
        set key [lindex $argv $i]
        if ![string match {-*} $key] continue
        set key [string range $key 1 end]
        set val [lindex $argv [incr i]]
        set opt($key) $val
        if [string match {-[A-z]*} $val] {
            incr i -1
            continue
        }
    }
}
proc create-sources-sinks {} {
    global ns opt s d src recvapp tp protocols protosinks f linuxcc

    set numsrc $opt(nsrc)
    for {set i 0} {$i < $numsrc} {incr i} {

        set tp($i) [$ns create-connection-list $opt(tcp) $s($i) $opt(sink) $d $i]
        set tcpsrc [lindex $tp($i) 0]
        set tcpsink [lindex $tp($i) 1]
        if { [info exists linuxcc] } {
            $ns at 0.0 "$tcpsrc select_ca $linuxcc"
            $ns at 0.0 "$tcpsrc set_ca_default_param linux debug_level 2"
        }

        $tcpsrc set fid_ [expr $i%256]
        $tcpsrc set window_ $opt(rcvwin)
        $tcpsrc set packetSize_ $opt(pktsize)

        if { [info exists opt(tr)] } {
            $tcpsrc trace cwnd_
            $tcpsrc trace rtt_
            $tcpsrc trace maxseq_
            $tcpsrc trace ack_
            $tcpsrc attach $f
        }

        set src($i) [ $tcpsrc attach-app $opt(app) ]
        $src($i) setup_and_start $i $tcpsrc
        set recvapp($i) [new LoggingApp $i]
        $recvapp($i) attach-agent $tcpsink
        $ns at 0.0 "$recvapp($i) start"
    }
}


proc finish {} {
    global ns opt stats src recvapp linuxcc
    global f nf

    for {set i 0} {$i < $opt(nsrc)} {incr i} {
        set sapp $src($i)
        $sapp dumpstats
        set rcdbytes [$recvapp($i) set nbytes_]
        set rcd_nrtt [$recvapp($i) set nrtt_]
        if { $rcd_nrtt > 0 } {
            set rcd_avgrtt [expr 1000.0*[$recvapp($i) set cumrtt_] / $rcd_nrtt ]
        } else {
            set rcd_avgrtt 0.0
        }
        if {$i == 0} {
            if {$opt(cycle_protocols) != "true"} {
                if { [info exists linuxcc] } {
                    puts "Results for $opt(tcp)/$linuxcc $opt(gw) $opt(sink) over $opt(simtime) seconds:"
                } else {
                    puts "Results for $opt(tcp) $opt(gw) $opt(sink) over $opt(simtime) seconds:"
                }
            } else {
                puts "Results for mix of protocols:"
            }
        }

        [$sapp set stats_] showstats $rcdbytes $rcd_avgrtt
    }

    if { [info exists f] } {
        $ns flush-trace
        close $f
    }
    if { [info exists nf] } {
        $ns flush-trace
        close $nf
        exec nam out.nam &
    }
    exit 0
}

## MAIN ##

Agent/TCP set tcpTick_ .0001
Agent/TCP set timestamps_ true
set opt(hdrsize) 50
set opt(flowoffset) 40

source $conffile
puts "Reading params from $conffile"

Getopt

#set opt(rcvwin) [expr int(32*$opt(maxq))]

if { ![info exists opt(spike)] } {
    set opt(spike) false
}

if {$opt(spike) == "true"} {
    set opt(ontype) "time"
}

if { ![info exists opt(reset)] } {
    set opt(reset) true;    # reset TCP connection on end of ON period
}

set_access_params $opt(nsrc)

puts "case: $opt(bneck)"

global defaultRNG
$defaultRNG seed $opt(seed)

#    ns-random $opt(seed)

set ns [new Simulator]
if { [info exists opt(nam)] } {
    set nf [open adhoc.nam w]
    $ns namtrace-all-wireless $nf $opt(x) $opt(y)
}
Queue set limit_ $opt(maxq)
RandomVariable/Pareto set shape_ 0.5

if { [info exists opt(tr)] } {
    # if we don't set up tracing early, trace output isn't created!!
    set f       [open adhoc.tr w]
    $ns trace-all $f

}

set flowfile flowcdf-allman-icsi.tcl



# set up topography object
#
#  Create nn mobilenodes [$opt(nsrc)] and attach them to the channel.
#

# configure the nodes

	for {set i 0} {$i < $opt(src) } { incr i } {
		set node_($i) [$ns node]
	}

# Provide initial location of mobilenodes
$node_(0) set X_ 5.0
$node_(0) set Y_ 5.0
$node_(0) set Z_ 0.0

$node_(1) set X_ 490.0
$node_(1) set Y_ 285.0
$node_(1) set Z_ 0.0

$node_(2) set X_ 150.0
$node_(2) set Y_ 240.0
$node_(2) set Z_ 0.0

# Generation of movements
$ns at 10.0 "$node_(0) setdest 250.0 250.0 3.0"
$ns at 15.0 "$node_(1) setdest 45.0 285.0 5.0"
$ns at 110.0 "$node_(0) setdest 480.0 300.0 5.0"

# Set a TCP connection between node_(0) and node_(1)
set tcp [new Agent/TCP/Newreno]
$tcp set class_ 2
set sink [new Agent/TCPSink]
$ns attach-agent $node_(0) $tcp
$ns attach-agent $node_(1) $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 10.0 "$ftp start"

# Printing the window size
proc plotWindow {tcpSource file} {
    global ns
    set time 0.01
    set now [$ns now]
    set cwnd [$tcpSource set cwnd_]
    puts $file "$now $cwnd"
    $ns at [expr $now+$time] "plotWindow $tcpSource $file"
}


# ending nam and the simulation
$ns at $opt(stop) "$ns nam-end-wireless $opt(stop)"
$ns at $opt(stop) "stop"
$ns at 150.01 "puts \"end simulation\" ; $ns halt"
proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    close $tracefd
    close $namtrace
}

$ns run

