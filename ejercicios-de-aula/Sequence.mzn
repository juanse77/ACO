int: n = 6;

array[1..n] of var 0..3: v;

constraint v[1] = 0;
constraint v[n] = 3;

constraint forall(i in 1..n-1)(v[i]+v[i+1] <= 3);
constraint forall(i in 1..n where i mod 3 = 0)(v[i] >= 2);

var int: suma = sum(v);

solve maximize suma;

output ["\(suma) = \(v)"];