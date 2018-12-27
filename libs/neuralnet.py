from random import randint
import math
import json
import numpy as np
# from matplotlib import pyplot as plt

from . import activationFunctions as af


# the grand model
class Model:
    def __init__(self,
            weights = [],
            biases = [],
            layer_sizes = [],
            layers = [],
            non_activated_layers = [],
            examples = [],
            dJdW_list = [],
            dJdB_list = [],
            costs = []):

        self.weights = weights
        self.biases = biases
        self.layer_sizes = layer_sizes
        self.layers = layers
        self.non_activated_layers = non_activated_layers
        self.examples = examples
        self.dJdW_list = dJdW_list
        self.dJdB_list = dJdB_list
        self.costs = costs


# imperative


def random_weights(layer_sizes):
    weights = []
    for i in range(len(layer_sizes)):
        # skip the first layer, as it has no previous layer
        if i != 0:
            # np.random.seed(0)
            weights.append(
                np.random.randn(
                    layer_sizes[i - 1], layer_sizes[i]))

    return weights

def random_biases(layer_sizes):
    biases = []

    for i in range(len(layer_sizes)):
        # skip the first layer, as it has no previous layer
        if i != 0:
            # np.random.seed(0)
            biases.append(
                np.random.randn(1, layer_sizes[i]))

    return biases


# functional


def activation(x):
    return af.tan_h(x)


def activation_prime(x):
    return af.tan_h_prime(x)


# get a specific layer
def layer(i, model):
    return np.array(model.layers[i])


# get weights between i and i + 1 layer
def layer_weights(i, model):
    return np.array(model.weights[i])


# get biases of i layer
def layer_biases(i, model):
    # offset of -1 since there is no bias for index layer
    return np.array(model.biases[i - 1])


# get a specific non-activated version of a layer with index i
def non_activated_layer(i, model):
    # since there's no input layer, index has offset of -1
    return np.array(model.non_activated_layers[i - 1])


# simply get the last layer
def last_layer(model):
    output_layer_index = number_of_layers(model) - 1

    return np.array(layer(output_layer_index, model))


# simply get the last non-activated layer
def last_non_activated_layer(model):
    output_layer_index = number_of_layers(model) - 1

    last_non_activated_layer = []
    for i in range(number_of_layers(model)):
        last_non_activated_layer.append(layer(i, model))

    return np.array(non_activated_layer(output_layer_index, model))


# imperative
def identity(n, m):
    matrix = []

    # generate row
    row = []
    for j in range(m):
        row.append(1)

    # add the rows to the matrix
    for i in range(n):
        matrix.append(row)

    return np.array(matrix)


def previous_layer(i, model):
    layer(i - 1, model)


def number_of_layers(model):
    return len(model.layer_sizes)


def number_of_input_layers(model):
    return len(model.layers[0])


# get output layer from input layer
def output_layer(input_layer, model):
    new_model = model
    new_model.layers = [input_layer]

    return last_layer(
        forward_propagate(new_model))


def insert_input_layer(input_layer, model):
    new_model = model
    new_model.layers = [ input_layer ]
    return new_model


# forward propagation to a new layer of index i based on the previous layer
def forward_propagate_step(i, model):
    output_layer_index = number_of_layers(model) - 1
    previous_layer = layer(i - 1, model)

    # weights between previous layer and current layer
    weights = layer_weights(i - 1, model)

    # biases of current layer
    biases = layer_biases(i, model)

    non_activated_new_layer = \
        np.dot(previous_layer, weights) + np.dot(model.identity_biases.T, biases)

    new_layer = \
        activation(
            non_activated_new_layer)

    new_model = model
    new_model.layers.append(
        new_layer)
    new_model.non_activated_layers.append(
        non_activated_new_layer)

    if i != output_layer_index:
        return forward_propagate_step(i + 1, new_model)
    else:
        return new_model

def forward_propagate(model):
    new_model = model
    new_model.layers = [ model.layers[0] ]
    new_model.non_activated_layers = []

    if not hasattr(model, 'identity_biases'):
        new_model.identity_biases = \
            identity(1, number_of_input_layers(model))

    return forward_propagate_step(1, new_model)


def backward_propagate_step(delta, i, model):
    dJdW = \
        np.dot(
            layer(i - 1, model).T, delta)

    dJdB = \
        np.dot(
            model.identity_biases, delta)

    model.dJdW_list.append(dJdW)
    model.dJdB_list.append(dJdB)

    if i == 1:
        model.dJdW_list.reverse()
        model.dJdB_list.reverse()

        return model
    else:
        new_delta = \
            np.dot(delta, model.weights[i - 1].T) * \
            np.array(
                activation_prime(
                    non_activated_layer(i - 1, model)))

        return backward_propagate_step(new_delta, i - 1, model)


def backward_propagate(model):
    new_model = model
    new_model.dJdW_list = []
    new_model.dJdB_list = []

    delta = \
        (last_layer(new_model) - new_model.examples) * \
        activation_prime(last_non_activated_layer(new_model))

    return backward_propagate_step(delta, number_of_layers(new_model) - 1, new_model)


# calculate the cost
def cost(model):
    return 0.5 * np.sum(np.square(last_layer(model) - model.examples))

def stochastic_model(model):
    random_input_layer_index = \
        randint(0, number_of_input_layers(model) - 1)

    layers = []
    for i in range(number_of_layers(model)):
        layers.append(
            np.array(
                [ model.layers[i][random_input_layer_index] ]))

    non_activated_layers = []
    for i in range(number_of_layers(model) - 1):
        non_activated_layers.append(
            np.array(
                [ model.non_activated_layers[i][random_input_layer_index] ]))

    examples = \
        [ model.examples[random_input_layer_index] ]

    s_model = Model(
        weights = model.weights,
        biases = model.biases,
        layer_sizes = model.layer_sizes,
        layers = layers,
        non_activated_layers = non_activated_layers,
        examples = examples,
        dJdW_list = model.dJdW_list,
        dJdB_list = model.dJdB_list,
        costs = model.costs)
    return s_model


# imperative

def train(model,
    alpha = 0.01,
    times = 1,
    stochastic = False,
    debug = True,
    decrease_alpha = True,
    callback_interval = 5000,
    callback = None):
    # model.costs = []
    model = forward_propagate(model)
    backed_up_model = model

    for i in range(times):
        print("Training " + str(i + 1) + "x")

        for j in range(10000):
            if stochastic:
                model = \
                    forward_propagate(
                        stochastic_model(backed_up_model))

            if decrease_alpha:
                alpha /= 1.00001
            
            model = \
                forward_propagate(
                    backward_propagate(model))

            for k in range(number_of_layers(model) - 1):
                model.weights[k] -= alpha * model.dJdW_list[k]
                model.biases[k] -= alpha * model.dJdB_list[k]
            
            # if debug and j % 100 == 0:
            #     model.costs.append(
            #         cost(
            #             forward_propagate(model)))

            if callback != None:
                if j % callback_interval == 0:
                    # use the backed up model with the new weights and biases
                    callback_model = backed_up_model
                    callback_model.weights = model.weights
                    callback_model.biases = model.biases

                    callback_model.cost = \
                        cost(
                            forward_propagate(
                                callback_model))

                    callback(callback_model)
    
    # if debug:
    #     plt.plot(model.costs)
    #     plt.show()

    # model.costs = []

    if stochastic:
        model.layers = backed_up_model.layers
        model.non_activated_layers = backed_up_model.non_activated_layers
        model.examples = backed_up_model.examples

    return forward_propagate(model)


# functional

# def predict_flowers (model):
    # lengths, widths, colors = [], [], []

    # for i in range(number_of_input_layers(model)):
    #     lengths.append(layer(0, model)[i][0])
    #     widths.append(layer(0, model)[i][1])
    #     if last_layer(model)[i][0] >= 0.5:
    #         colors.append('r')
    #     else:
    #         colors.append('b')
    
    # plt.scatter(lengths, widths, 100, colors)
    # plt.show()

    # return model