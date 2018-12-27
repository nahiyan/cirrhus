from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Snapshot
from input_data.models import InputData

# Create your views here.

def detail(request, snapshot_id):
	snapshot = get_object_or_404(Snapshot, pk = snapshot_id)
	training_session = snapshot.training_session
	flavor = training_session.flavor
	input_data_list = InputData.objects.filter(flavor = flavor)

	context = {
		'flavor': flavor,
		'training_session': training_session,
		'snapshot': snapshot,
		'input_data_list': input_data_list,
	}

	return render(request, "snapshots/detail.html", context)


def delete(request, snapshot_id):
	snapshot = get_object_or_404(Snapshot, pk = snapshot_id)
	training_session = snapshot.training_session
	flavor = training_session.flavor

	if request.method == "POST":
		snapshot.delete()

		messages.success(request, "Snapshot deleted successfully!")
		return redirect(
			"training_sessions:detail",
			training_session_id = training_session.id)

	context = {
		'snapshot': snapshot,
		'training_session': training_session,
		'flavor': flavor,
	}

	return render(request, "snapshots/delete.html", context)