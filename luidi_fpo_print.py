#Imprime o valor das tensões nodais em kV e p.u
printf "\n\tmatriz_voltage_ampl=[\n";
for {n in N,d in D} {
	printf "%d\t%0.5f\n",n,sqrt(V2[n,d]);
}
printf "\n\];\n";
#cálculo da tensão mínima do sistema
var volmin;
let volmin := min {n in N,d in D} V2[n,d];
printf "\nvmin barra %d\t%10.4f\n", min {n in N,d in D: V2[n,d] == volmin} n, sqrt( volmin ) / vb;
