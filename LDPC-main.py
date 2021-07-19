from LDPC import MessagePassing, matrix_generation, BSC_channel
import numpy as np

if __name__ == '__main__':
    n =  12
    w_c = 2
    w_r = 4
    seed = 10
#    code = np.random.choice([0,1],size = n)
    code = np.array([1,0,1,0,1,0,1,0,0,0,0,0])    # initial codeword for testing. I don't generate G here so this one is found by trial, not in systematic way
    print(f"Original codeword: {code}")
    
    matrix = matrix_generation(n,w_c,w_r,seed)
    print(matrix)
    received, postProba = BSC_channel(code, crossoverProba= 0.1)    
    print(postProba)
    print(f"Message receive:{received}")
    verifi, res = MessagePassing(matrix, postProba)
    if verifi:
        print(res)
    else:
        print("Fail to decode")
