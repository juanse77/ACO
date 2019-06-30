include "globals.mzn";
set of int: R = 1..9;
int: celda = 3;

array[R,R] of var R: s;

s=[|
_, _, _, 1, _, 2, 9, _, _|
_, _, _, _, 9, _, 3, _, 1|
_, _, _, _, _, 8, _, _, 6|
_, _, _, _, 3, _, _, _, _|
_, 6, 2, _, _, _, _, _, _|
_, 7, 9, _, 1, 6, _, _, _|
_, _, 8, _, 6, _, _, _, 7|
_, _, 4, _, _, _, 1, 9, _|
_, _, _, _, _, 4, _, 2, _|
|];

constraint forall(i in R)(
    alldifferent([s[i,j] | j in R])
);
  
constraint forall(j in R)(
    alldifferent([s[i,j] | i in R])
);

constraint forall(i in 0..2, j in 0..2)
  (alldifferent([s[r,c] | r in i*3+1..i*3+3, c in j*3+1..j*3+3]));

solve satisfy;
  
  
  
  
  