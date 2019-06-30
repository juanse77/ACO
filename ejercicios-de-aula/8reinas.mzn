int: n = 8;
set of int: R = 1..n;
array[R] of var R: columnas;

constraint forall(i in R, j in i+1..n)(
  columnas[i] != columnas[j] /\
  columnas[i] != columnas[j] + (j-i) /\
  columnas[i] != columnas[j] - (j-i)
  );
  
solve satisfy;