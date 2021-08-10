import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, coo_matrix, vstack
from LDPC import matrix_generation, verification
import random
import time

def current_milli_time():
    return round(time.time() * 1000)


def BSC_channel(codeword, p: float):
  n = codeword.shape[0]
  received = np.copy(codeword)
  postproba = np.array([])
  for i in range(n):
    if random.random() < p:
      received[i] = int(codeword[i]^1)
  #   if received[i] == 0:
  #     postproba=np.append(postproba,np.log((1-p)/p))
  #   else:
  #     postproba=np.append(postproba,np.log(p/(1-p)))
  postproba=(1-received)*(1-p)+received*p
  postproba=np.log(postproba/(1-postproba))
  return received, postproba


def matrix_input(n,w_c,w_r,seed,p,received):
  data=(1-received)*(1-p)+received*p
  data=np.log(data/(1-data))
  indptr = np.arange(0,n+1,w_r)
  indices = np.arange(n)
  matrix = csr_matrix((data,indices,indptr))
  for i in range(w_c -1):
    temp = np.copy(indices)
    np.random.RandomState(seed = seed*i).shuffle(temp)
    matrix = vstack([matrix,csr_matrix((data[temp], temp, indptr))])
  return matrix

def ftanh(w):
  t=np.exp(w)
  return (t-1)/(t+1)


def horizontal_run(matrix, syndrome, w_r, m):
   #for x in lookup:
   for i in range(m):
    R2=np.array([])
    #for row_neighbor in lookup[x].neighborR:
    for k in range(w_r):
      R1=np.delete(matrix[i].data,k)
      #res *= ftanh(lookup[row_neighbor].q_0)
      res=1
      for j in range(w_r-1):
        res *= ftanh(R1[j])
      R2=np.append(R2,np.log((1+(-1)**syndrome[i]*res)/(1-(-1)**syndrome[i]*res)))
    matrix[i,matrix[i].tocoo().col]=R2

def vertical_run(matrix, post_proba, w_c, n):

  string=np.zeros(n)

  #for x in lookup:
  for i in range(n):
    beta = post_proba[i]
    #for col_neighbor in lookup[x].neighborC:
    C2=np.array([])
    for k in range(w_c):
      C1=np.delete(matrix[i].data,k)
      #beta += lookup[col_neighbor].r_0
      C2=np.append(C2,beta+C1.sum())
    beta+=matrix[i].data.sum()
    matrix[i,matrix[i].tocoo().col]=C2
    if beta > 0:
      string[i] = 0
    else:
      string[i] = 1
  return string


def horizontal_run_block(matrix, syndrome, w_c, w_r, m, n):
 
    r=n//w_r
    #w_c=1
    i=0
    matrix2=matrix[i*r:(i+1)*r]
    #print(matrix2)
    D=ftanh(matrix2.data)
    syndrome2=syndrome[i*r:(i+1)*r]
    Ptot= np.zeros((r,w_r))
    for k in range(w_r):
      indptr = np.arange(k,n,w_r)
      L=np.delete(D,indptr)
      #print(L)
      l=len(L)
      M=L.reshape(l//(w_r-1),w_r-1)
      #print(M)
      P=M.prod(axis=1)
      #print(P)
      P=(-1)**syndrome2*P
      P=np.log((1+P)/(1-P))
      Ptot[:,k]=P
      #print(Ptot)
    Ptot=np.reshape(Ptot,(n,))
    matrix2.data=Ptot
    #matrix[i*r:(i+1)*r].data=Ptot
    newmatrix = csr_matrix(matrix2)

    for i in range(1,w_c):
      matrix2=matrix[i*r:(i+1)*r]
      #print(matrix2)
      D=ftanh(matrix2.data)
      syndrome2=syndrome[i*r:(i+1)*r]
      Ptot= np.zeros((r,w_r))
      for k in range(w_r):
        indptr = np.arange(k,n,w_r)
        L=np.delete(D,indptr)
        #print(L)
        l=len(L)
        M=L.reshape(l//(w_r-1),w_r-1)
        #print(M)
        P=M.prod(axis=1)
        #print(P)
        P=(-1)**syndrome2*P
        P=np.log((1+P)/(1-P))
        Ptot[:,k]=P
        #print(Ptot)
      Ptot=np.reshape(Ptot,(n,))
      matrix2.data=Ptot
      #matrix[i*r:(i+1)*r].data=Ptot
      newmatrix = vstack([newmatrix,csr_matrix(matrix2)])
    return newmatrix


def new_horizontal_run(matrix, syndrome, w_c, w_r, m, n):
 
    nbo = w_r*m

    D=ftanh(matrix.data)
    Ptot= np.zeros((m,w_r))

    for k in range(w_r):
      indptr = np.arange(k,nbo,w_r)
      L=np.delete(D,indptr)
      #print(L)
      l=len(L)
      M=L.reshape(l//(w_r-1),w_r-1)
      #print(M)
      P=M.prod(axis=1)
      #print(P)
      P=(-1)**syndrome*P
      P=np.log((1+P)/(1-P))
      Ptot[:,k]=P
      #print(Ptot)
    Ptot=np.reshape(Ptot,(nbo,))
    matrix.data=Ptot

    #return newmatrix


def new_vertical_run(matrix, postproba, w_c, w_r, m, n):

   
    matrix=matrix.transpose().tocsr()
    nbo = w_c*n

    D=matrix.data
    Ptot= np.zeros((n,w_c))
    for k in range(w_c):
      indptr = np.arange(k,nbo,w_c)
      L=np.delete(D,indptr)
      #print(L)
      l=len(L)
      M=L.reshape(l//(w_c-1),w_c-1)
      #print(M)
      P=M.sum(axis=1)
      #print(P)
      P=postproba+P
      Ptot[:,k]=P
      #print(Ptot)
    Ptot=np.reshape(Ptot,(nbo,))
    matrix.data=Ptot
    #newmatrix = csr_matrix(matrix2)
    l=len(D)
    M=D.reshape(l//(w_c),w_c)
    #print(M)
    beta=M.sum(axis=1)
    beta=postproba+beta
    string=np.array(beta<=0)
    string=string.astype(int)

    return (matrix,string)


def MessagePassing(matrix0, matrix, postproba, syndrome, w_c, w_r, itermp):
  
  m,n = matrix.get_shape()
  #print(f'm:{m}, n: {n}')
  time1=current_milli_time()

  for i in range(itermp):
    #print("round: {}".format(i))
    #    print("=======================Horizontal Round===========================")
    #time00=current_milli_time()
    #horizontal_run(matrix, syndrome, w_r,m)
    #matrix=horizontal_run_block(matrix, syndrome, w_c, w_r,m, n)
    new_horizontal_run(matrix, syndrome, w_c, w_r,m, n)
    #print(matrix)
    #time01=current_milli_time()
    #time=time01-time00
    #print("time for horizontal_run: {} ms".format(time))
    #print(matrix)
    #    print("=======================Vertical Round===========================")
    #time00=current_milli_time()
    #string = vertical_run(matrix.transpose(), postproba,w_c,n)
    matrix, string = new_vertical_run(matrix, postproba,w_c,w_r,m,n)
    matrix=matrix.transpose().tocsr()
    #time01=current_milli_time()
    #time=time01-time00
    #print("time for vertical_run: {} ms".format(time))
    #print(matrix)
    #time00=current_milli_time()
    if verification(matrix0, string, syndrome):
      #time01=current_milli_time()
      #time=time01-time00
      #print("time to verif: {} ms".format(time))
      #print("success")
      time2=current_milli_time()
      print("round: {}".format(i))
      time=time2-time1
      print("time to decode: {} ms".format(time))
      return (1, i+1, time, string)
    else:
        #time01=current_milli_time()
        #time=time01-time00
        #print("time for verif: {} ms".format(time))
        continue
  time2=current_milli_time()
  #print("round: {}".format(i))
  time=time2-time1
  print("time to not decode: {} ms in {} iter ({} sec / iter)".format(time,itermp,round(time/itermp/1000,3)))
  return (0, i+1, time, None)

def runatest():
  time00=current_milli_time()
  n =  1000000
  w_c = 3
  w_r = 6
  p=0.05
  #seed = int(sys.argv[1])
  seed = 10
  #print(f'seed: {seed}')
  n = w_r*(n//w_r)
  print("n={} wc={} wr={} p={}".format(n,w_c,w_r,p))
  codeword = np.random.choice([0,1],size = n)
  time0=current_milli_time()
  matrix0 = matrix_generation(n,w_c,w_r,seed)
  time1=current_milli_time() 
  print("time for gen H: {} ms".format(time1-time0))
  #time0=current_milli_time()
  syndrome = matrix0.dot(codeword)%2
  #time1=current_milli_time() 
  #print("time to compute Hc: {} ms".format(time1-time0))

  time11=current_milli_time() 
  print("time before loop: {} ms".format(time11-time00))


  itertest=5
  itermp=250
  success=0
  Lrounds=[]
  Ltime=[]
  false_pos = 0

  time00=current_milli_time()

  for i in range(itertest):
    time0=current_milli_time()
    received, postproba = BSC_channel(codeword, p)
    time1=current_milli_time() 
    print("time to comp bsc channel: {} ms".format(time1-time0))
    time0=current_milli_time()
    matrix=matrix_input(n,w_c,w_r,seed,p,received)
    time1=current_milli_time() 
    print("time for gen H_Q: {} ms".format(time1-time0))
    #print(matrix)
    status, rounds, time, string = MessagePassing(matrix0, matrix, postproba, syndrome, w_c, w_r, itermp)
    if status:
      time0=current_milli_time()
      if np.array_equal(string,codeword):
        success += 1
      else:
        false_pos += 1
      time1=current_milli_time() 
      print("time for check false pos: {} ms".format(time1-time0))
      Lrounds.append(rounds)
      Ltime.append(time) 
    
  if success > 0:
    mean_rounds = sum(Lrounds)/len(Lrounds)
    print(f'mean rounds: {round(mean_rounds,2)} min: {min(Lrounds)} max: {max(Lrounds)}')
    mean_time = sum(Ltime)/len(Ltime)
    print(f'mean time: {round(mean_time/1000,3)} sec ({round(mean_time/mean_rounds/1000,3)} sec / round)')
  print(f'success: {success} / {itertest}')
  print(f'false_pos: {false_pos} / {itertest}')

  time11=current_milli_time() 
  print("time in the loop: {} ms".format(time11-time00))


if __name__== '__main__':
  runatest()