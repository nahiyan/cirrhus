from django.contrib import admin
from .models import TrainingData, Weight, Bias, InputData

# Register your models here.

admin.site.register(TrainingData)
admin.site.register(Weight)
admin.site.register(Bias)
admin.site.register(InputData)