from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import InputData
from flavors.models import Flavor

# Create your views here.

def list(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)
	input_data_list = InputData.objects.filter(flavor = flavor)

	context = {
		'flavor': flavor,
		'input_data_list': input_data_list,
	}

	return render(request, "input_data/list.html", context)


def create(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)

	if request.method == 'POST':
		name = request.POST['name']

		InputData.objects.create(
			name = name,
			flavor = flavor)

		messages.success(request, "Input Data created successfully!")

		return redirect("input_data:list", flavor_machine_name = flavor_machine_name)

	context = {
		'flavor': flavor,
	}

	return render(request, "input_data/create.html", context)

def delete(request, input_data_id):
	input_data = get_object_or_404(InputData, pk = input_data_id)
	flavor = input_data.flavor

	if request.method == 'POST':
		input_data.delete()

		messages.success(request, "Deleted input data successfully!")

		return redirect("input_data:list", flavor_machine_name = flavor.machine_name)

	context = {
		'input_data': input_data,
		'flavor': flavor,
	}

	return render(request, "input_data/delete.html", context)