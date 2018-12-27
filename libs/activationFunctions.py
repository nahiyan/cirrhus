import numpy as np

def tan_h (x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

def tan_h_prime(x):
    return 1 - sigmoid(x) ** 2

def relu(x):
    return np.log(1 + np.exp(x))
def relu_prime (x):
    return np.exp(x) / (1 + np.exp(x))

def sigmoid (x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime (signal):
    return np.exp(-signal)/((1+np.exp(-signal))**2)