int: nRecetas;
set of int: RECETAS = 1..nRecetas;
array[RECETAS] of int: valor;
int: Ingredientes;

set of int: INGREDIENTES = 1..Ingredientes;

array[INGREDIENTES] of set of RECETAS: group;
var set of RECETAS: menu;

constraint forall(i in INGREDIENTES)(card(menu intersect group[i]) <=1);

constraint card(menu)<=3;
var int: valorNutricional = sum(m in menu)(valor[m]);
solve maximize(valorNutricional);

output["Valor nutricional: \(valorNutricional) ->", show(menu)];