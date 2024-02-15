# Measuring afte the full pin check fix

I wonder if a better logic analyser could measure the absence of the instruction when the flag is set. This could be fixed by setting another flag in case the current digit is correct (equal instructions).

**no number correct**  
10.663  
10.657  
10.657  
10.594

**first number correct**  
10.657  
10.657  
10.625  
10.625

**first two correct**  
10.75  
10.782  
10.782  
10.75

**fist three correct**  
10.741  
10.77  
10.77  
10.75
