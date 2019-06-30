include "globals.mzn";

enum Mujeres = {Maria, Ana, Lucia};
enum Hombres = {Carlos, Marco, Juan};

array[Mujeres, Hombres] of int: mpreferencias = [|1, 2, 3, |3, 2, 1, |3, 1, 2 |];
array[Hombres, Mujeres] of int: hpreferencias = [|2, 1, 3, |1, 2, 3, | 1, 3, 2 |];

% 1 -> mayor prioridad

array[Hombres] of var Mujeres: esposas;
array[Mujeres] of var Hombres: esposos;

constraint inverse(esposas, esposos);
constraint forall(m in Mujeres, h in Hombres)
      (mpreferencias[m,h] < mpreferencias[m,esposos[m]] -> hpreferencias[h,esposas[h]] < hpreferencias[h,m]);
constraint forall(m in Mujeres, h in Hombres)
      (hpreferencias[h,m] < hpreferencias[h,esposas[h]] -> mpreferencias[m,esposos[m]] < mpreferencias[m,h]);
  
solve satisfy;