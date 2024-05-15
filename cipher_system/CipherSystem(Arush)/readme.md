
So I created our cipher system, which is usable through the functions RBAencryption.py and RBAdecryption.py. 

The parameters of both the functions are:  
Usage: python3 RBAencryption.py [ciphersystem] [cipherkeyset]

Possible inputs: 


[ciphersystem] = XOR, DES, VIG, RC4       -> type of encryption system we want to use. 


[cipherkeyset] = keyset1 (for example)    -> the 'name' of the key we are using. Think of this as the value in a <value>:<key> pair, where you put in the value and 
                                             the program will find the key, or create a new 50-character key if the inputted value is not found. 



In this way, we can vary/change both the ciphersystem and the keys (as well as switch back to old ones) we are using for our cipher system. 


