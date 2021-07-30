from operator import pos
import timeit
import LDPC
import numpy as np
import time
from scipy.sparse import csc_matrix 

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

@profile
@timerfunc
def run(n,w_c,w_r, probability):
    numberOfTest = 20
    success = 0
    seed = 10
#    while(True):
#        if LDPC.check_cycle(LDPC.create_lookup(LDPC.matrix_generation(n,w_c,w_r,seed))):
#            break
#        seed += 1
    code = np.random.choice([0,1],size = n) 
    matrix = LDPC.matrix_generation(n,w_c,w_r,seed)
    lookup = LDPC.create_lookup(matrix)
    matrix = csc_matrix(matrix)
    syndrome = matrix.dot(code)
    
    for i in range(numberOfTest):
        received, postProba = LDPC.BSC_channel(code, crossoverProba= probability)
        lookup = LDPC.create_input(lookup, postProba)
        verifi, res = LDPC.MessagePassing(lookup, matrix, postProba, syndrome)
        if verifi:
            success += 1      
    print("======================================================================")
    print(f"There are {success} successes out of {numberOfTest} tests")
    print("======================================================================")

def test():
    n1 =  [128,256,512,1024,2048]
#    n1 = [1024]
    set1 = [(3,4)]
    n2 = [125,250,500,1000,2000]
#    n2 = [1000]
    set2 = [(3,5),(4,5)]
    n3 = [120,240,480,960,1920]
#    n3 = [960]
    set3 = [(4,6),(5,6)]
    proba = (0.02,0.05,0.1)
    for n in n1:
        for set in set1:
            for p in proba:
                print(f"n:{n} w_c: {set[0]}, w_r: {set[1]}, p: {p}")
                run(n,set[0],set[1],p)

    for n in n2:
        for set in set2:
            for p in proba:
                print(f"n:{n} w_c: {set[0]}, w_r: {set[1]}, p: {p}")
                run(n,set[0],set[1],p)
    
    for n in n3:
        for set in set3:
            for p in proba:
                print(f"n:{n} w_c: {set[0]}, w_r: {set[1]}, p: {p}")
                run(n,set[0],set[1],p)

if __name__ == "__main__":
    test()
