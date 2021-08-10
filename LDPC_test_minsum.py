from LDPC_test import MessagePassing4, create_input3, run_test
from LDPC import matrix_generation, BSC_channel, create_lookup
import numpy as np
import time
import sys
np.set_printoptions(threshold=sys.maxsize)

from scipy.sparse import csc_matrix, csr_matrix 



def current_milli_time():
    return round(time.time() * 1000)

if __name__ == '__main__':
    n =  1000
    w_c = 3
    w_r = 6
    crossoverProba=0.05
    #seed = int(sys.argv[1])
    seed = 10
    #print(f'seed: {seed}')
    n = w_r*(n//w_r)
    print("n={} wc={} wr={} p={}".format(n,w_c,w_r,crossoverProba))
    codeword = np.random.choice([0,1],size = n)
    time0=current_milli_time()
    matrix = matrix_generation(n,w_c,w_r,seed)
    time1=current_milli_time() 
    print("time for gen H: {} ms".format(time1-time0))
    #print(matrix)
    #exit()

    time0=current_milli_time()
    syndrome = matrix.dot(codeword)%2
    time1=current_milli_time() 
    print("time to compute Hc: {} ms".format(time1-time0))
    #print(syndrome)
    #print(np.array_equal(syndrome,syndrome1))

    time0=current_milli_time()     
    lookup = create_lookup(matrix,w_r,w_c)
    time1=current_milli_time() 
    print("time to create lookup 4: {} ms".format(time1-time0))
    

    itermp = 100
    print(f'itermp max: {itermp}')

    #run_test(matrix1, lookup, codeword, crossoverProba, syndrome, bpiter, itertest=10)
    itertest=5

    Ltime=[]
    Lrounds=[]
    success = 0
    false_pos = 0

    for i in range(itertest):
        received, postProba = BSC_channel(codeword, crossoverProba)
    
        create_input3(lookup, postProba)
        #print(lookup)

        #verifi, res = MessagePassing2(matrix, lookup, postProba, syndrome)
        verifi, rounds, time, string = MessagePassing4(matrix, lookup, postProba, syndrome, itermp)
        #print(f'y: {string}')
        if verifi:
            #print(res)
            print("ok")
            print(f"rounds: {rounds}")
            Ltime.append(time)
            Lrounds.append(rounds)
            if np.array_equal(string,codeword):
                success += 1
            else:
                false_pos += 1

        else:
            print("Fail to decode")
            print(f"rounds: {rounds}")

    if Ltime != []:
        mean_rounds = sum(Lrounds)/len(Lrounds)
        print(f'mean rounds: {round(mean_rounds,2)} min: {min(Lrounds)} max: {max(Lrounds)}')
        mean_time = sum(Ltime)/len(Ltime)
        print(f'mean time: {round(mean_time/1000,3)} sec ({round(mean_time/mean_rounds/1000,3)} sec / round)')
    print(f'success: {success} / {itertest}')
    print(f'false_pos: {false_pos} / {itertest}')
    print(' ')
