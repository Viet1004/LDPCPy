import matplotlib.pyplot as plt 
from math import log2

def entropy(error):
    return -error*log2(error) - (1-error)*log2(1-error)

def secret_keyrate(error, correction_rate):
    return 1 - entropy(error) - correction_rate

def draw_graph():
    p_set = [0.02,0.05,0.07]
    i = 0
    for p in p_set:
        end_point = 1 - entropy(p)
        start_point = entropy(p)
        x_set = [start_point + 0.01*i for i in range(int((end_point-start_point)/0.01))]
        y_set = [secret_keyrate(p,x) for x in x_set]
#        print("X_set:", x_set)
#        print("Y_set:", y_set)
#        plt.figure(i)
        i += 1
        plt.plot(x_set,y_set, label = f"p = {p}")
        plt.ylabel("secret key rate")
        plt.xlabel("w_c/w_r")
        plt.legend()
        plt.xlim(0,1)
        plt.ylim(0,1)

    plt.show() 

if __name__ == "__main__":
    draw_graph()