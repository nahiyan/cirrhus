from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import TrainingData
from flavors.models import Flavor

# Create your views here.

def list(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)
	training_data_list = TrainingData.objects.filter(flavor = flavor)

	context = {
		'flavor': flavor,
		'training_data_list': training_data_list,
	}

	return render(request, "training_data/list.html", context)


def create(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)

	if request.method == "POST":
		name = request.POST['name']

		TrainingData.objects.create(
			name = name,
			flavor = flavor)

		messages.success(request, "Training Data created successfully!")

		return redirect(
			"training_data:list",
			flavor_machine_name = flavor.machine_name)

	context = {
		'flavor': flavor
	}

	return render(request, "training_data/create.html", context)


def delete(request, training_data_id):
	training_data = \
		get_object_or_404(
			TrainingData,
			pk = training_data_id)
	flavor = training_data.flavor

	if request.method == "POST":
		training_data.delete()

		messages.success(request, "Training Data deleted successfully!")

		return redirect(
			"training_data:list",
			flavor_machine_name = flavor.machine_name)

	context = {
		'training_data': training_data,
		'flavor': flavor,
	}

	return render(request, "training_data/delete.html", context)