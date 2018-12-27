from django.db import models

# Create your models here.

class Flavor (models.Model):
	name = models.CharField(max_length = 50)
	number_of_input_neurons = models.IntegerField()
	number_of_output_neurons = models.IntegerField()
	machine_name = models.CharField(max_length = 40)

	def __str__(self):
		return self.name + "(" + self.machine_name + ")"