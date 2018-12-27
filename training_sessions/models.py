from django.db import models
from flavors.models import Flavor

# Create your models here.

class TrainingSession(models.Model):
	name = models.CharField(max_length = 50)
	flavor = models.ForeignKey(Flavor, on_delete = models.CASCADE)
	hidden_layers = models.CharField(max_length = 100)
	create_timestamp = models.DateTimeField(auto_now_add = True)
	status = models.CharField(max_length = 10, default = "done")

	def __str__(self):
		return self.flavor.name + " - " + self.name

	def layer_sizes(self):
		sizes = [self.flavor.number_of_input_neurons]

		hidden_layers = str(self.hidden_layers).split(',')
		for hidden_layer in hidden_layers:
			sizes.append(int(hidden_layer))

		sizes.append(self.flavor.number_of_output_neurons)

		return sizes