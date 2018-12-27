from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from flavors.models import Flavor
from training_sessions.models import TrainingSession
from snapshots.models import Snapshot
from training_data.models import TrainingData
from input_data.models import InputData
from logs.models import CostLog

# Create your views here.

def list(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)
	training_sessions = TrainingSession.objects.filter(flavor = flavor)

	context = {
		'flavor': flavor,
		'training_sessions': training_sessions
	}

	return render(request, "training_sessions/list.html", context)


def detail(request, training_session_id):
	training_session = get_object_or_404(TrainingSession, pk = training_session_id)
	flavor = training_session.flavor
	snapshots = Snapshot.objects.filter(training_session = training_session).order_by('-id')
	logs = CostLog.objects.filter(snapshot__in = snapshots)
	input_data_list = InputData.objects.filter(flavor = flavor).order_by('-id')

	context = {
		'training_session': training_session,
		'flavor': flavor,
		'snapshots': snapshots,
		'logs': logs,
		'input_data_list': input_data_list,
	}

	return render(request, "training_sessions/detail.html", context)


def create(request, flavor_machine_name):
	flavor = get_object_or_404(Flavor, machine_name = flavor_machine_name)
	training_data_list = TrainingData.objects.filter(flavor = flavor)

	if request.method == "POST":
		name = request.POST['name']
		hidden_layers = request.POST['hidden_layers']
		
		new_training_session = TrainingSession.objects.create(
			name = name,
			hidden_layers = hidden_layers,
			flavor = flavor)

		return redirect(
			flavor_machine_name + ":initialize_training_session",
			training_session_id = new_training_session.id)


	context = {
		'flavor': flavor,
		'training_data_list': training_data_list
	}

	return render(request, "training_sessions/create.html", context)


def run(request, training_session_id):
    training_session = \
        get_object_or_404(TrainingSession, pk = training_session_id)
    flavor = training_session.flavor
    training_data_list = TrainingData.objects.filter(flavor = flavor)
    snapshots = Snapshot.objects.filter(training_session = training_session).order_by('-id')

    context = {
        'training_session': training_session,
        'flavor': flavor,
        'training_data_list': training_data_list,
        'snapshots': snapshots,
    }

    return render(request, "training_sessions/run.html", context)


def delete(request, training_session_id):
	training_session = \
		get_object_or_404(
			TrainingSession, pk = training_session_id)

	flavor = training_session.flavor

	if request.method == "POST":
		training_session.delete()

		messages.success(request, "Training Session deleted successfully!")
		return redirect(
			"training_sessions:list",
			flavor_machine_name = flavor.machine_name)

	context = {
		'flavor': flavor,
		'training_session': training_session,
	}

	return render(request, "training_sessions/delete.html", context)