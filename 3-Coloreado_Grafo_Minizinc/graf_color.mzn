int: nNodos;
int: nAristas;
array[1..nAristas,1..2] of int: aristas;
array[0..nNodos-1] of var 1..nAristas: resultado;

constraint resultado[0] = 1;

constraint forall(j in 1..nAristas)
            (resultado[aristas[j,1]] != resultado[aristas[j,2]]);
      
solve minimize sum(resultado);
