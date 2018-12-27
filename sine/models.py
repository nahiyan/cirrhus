from django.db import models
from training_data.models import TrainingData
from input_data.models import InputData
from snapshots.models import Snapshot

# Create your models here.

class TrainingData(models.Model):
	x = models.FloatField()
	y = models.FloatField()
	training_data = models.ForeignKey(TrainingData, on_delete = models.CASCADE)

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class InputData(models.Model):
	x = models.FloatField()
	input_data = models.ForeignKey(InputData, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.x)

class Weight(models.Model):
	value = models.FloatField()
	snapshot = models.ForeignKey(Snapshot, on_delete = models.CASCADE)
	layer = models.IntegerField()

class Bias(models.Model):
	value = models.FloatField()
	snapshot = models.ForeignKey(Snapshot, on_delete = models.CASCADE)
	layer = models.IntegerField()