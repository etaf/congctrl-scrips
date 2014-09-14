set terminal postscript eps enhanced font ',18'
#set terminal svg fsize 8
set output "qlen.eps"
set multiplot layout 5,1
#set ylabel "buffer size(packet)"
#set xlabel "time(ms)"
#set title "immediate buffer size compare"
set yrange [0:250]
set ytics 100
plot "DropTail.out" u 1:5 w l title "DropTail"
plot "Blue.out" u 1:5 w l title "BLUE"
plot "RED.out" u 1:5 w l title "RED"
plot "CoDel.out" u 1:5 w l title "CoDel"
plot "KEMY.out" u 1:5 w l title "KEMY"
#
#plot "DropTail.out" u 1:8 w p title "DropTail"
#plot "Blue.out" u 1:8 w p title "BLUE"
#plot "RED.out" u 1:8 w p title "RED"
#plot "CoDel.out" u 1:8 w p title "CoDel"
#plot "KEMY.out" u 1:8 w p title "KEMY"

unset multiplot
set output
set term wxt
