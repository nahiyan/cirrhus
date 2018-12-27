import numpy as np
import neuralnet as nn

def test_result(value, fail_message):
	if (value == 1):
		return "."
	else:
		return fail_message


# zero cost
def test_cost_is_zero(value):
	if (value == 0):
		return 1
	else:
		return 0


# non-zero cost
def test_cost_is_x(value, x):
	if (value == x):
		return 1
	else:
		return 0


def test_random_weights_is_5_by_6(result):
	n = len(result[0])
	m = len(result[0][0])
	if n == 5 and m == 6:
		return 1
	else:
		return 0


def test_random_biases_is_1_by_6(result):
	n = len(result[0])
	m = len(result[0][0])
	if n == 1 and m == 6:
		return 1
	else:
		return 0


def test_output_layer_is_1_by_3(result):
	n = len(result)
	m = len(result[0])
	if n == 1 and m == 3:
		return 1
	else:
		return 0


# zero cost
ZERO_COST = nn.cost(
	np.array([1, 0]), np.array([1, 0]))
print(
	test_result(
		test_cost_is_zero(ZERO_COST), "Cost should have been zero."))


# non-zero cost = 0.6348
NON_ZERO_COST = nn.cost(
	np.array([0.9, 0.64, 0.6, 0.3]), np.array([1, 0, 0, 1]))
print(
	test_result(
		test_cost_is_x(NON_ZERO_COST, 0.6348), "Cost should have been 0.6348."))


# random_weights generate n x m matrix
weights = \
	nn.random_weights([5, 6])
print(
	test_result(
		test_random_weights_is_5_by_6(weights), "Random weights should be 5 x 6"))


# random_biases generate 1 x n matrix
biases = \
	nn.random_biases([5, 6])
print(
	test_result(
		test_random_biases_is_1_by_6(biases), "Random biases be 1 x 6"))

# output_layer generate 1 x n matrix
input_layer = \
	np.array(
		[[1, 1]])

layer_sizes = [2, 3]

init_model = \
    nn.Model(
        weights = nn.random_weights(layer_sizes),
        biases = nn.random_biases(layer_sizes),
        layer_sizes = layer_sizes)

output_layer = \
	nn.output_layer(input_layer, init_model)
print(
	test_result(
		test_output_layer_is_1_by_3(output_layer), "Output layer be 1 x 3"))