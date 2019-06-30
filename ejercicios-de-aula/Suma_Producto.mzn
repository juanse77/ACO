int: n = 5;

array[1..n] of var 1..9: v;

constraint sum(v) == product(v);
constraint forall(i in 1..n-1)(v[i] <= v[i+1]);

solve satisfy;