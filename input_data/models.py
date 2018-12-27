from django.db import models
from flavors.models import Flavor

# Create your models here.

class InputData(models.Model):
	name = models.CharField(max_length = 50)
	flavor = models.ForeignKey(Flavor, on_delete = models.CASCADE)
	create_timestamp = models.DateTimeField(auto_now_add = True)
	number_of_entries = models.IntegerField(default = 0)