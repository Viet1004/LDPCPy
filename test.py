from operator import pos
import timeit

from scipy.sparse.csr import csr_matrix
import LDPC
import numpy as np
import time
from scipy.sparse import csc_matrix, save_npz, load_npz 
#from numba import jit

import sys
np.set_printoptions(threshold=sys.maxsize)

def timerfunc(func):
    """
    A timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime in avarage for {func} took {time} seconds to complete"
        print(msg.format(func=func.__name__,
                         time=runtime/20))
        return value
    return function_timer

#@profile
#@timerfunc
def run(n,w_c,w_r, probability,numberOfTest = 1):
    n = int(n//w_r * w_r)
    print(f"n:{n} w_c: {w_c}, w_r: {w_r}, p: {probability}")
    startPreparation = time.time()
    success = 0
    success_log = 0
    success_new = 0
    seed = 10
    m = int(n*w_c/w_r)
#    while(True):
#        if LDPC.check_cycle(LDPC.create_lookup(LDPC.matrix_generation(n,w_c,w_r,seed))):
#            break
#        seed += 1
    code = np.random.choice([0,1],size = n)
    degreeOfVNode = np.zeros(n, dtype=np.int8) + w_c
#    matrix_PEG = LDPC.matrix_generation_PEG(degreeOfVNode,m,n)
#    start1 = time.time()
    matrix = LDPC.matrix_generation(n,w_c,w_r,seed)
#    end1 = time.time()
#    print(f"Matrix generation took: {end1 - start1}")
##    lookup_PEG = LDPC.create_lookup(matrix_PEG)
#    lookup = LDPC.create_lookup(matrix)
##    matrix = csc_matrix(matrix)
##    syndrome_PEG = matrix_PEG.dot(code)
#============ Use for testing

#============ End of testing
    syndrome = matrix.dot(code) % 2 
#    endPreparation = time.time()
#
#    print(f"Preparation time is : {endPreparation - startPreparation}")
#
    startExecution = time.time()
    for i in range(numberOfTest):
        received, postProba = LDPC.BSC_channel(code, crossoverProba= probability)
#        lookup_with_proba_PEG = LDPC.create_input(lookup_PEG, postProba)
#        lookup_with_proba = LDPC.create_input(lookup, postProba)
#        lookup_with_proba_log = LDPC.create_input_log(lookup, postProba)
##        verifi_PEG, res_PEG = LDPC.MessagePassing(lookup_with_proba_PEG, matrix_PEG, postProba, syndrome_PEG)
##        start1 = time.time()
##        verifi, res = LDPC.MessagePassing(lookup_with_proba, matrix, postProba, syndrome)
##        end1 = time.time()
##        print(f"It took {end1 - start1}")
#        start2 =  time.time()
#        verifi_log, res_log = LDPC.MessagePassing_log(lookup_with_proba_log, matrix, postProba, syndrome)
#        end2 = time.time()
#        print(f"Log algo took {end2 - start2}")
##        if verifi:
##            print("This is normal scheme")
##            success += 1  
#        if verifi_log:
#            print("this is log scheme")
#            success_log += 1    
#This is the test space =============================================
    #================
#        postProba = np.array([0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.2,0.8,0.8])
    #================
        start = time.time()
        LDPC.input_generation_regularLDPC(matrix,postProba)
        end = time.time()
        print(f"Preparation time of new method is: {end-start}")
        start = time.time()
        verifi_new, res_new = LDPC.new_MessagePassing(matrix, postProba,syndrome,n)
        end = time.time()
        print(f"new algo took: {end-start}")
        if verifi_new:
            print("This is new scheme")
            success_new += 1  
        else:
            print("Fail to decode!!!")

#        print("\nCompare to code of Anne \n")
#        matrix0 = LDPC.matrix_generation(n,w_c,w_r,seed)
#        print("**************************************************")
#        matrix=new_lookup.matrix_input(n,w_c,w_r,seed,probability,received)
#        postProba = np.log(np.array(postProba)/(1-np.array(postProba)))
#        new_lookup.MessagePassing(matrix0,matrix,postProba,syndrome,w_c,w_r,60)
        
#End of test space =================================================

    endExecution = time.time()
    print(f"Execution time in avarage is : {-(startExecution-endExecution)/numberOfTest}")
    print("======================================================================")
#    print(f"There are {success} successes out of {numberOfTest} tests")
#    print("======================================================================")
    print(f"There are {success_log} successes out of {numberOfTest} tests")
    print("======================================================================")
    print(f"There are {success_new} successes out of {numberOfTest} tests")
    print("======================================================================")

# Test space ====================================================================
#@jit
def test():
#    n1 =  [128,256,512,1024,2048]
    n1 = [201600,1000000]
    set1 = [(4,9)]
#    n2 = [125,250,500,1000,2000]
#    n2 = [1000]
#    set2 = [(3,5),(4,5)]
#    n3 = [120,240,480,960,1920]
#    n3 = [960]
#    set3 = [(4,6),(5,6)]
    proba = (0.05,)
    for n in n1:
        for set in set1:
            for p in proba:
                run(n,set[0],set[1],p)

#    for n in n2:
#        for set in set2:
#            for p in proba:
#                print(f"n:{n} w_c: {set[0]}, w_r: {set[1]}, p: {p}")
#                run(n,set[0],set[1],p)
#    
#    for n in n3:
#        for set in set3:
#            for p in proba:
#                print(f"n:{n} w_c: {set[0]}, w_r: {set[1]}, p: {p}")
#                run(n,set[0],set[1],p)

if __name__ == "__main__":
#    test()
    start = time.time()
    #m = 100
    n = 10000
    m = int(0.25*n)
    print(f'n {n} m {m}')
    Dv = LDPC.matrix_generation_test(m,n)
    #print(Dv)
    # print(sum(Dv))
    # n =  100
    # w_c = 3
    # w_r = 6
    # n = w_r*(n//w_r)
    # m = w_c*(n//w_r)
    p=0.02
    seed = 10    
    #print("n={} wc={} wr={} p={}".format(n,w_c,w_r,p))
    
    #Dv = np.array(n*[w_c])
    #matrix = LDPC.matrix_generation_PEG(Dv, m,n)
    #save_npz('sparse_irregular_075_10000.npz', matrix)
    matrix = load_npz('sparse_irregular_075_10000.npz')
    #matrix = LDPC.matrix_generation(n,w_c,w_r,seed)
    end = time.time()
    print(f"time to gen H {round(end - start,6)} sec")
    codeword = np.random.choice([0,1],size = n)
    #print(f'codeword: {codeword}')
    syndrom = matrix.dot(codeword) %2
    #print(f'syndrom: {syndrom}')

    #print(f'rank: {np.linalg.matrix_rank(matrix.todense())}')


    success = 0
    false_pos = 0
    Lrounds = []
    Lcopm = []
    nbTest=10
    for i in range(nbTest):
        received, postProba = LDPC.BSC_channel(codeword, p)
        #print(f'received: {received} postProba: {postProba}')
        initial_error=((received-codeword)%2).sum()
        copm=initial_error/n
        #print(f'true crossoverProba: {round(copm,5)}')
        Lcopm.append(copm)
        time0=round(time.time()*1000)
        verifi, rounds, recv_vec, match_fail, match_success = LDPC.new_MessagePassing(matrix, postProba,syndrom,n)
        if verifi:
            print("Successful decoding!")
            if ((codeword-recv_vec)%2).sum() == 0:
                success += 1
                Lrounds.append(rounds)
            else :
                false_pos += 1
            time1=round(time.time()*1000)
            print(f'time to decode {time1-time0} ms')
        else:
            print("Failed!!!")
            time1=round(time.time()*1000)
            print(f'time to not decode {time1-time0} ms')
        #print(f'resulting error: {((codeword-recv_vec)%2).sum()}')

    print(f'total success: {success } / {nbTest} false_pos: {false_pos}')
    if success != 0:
        mean_rounds = sum(Lrounds)/len(Lrounds)
        print(f'mean rounds: {round(mean_rounds,2)} min: {min(Lrounds)} max: {max(Lrounds)}')
        #mean_time = sum(Ltime)/len(Ltime)
        #print(f'mean time: {round(mean_time/1000,3)} sec ({round(mean_time/mean_rounds/1000,3)} sec / round)')

    mean_coproba_measured = sum(Lcopm)/len(Lcopm) 
    Lcopm=np.array(Lcopm)
    print(f'mean crossoverProba measured: {round(mean_coproba_measured,5)}, min: {round(min(Lcopm),5)} max: {round(max(Lcopm),5)} and {len(Lcopm[Lcopm>p])} > p')
    print(f'match cnt_zero != 0 and failed : {match_fail} /{nbTest-success-false_pos}')
    print(f'match cnt_zero != 0 and success : {match_success} /{success+false_pos}')
    
    
#    probability = 0.4
#    n = 8
##    code = np.random.choice([0,1],size = n)
#
#    code = np.zeros(n,dtype=np.int8)
#    received, postProba = LDPC.BSC_channel(code, crossoverProba= probability)
#    matrix = LDPC.input_generation_regularLDPC(n,3,4,postProba,10)
#    print(matrix)    
#    lengths = [12]
#    w_c = 3
#    w_r = 4
#    for length in lengths:
#        degreeOfNode = np.array([2,3,4,1,0,1,0,2,4,0,1,0])
#        start1 = time.time()
#        matrixPEG = LDPC.matrix_generation_PEG(degreeOfNode,int(length*w_c/w_r),length)
#        end1= time.time()
#        print(f"PEG takes {end1 - start1}")
#        print(matrixPEG.toarray())
#        start2 = time.time()
#        matrixNormal = LDPC.matrix_generation(length, w_c, w_r, seed = 10)
#        end2 = time.time()
#        print(f"Normal MG takes {end2 - start2}")
#        print(matrixNormal.toarray())
#        print(f"Number of cycle of size 4 for matrix generated by PEG is : {LDPC.count_cycle_size_four(LDPC.create_lookup(matrixPEG))}")
#        print(f"Number of cycle of size 4 for matrix generated by normal method is : {LDPC.count_cycle_size_four(LDPC.create_lookup(matrixNormal))}")
    