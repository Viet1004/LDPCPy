from LDPC import MessagePassing, matrix_generation, BSC_channel
import LDPC
import numpy as np

if __name__ == '__main__':
    n =  1024
    w_c = 3
    w_r = 4
    seed = 10
    code = np.random.choice([0,1],size = n)
#    code = np.ones(n)    # initial codeword for testing. I don't generate G here so this one is found by trial, not in systematic way
#    print(f"Original codeword: {code}")

#    while(True):
#        print(f"seed now is {seed}")
#        if LDPC.check_cycle(LDPC.create_lookup(LDPC.matrix_generation(n,w_c,w_r,seed))):
#            break
#        seed += 1

    matrix = matrix_generation(n,w_c,w_r,seed)

    syndrome = np.dot(matrix, code)
#    print(matrix)
    received, postProba = BSC_channel(code, crossoverProba= 0.1)    
#    print(postProba)
    print(f"Message receive:{received}")
    verifi, res = MessagePassing(matrix, postProba, syndrome)
    if verifi:
        print(res)
    else:
        print("Fail to decode")
