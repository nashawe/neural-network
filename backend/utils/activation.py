import numpy as np

def sigmoid(x):
    x = np.clip(x, -500, 500)  # Prevent overflow
    return 1 / (1 + np.exp(-x))

def deriv_sig(x):
    sig_x = sigmoid(x)  # Ensure x is passed through sigmoid first
    return sig_x * (1 - sig_x)

def tanh(x): #uses built 
    return np.tanh(x)

def deriv_tanh(x):
    return 1 - np.tanh(x) ** 2

def relu(x):
    return np.maximum(0, x)

def deriv_relu(x):
    return (x > 0).astype(float)

def softmax(x):
    # x: shape (batch_size, n_classes)
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

