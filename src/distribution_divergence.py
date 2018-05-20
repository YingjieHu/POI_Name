


import numpy as np
import matplotlib.pyplot as plt


def softmax(x):
    orig_shape = x.shape

    if len(x.shape) > 1:
        # Matrix
        ### YOUR CODE HERE
        x = np.exp(x - np.max(x, 1, keepdims= True))
        x /= np.sum(x, 1, keepdims = True)
        ### END YOUR CODE
    else:
        # Vector
        ### YOUR CODE HERE
        x = np.exp(x - np.max(x))
        x /= np.sum(x)
        ### END YOUR CODE

    assert x.shape == orig_shape
    return x


def normalize(x):
    orig_shape = x.shape

    if len(x.shape) > 1:
        # Matrix
        ### YOUR CODE HERE
        #x = np.exp(x - np.max(x, 1, keepdims= True))
        x /= np.sum(x, 1, keepdims = True)
        ### END YOUR CODE
    else:
        # Vector
        ### YOUR CODE HERE
        #x = np.exp(x - np.max(x))
        x /= np.sum(x)
        ### END YOUR CODE

    assert x.shape == orig_shape
    return x


from scipy.stats import entropy
from numpy.linalg import norm

def JSD(P, Q):
    _P = P / norm(P, ord=1)
    _Q = Q / norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    return 0.5 * (entropy(_P, _M) + entropy(_Q, _M))


def calculate_divergence():

    data = np.empty([7,10])
    
    category_list = []
    metro_list = []
    
    i = -1
    with open('../word_metro_cate_usage_refined.csv','r') as fr:
        for line in fr:
            splitted = line.split(',')
            if i== -1:
                for j in range(1,11):
                    category_list.append(splitted[j].strip())
            else:
                metro_list.append(splitted[0])
                #print(splitted[0])
                for j in range(1,11):
                    data[i,j-1] = splitted[j]
                
            i += 1
        
    #data = softmax(data)   
    data = normalize(data)
    
    
    sum = 0.0
    for i in range(6):
        for j in range(i+1,7):
            sum += JSD(data[i], data[j])
            
    print(sum/21.0)
    
    

if __name__ == '__main__':
    calculate_divergence()
    #data = np.array([2.0,1.0,2.0])
    #print(normalize(data))
