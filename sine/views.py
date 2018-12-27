import math
import numpy as np

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from flavors.models import Flavor
from training_data.models import TrainingData
from input_data.models import InputData
from training_sessions.models import TrainingSession
from snapshots.models import Snapshot
from .models import TrainingData as SineTrainingData, Weight, Bias, InputData as SineInputData

from libs import neuralnet as nn

# Create your views here.

def run(request):
    flavor = get_object_or_404(Flavor, machine_name = 'sine')
    input_data_list = InputData.objects.filter(flavor = flavor).order_by('-id')
    training_sessions = TrainingSession.objects.filter(flavor = flavor).order_by('-id')

    if request.method == 'POST':
        input_data = get_object_or_404(InputData, pk = request.POST['input_data'])
        training_session = get_object_or_404(TrainingSession, pk = request.POST['training_session'])
        output_type = request.POST['output']
        compare = request.POST['compare']

        if 'snapshot' in request.POST:
            snapshot = get_object_or_404(Snapshot, pk = int(request.POST['snapshot']))
        else:
            snapshot = Snapshot.objects.filter(training_session = training_session).order_by('-id')[:1]

        from libs import neuralnet as nn

        layer_sizes = training_session.layer_sizes()

        weight_objects = Weight.objects.filter(snapshot = snapshot)
        bias_objects = Bias.objects.filter(snapshot = snapshot)

        from libs import helpers
        weights, biases = \
            helpers.generate_weights_and_biases_from_objects(
                weight_objects, bias_objects, layer_sizes)

        # prepare the input layer
        sine_input_data_list = \
            SineInputData.objects.filter(
                input_data = input_data)
        
        input_layer = []

        for sine_input_data in sine_input_data_list:
            input_layer.append(
                [float(sine_input_data.x)])

        input_layer = np.array(input_layer)

        # get the output
        init_model = \
            nn.Model(
                weights = weights,
                biases = biases,
                layer_sizes = layer_sizes)

        forward_propagated_model = \
            nn.forward_propagate(
                nn.insert_input_layer(
                    input_layer, init_model))

        output_layer = \
            nn.last_layer(
                forward_propagated_model)


        # shape the input/output layers correctly
        input_layer = input_layer.T[0]
        output_layer = output_layer.T[0]

        # join the input and output layers
        outputs = []
        for i in range(len(input_layer)):
            if compare == 'yes':
                outputs.append([ input_layer[i], output_layer[i],  math.sin(input_layer[i])])
            else: 
                outputs.append([ input_layer[i], output_layer[i] ])

        context = {
            'outputs': outputs,
            'compare': compare,
        }

        if output_type == 'plain_text':
            return render(request, "sine/output_plain_text.html", context)
        else:
            return render(request, "sine/output_graph.html", context)

    context = {
        'input_data_list': input_data_list,
        'training_sessions': training_sessions,
    }

    return render(request, "sine/run.html", context)

def index(request):
    context = {
        'training_data_count': TrainingData.objects.all().count()
    }
    return render(request, "sine/index.html", context)

def generate_training_data(request, training_data_id):
    training_data = get_object_or_404(TrainingData, pk = training_data_id)

    if (request.method == "POST"):
        range_from = float(request.POST['range_from'])
        range_to = float(request.POST['range_to'])

        number_of_values = int(request.POST['number_of_values'])

        values = np.linspace(range_from * math.pi, range_to * math.pi, number_of_values)

        sine_training_data_objects = []

        for i in range(number_of_values):
            sine_training_data_objects.append(
                SineTrainingData(
                    x = values[i],
                    y = math.sin(values[i]),
                    training_data = training_data))

        SineTrainingData.objects.bulk_create(sine_training_data_objects)

        training_data.number_of_entries = number_of_values
        training_data.save()

        messages.success(request, "Training Data generated successfully!")
        return redirect("training_data:list", flavor_machine_name = "sine")


    context = {
        'training_data': training_data
    }

    return render(request, "sine/generate_training_data.html", context)

def generate_input_data(request, input_data_id):
    input_data = get_object_or_404(InputData, pk = input_data_id)

    if (request.method == "POST"):
        range_from = float(request.POST['range_from'])
        range_to = float(request.POST['range_to'])

        number_of_values = int(request.POST['number_of_values'])

        values = np.linspace(range_from * math.pi, range_to * math.pi, number_of_values)

        # delete the old input data before
        SineInputData.objects.filter(input_data = input_data).delete()

        # insert the new input data
        for i in range(number_of_values):
            SineInputData.objects.create(
                x = values[i],
                input_data = input_data)


        input_data.number_of_entries = number_of_values
        input_data.save()

        messages.success(request, "Input Data Generated Successfully!")
        return redirect("input_data:list", flavor_machine_name = "sine")
        

    return render(request, "sine/generate_input_data.html")

def reset(request, training_data_id):
    training_data = get_object_or_404(TrainingData, pk = training_data_id)

    if (request.method == "POST"):
        SineTrainingData.objects.filter(training_data = training_data).delete()
        
        training_data.number_of_entries = 0
        training_data.save()

        return redirect('training_data:list', flavor_machine_name = 'sine')

    context = {
        'training_data': training_data
    }

    return render(request, "sine/reset.html", context)

def initialize_training_session(request, training_session_id):
    training_session = \
        get_object_or_404(
            TrainingSession, pk = training_session_id)

    # create a snapshot
    new_snapshot = Snapshot.objects.create(
        name = "Initial Snapshot",
        training_session = training_session)

    # populate weights and biases with random values
    layer_sizes = training_session.layer_sizes()

    weights = nn.random_weights(layer_sizes)
    biases = nn.random_biases(layer_sizes)

    weight_objects = []
    bias_objects = []

    # create weight and bias objects
    number_of_layers = len(layer_sizes)
    for i in range(number_of_layers - 1):
        current_layer_weights = weights[i].flatten()
        current_layer_biases = biases[i].flatten()

        for weight in current_layer_weights:
            weight_objects.append(
                Weight(
                    value = weight,
                    snapshot = new_snapshot,
                    layer = i))

        for bias in current_layer_biases:
            bias_objects.append(
                Bias(
                    value = bias,
                    snapshot = new_snapshot,
                    layer = i))

    # bulk create weights and biases
    Weight.objects.bulk_create(weight_objects)
    Bias.objects.bulk_create(bias_objects)

    messages.success(request, 'Training Session Initialized!')

    return redirect("training_sessions:list", flavor_machine_name = 'sine')

def input_data_detail(request, input_data_id):
    input_data = get_object_or_404(InputData, pk = input_data_id)
    sine_input_data_list = SineInputData.objects.filter(input_data = input_data)

    sine_input_data_flattened = ""
    for sine_input_data in sine_input_data_list:
        sine_input_data_flattened += str(sine_input_data) + ", "

    # slice it
    sine_input_data_flattened = sine_input_data_flattened[:-2]

    if request.method == 'POST':
        SineInputData.objects.filter(input_data = input_data).delete()

        values = request.POST['values']
        separated_values = values.split(',')

        sine_input_data_objects = []
        for separated_value in separated_values:
            sine_input_data_objects.append(
                SineInputData(
                    x = separated_value,
                    input_data = input_data))

        SineInputData.objects.bulk_create(sine_input_data_objects)

        input_data.number_of_entries = len(separated_values)
        input_data.save()

        messages.success(request, "Input Data Saved Successfully!")
        return redirect("sine:input_data_detail", input_data_id = input_data_id)


    context = {
        'input_data': input_data,
        'sine_input_data_flattened': sine_input_data_flattened,
    }

    return render(request, "sine/input_data_detail.html", context)


def train(request, training_session_id):
    training_session = \
        get_object_or_404(TrainingSession, pk = training_session_id)
    flavor = training_session.flavor
    training_data_list = TrainingData.objects.filter(flavor = flavor)
    snapshots = Snapshot.objects.filter(training_session = training_session)

    if request.method == 'POST':
        iterations = int(request.POST['iterations'])
        alpha = request.POST['alpha']

        # alpha = 0.01 by default
        if len(alpha) == 0:
            alpha = 0.01
        else:
            alpha = float(alpha)

        algorithm = request.POST['algorithm']
        training_data = request.POST['training_data']
        snapshot = request.POST['snapshot']

        # load the objects for weights and biases
        weight_objects = Weight.objects.filter(snapshot = snapshot)
        bias_objects = Bias.objects.filter(snapshot = snapshot)

        # prepare the weights and biases
        from libs import helpers
        layer_sizes = training_session.layer_sizes()
        weights, biases = \
            helpers.generate_weights_and_biases_from_objects(
                weight_objects, bias_objects, layer_sizes)

        # load the sine training data
        sine_training_data_list = \
            SineTrainingData.objects.filter(
                training_data = training_data)
        
        input_layer, examples = [], []

        for sine_training_data in sine_training_data_list:
            input_layer.append(
                [float(sine_training_data.x)])
            examples.append(
                [float(sine_training_data.y)])

        # make sure input layer and examples are np arrays
        input_layer = np.array(input_layer)
        examples = np.array(examples)

        # prepare the model
        from libs import neuralnet as nn
        model = \
            nn.insert_input_layer(
                input_layer,
                nn.Model(
                    layer_sizes = layer_sizes,
                    weights = weights,
                    biases = biases,
                    examples = examples))

        # prepare the settings
        settings = {
            'times': iterations,
            'alpha': alpha,
            'stochastic': True
        }

        if algorithm == 'sgd':
            settings['stochastic'] = True
        else:
            settings['stochastic'] = False

        model = nn.forward_propagate(model)

        # train the bad boy in the background!
        from training_sessions import background_trainer as bt
        bt.train(settings, model, training_session)

    return redirect("training_sessions:list", flavor_machine_name = flavor.machine_name)