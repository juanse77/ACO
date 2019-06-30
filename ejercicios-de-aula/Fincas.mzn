int: nFincas = 5;
array[1..nFincas] of float: valor = [2, 2.4, 3, 4, 4.4]; 
array[1..nFincas] of var 0..1: seleccionados;

constraint sum(seleccionados) = 3;
constraint (seleccionados[4] + seleccionados[5]) <= 1;

solve minimize sum(i in 1..nFincas)(valor[i]*seleccionados[i]);