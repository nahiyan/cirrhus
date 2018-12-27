from django.shortcuts import render, get_object_or_404
from .models import Flavor

# Create your views here.

def index (request):
	flavors = Flavor.objects.all

	if flavors.count() == 0:
		Flavor.objects.bulk_create(
			[
				Flavor(
					name = "Sine",
					machine_name = "sine",
					number_of_input_neurons = 1,
					number_of_output_neurons = 1),
				Flavor(
					name = "Flowers",
					machine_name = "flowers",
					number_of_input_neurons = 2,
					number_of_output_neurons = 1)
			])

	context = {
		'flavors': flavors
	}

	return render(request, "flavors/index.html", context)