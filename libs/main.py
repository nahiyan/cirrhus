import math
import numpy as np
import neuralnet as nn

layer_sizes = [1, 3, 2, 1]

# linespace = np.array([ np.linspace(0, 2 * math.pi, 100) ])
# input_layer = linespace.T
# examples = np.sin(input_layer)

# examples = \
# 	[
# 		[1],
# 	    [0],
# 	    [1],
# 	    [0],
# 	    [1],
# 	    [0],
# 	    [1],
# 	    [0],
# 	]

# init_model = \
#     nn.Model(
#         weights = nn.random_weights(layer_sizes),
#         biases = nn.random_biases(layer_sizes),
#         layer_sizes = layer_sizes,
#         examples = examples)

# input_layer = \
# 	[
# 	    [3, 1.5],
# 	    [2, 1],
# 	    [4, 1.5],
# 	    [3, 1],
# 	    [3.5, .5],
# 	    [2, .5],
# 	    [5.5, 1],
# 	    [1, 1],
# 	]

# nn.predict_sine(
#     nn.train(
#         times = 3,
#         stochastic = True,
#         decrease_alpha = False,
#         alpha = 0.01,
#         debug = False,
#         model = \
#             nn.insert_input_layer(
#                 input_layer, init_model)))