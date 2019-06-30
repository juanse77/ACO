% Cinco productos con un valor de mercado distinto
% Cantidad de recursos
% Maximizar el valor de mercado
int: nProductos = 5;
int: nRecursos = 4;

array[1..nProductos] of int: costes=[11, 18, 15, 17, 11];
array[1..nRecursos] of int: recursos=[5000, 7500, 4000, 3000];

array[1..nRecursos, 1..nProductos] of float: produccion=[| 1.5, 2, 1.5, 0.5, 0.1 | 1, 0, 0.5, 1, 2.5 | 1, 2, 1, 0.9, 0.1 | 1, 0, 1, 1.5, 2.5 |];

array[1..nProductos] of var int: productos;

constraint forall(i in 1..nProductos)(productos[i] >= 0);
constraint forall(k in 1..nRecursos)(sum(i in 1..nProductos)(productos[i]*produccion[k,i]) <= recursos[k]);

solve maximize sum(i in 1..nProductos)(costes[i]*productos[i]);