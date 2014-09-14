set terminal postscript eps color
#set terminal svg fsize 12
set output "qlen.eps"
set ylabel "buffer size(packet)"
set xlabel "time(ms)"
set title "immediate buffer size compare"

#plot "DropTail.out" u 1:5 w l lc rgb "black" title "DropTail",\
     #"CoDel.out" u 1:5 w l lc rgb "purple" title "CoDel",\
     #"RED.out" u 1:5 w l lc rgb "red" title "RED",\
     #"Blue.out" u 1:5 w l title "Blue",\
     #"KEMY.out" u 1:5 w l  title "kemy"
     #
plot "DropTail.out" u 1:5 w l title "DropTail",\
     "CoDel.out" u 1:5 w l  title "CoDel",\
     "RED.out" u 1:5 w l title "RED",\
     "Blue.out" u 1:5 w l title "Blue",\
     "KEMY.out" u 1:5 w l  title "kemy"

set output
set term wxt
