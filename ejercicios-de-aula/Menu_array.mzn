int: nRecetas;
set of int: RECETAS = 1..nRecetas;
set of int: RECETASx = 0..nRecetas;

array[RECETAS] of int: valor;
int: Ingredientes;

set of int: INGREDIENTES = 1..Ingredientes;
int: numPlatos = 3;
array[INGREDIENTES] of set of RECETAS: group;
array[1..numPlatos] of var RECETASx: menu;

constraint forall(i in 1..numPlatos-1)(menu[i] >= (menu[i]!=0) + menu[i+1]);
constraint forall(i in INGREDIENTES)(sum(j in 1..numPlatos)(menu[j] in group[i])<=1);

var int: valorNutricional = sum(m in 1..numPlatos where menu[m]!=0)(valor[menu[m]]);

solve maximize(valorNutricional);

output["Valor nutricional: \(valorNutricional) ->", show(menu)];