from django.db import models
from training_data.models import TrainingData
from input_data.models import InputData
from snapshots.models import Snapshot

# Create your models here.

class TrainingData(models.Model):
	width = models.FloatField()
	length = models.FloatField()
	color = models.FloatField()
	training_data = models.ForeignKey(TrainingData, on_delete = models.CASCADE, related_name = 'training_data')

	def __str__(self):
		return str(self.width) + ", " + str(self.length) + " = " + str(self.color)

class InputData(models.Model):
	width = models.FloatField()
	length = models.FloatField()
	input_data = models.ForeignKey(InputData, on_delete = models.CASCADE, related_name = 'input_data')

	def __str__(self):
		return str(self.width) + ", "  + str(self.length)

class Weight(models.Model):
	value = models.FloatField()
	snapshot = models.ForeignKey(Snapshot, on_delete = models.CASCADE, related_name = 'weight_snapshot')
	layer = models.IntegerField()

class Bias(models.Model):
	value = models.FloatField()
	snapshot = models.ForeignKey(Snapshot, on_delete = models.CASCADE, related_name = 'bias_snapshot')
	layer = models.IntegerField()