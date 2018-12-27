import numpy as np
from . import neuralnet as nn

def generate_weights_and_biases_from_objects(
    weight_objects, bias_objects, layer_sizes):
    flattened_weights, flattened_biases = [], []

    # add layers
    for i in range(len(layer_sizes) - 1):
        flattened_weights.append([])
        flattened_biases.append([])

    # load the flattened arrays of weights and biases for each layers
    for weight_object in weight_objects:
        flattened_weights[int(weight_object.layer)].append(
            float(weight_object.value))

    for bias_object in bias_objects:
        flattened_biases[int(bias_object.layer)].append(
            float(bias_object.value))

    # reshape the flattened weights and biases
    weights, biases = [], []
    
    for i in range(len(layer_sizes) - 1):
        weights.append(
            np.array(flattened_weights[i]).reshape(
                [layer_sizes[i], layer_sizes[i + 1]]))

        biases.append(
            np.array(flattened_biases[i]).reshape(
                [1, layer_sizes[i + 1]]))

    return weights, biases