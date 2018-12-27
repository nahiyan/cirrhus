from django.shortcuts import render, get_object_or_404
from .models import Flavor

# Create your views here.

def index (request):
	context = {
		'flavors': Flavor.objects.all
	}

	return render(request, "flavors/index.html", context)