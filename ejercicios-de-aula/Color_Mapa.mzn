enum Countries = {Belgium, Denmark, France, Germany, Netherlands, Luxembourg};
enum Colors = {black, yellow, red, blue};

array[Countries] of var Colors: color;

constraint color[Belgium] != color[France];
constraint color[Belgium] != color[Germany];
constraint color[Belgium] != color[Netherlands];
constraint color[Belgium] != color[Luxembourg];
constraint color[Denmark] != color[Germany];
constraint color[France] != color[Germany];
constraint color[France] != color[Luxembourg];
constraint color[Germany] != color[Netherlands];
constraint color[Germany] != color[Luxembourg];

solve satisfy;