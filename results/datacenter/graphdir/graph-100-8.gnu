set xrange [0:-0.686418320289] reverse
set yrange [0:1.72294570086]
#set logscale x 2
#set logscale y 2

set xtics ("1" log(1)/log(2), "2" log(2)/log(2), "4" log(4)/log(2), "8" log(8)/log(2), "16" log(16)/log(2), "32" log(32)/log(2), "64" log(64)/log(2), "128" log(128)/log(2), "256" log(256)/log(2), "512" log(512)/log(2), "1024" log(1024)/log(2), "2048" log(2048)/log(2), "4096" log(4096)/log(2), "8192" log(8192)/log(2), "16384" log(16384)/log(2), "32768" log(32768)/log(2))

set xlabel "Queueing delay (ms)"
set ylabel "Throughput (Mbps)"
set grid

#set title "15 Mbps dumbbell, Empirical distribution of flow lengths, nsrc 8"

unset key

set terminal svg fsize 12
set output "graph-100-8.svg"
set label "R" at -1,0.91 point textcolor lt 1
set label "B" at -1,0.86 point textcolor lt 1
set label "KEMY" at -1,0.78 point textcolor lt 1
set label "CoDel" at -1,0.86 point textcolor lt 1
set label "D" at -1,0.85 point textcolor lt 1
plot "RED-8.ellipse" with lines lt 1, "Blue-8.ellipse" with lines lt 1, "KEMY-8.ellipse" with lines lt 1, "CoDel-8.ellipse" with lines lt 1, "DropTail-8.ellipse" with lines lt 1
set output
