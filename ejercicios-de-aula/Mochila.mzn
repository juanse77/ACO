int: capacity = 45;
set of int: ITEM = 1..6;

array[ITEM] of var int: cantidad;
array[ITEM] of int: weight = [10, 12, 23, 9, 12, 15];
array[ITEM] of int: value = [12, 10, 21, 8, 14, 13];

constraint forall(i in ITEM)(cantidad[i] >= 0);
constraint sum(i in ITEM)(cantidad[i]*weight[i]) <= capacity;

solve maximize sum(i in ITEM)(cantidad[i]*value[i]);