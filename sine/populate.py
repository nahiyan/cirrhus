from snapshots.models import Snapshot
from .models import Weight, Bias

def populate_weights_biases(snapshot, model):
	flattened_weights_objects, flattened_biases_objects = [], []
	
	for i in range(len(model.layer_sizes) - 1):
		current_layer_weights = model.weights[i]
		current_layer_biases = model.biases[i]

		flattened_weights = current_layer_weights.flatten()
		flattened_biases = current_layer_biases.flatten()

		for flattened_weight in flattened_weights:
			flattened_weights_objects.append(
				Weight(
					value = flattened_weight,
					snapshot = snapshot,
					layer = i))

		for flattened_bias in flattened_biases:
			flattened_biases_objects.append(
				Bias(
					value = flattened_bias,
					snapshot = snapshot,
					layer = i))

	Weight.objects.bulk_create(flattened_weights_objects)
	Bias.objects.bulk_create(flattened_biases_objects)
