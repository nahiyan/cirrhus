from django.db import models
from snapshots.models import Snapshot

# Create your models here.

class CostLog(models.Model):
	cost = models.DecimalField(max_digits = 15, decimal_places = 5)
	snapshot = models.ForeignKey(Snapshot, on_delete = models.CASCADE)
	create_timestamp = models.DateTimeField(auto_now_add = True)