include "globals.mzn";

int: num_magico;

array[1..3, 1..3] of var 1..9: tabla;

constraint alldifferent(tabla);

constraint forall(i in 1..3)(sum(j in 1..3)(tabla[i,j]) = num_magico);
constraint forall(i in 1..3)(sum(j in 1..3)(tabla[j,i]) = num_magico);
constraint sum(i in 1..3)(tabla[i,i]) = num_magico;
constraint sum(i in 1..3)(tabla[i,4-i]) = num_magico;

solve satisfy;