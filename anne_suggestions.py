import timeit
import LDPC 
import numpy as np
import time
from scipy.sparse import csc_matrix, csr_matrix 
import gc

## suggestion to create the lookup table from the sparse matrix rather than from the 'big' matrix
## also use gc: garbage collector (l.81) to empty the memory of the 'big' matrix once the sparse one is there. 

## just a basic time function from google, in ms
def current_milli_time():
    return round(time.time() * 1000)

## takes a csc matrix as input and return a lookup table
def create_lookup2(matrix, w_r, w_c):
  #m,n = np.shape(matrix)
  m,n = matrix.get_shape()
  lookup = {}
  # we first remap the row of H to the neighborR of the lookup 
  for i in range(m):
    R = matrix.getrow(i).tocoo().col
    for k in range(w_r):
      neighborR1 = np.delete(R,k) 
      neighborR = []
      for l in range(w_r-1):
        neighborR.append((i,neighborR1[l]))
      data = LDPC.Data(neighborC = [], neighborR = neighborR, q_0 = 0, q_1 = 0, r_0 = 0, r_1 = 0)
      lookup[(i,R[k])] = data
      #print(lookup)

  # then we remap the columns of H to the neighborR field of the lookup
  for x in lookup:
    if not lookup[x].neighborC:
      (i,j) = x
      #print(f'x {x}')
      C = matrix.getcol(j).tocoo().row
      for k in range(w_c):
        neighborC1 = np.delete(C,k) 
        neighborC = []
        for l in range(w_c-1):
          neighborC.append((neighborC1[l],j))
        data = lookup[(C[k],j)]
        data.neighborC = neighborC
  return lookup


def test():
    n =  2000
    w_c = 4
    w_r = 10
    seed = 10
    n = w_r*(n//w_r)
    time0=current_milli_time()
    matrix = LDPC.matrix_generation(n,w_c,w_r,seed)
    time1=current_milli_time() 
    print("time to create H: {} ms".format(time1-time0))
    #print(matrix)

    codeword = np.random.choice([0,1],size = n) 
    time1=current_milli_time() 
    syndrome = np.dot(matrix,codeword)%2
    #print(np.any(syndrome))
    time2=current_milli_time() 
    print("time Hx with standard: {} ms".format(time2-time1))


    print("lookup init")
    time1=current_milli_time() 
    lookup = LDPC.create_lookup(matrix)
    time2=current_milli_time() 
    print("time to create lookup: {} ms".format(time2-time1))
    #print(lookup)

    time1=current_milli_time() 
    matrix1 = csc_matrix(matrix)
    time2=current_milli_time() 
    print("time to compress H: {} ms".format(time2-time1))
    #print(matrix1)

    del matrix
    gc.collect()


    print("lookup new")
    time1=current_milli_time()     
    lookup = create_lookup2(matrix1,w_r,w_c)
    time2=current_milli_time() 
    print("time to create lookup 2: {} ms".format(time2-time1))
    #print(lookup)

    time1=current_milli_time()  
    syndrome1 = matrix1.dot(codeword)%2
    #print(np.any(syndrome1))
    time2=current_milli_time() 
    print("time Hx with csc: {} ms".format(time2-time1))




if __name__ == "__main__":
    test()
