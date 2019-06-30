var 0..10: x;

constraint x mod 4 = 0;

var int: obj = (x-7)*(x-7);

solve minimize obj;

output["x=\(x); \nobj=\(obj);\n"];