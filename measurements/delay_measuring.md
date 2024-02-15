# Measuring after the random delay fix

The delays are much higher because of the random number geneation, every random call needs round about 90µs.

2 * ~90µs (random call) + ~10µs (normal runtime) + 2 * 0-10µs (acutal delay) = ~190-210µs runtime

**no number correct**  
200.437  
200.25  
195.187  
192.313

**first number correct**  
200.209  
203.536  
192.396  
203.562

**first two correct**  
196.375  
198.437  
202.084  
197.271

**fist three correct**  
199.771  
193.021  
198.75  
201.375
