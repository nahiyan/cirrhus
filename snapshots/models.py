from django.db import models
from training_sessions.models import TrainingSession

# Create your models here.

class Snapshot(models.Model):
	name = \
		models.CharField(max_length = 50)
	training_session = \
		models.ForeignKey(TrainingSession, on_delete = models.CASCADE)
	create_timestamp = \
		models.DateTimeField(auto_now_add = True)