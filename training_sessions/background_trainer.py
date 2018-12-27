import threading
from libs import neuralnet as nn
from snapshots.models import Snapshot
from importlib import import_module
from logs.models import CostLog


class Thread(threading.Thread):
    def __init__(self, settings, model, training_session):
        threading.Thread.__init__(self)
        self.settings = settings
        self.model = model
        self.training_session = training_session
        self.current_iteration = 0


    def cb(self, model):
        # create the snapshot
        snapshot = Snapshot.objects.create(
            name = "Auto-generated",
            training_session = self.training_session)

        # insert the weights and biases associated with the snapshot
        flavor = self.training_session.flavor

        populate = import_module(flavor.machine_name + '.populate')
        populate.populate_weights_biases(snapshot, model)

        # update status
        self.current_iteration += 0.5
        percentage = "{:.1f}".format((self.current_iteration / self.settings['times']) * 100)

        self.training_session.status = str(percentage) + "%"
        self.training_session.save()

        # log down the cost
        CostLog.objects.create(
            snapshot = snapshot,
            cost = model.cost)


    def run(self):
        self.training_session.status = "0%"
        self.training_session.save()

        nn.train(
            times = self.settings['times'],
            stochastic = self.settings['stochastic'],
            decrease_alpha = False,
            alpha = self.settings['alpha'],
            debug = False,
            model = self.model,
            callback_interval = 5000,
            callback = self.cb)
        
        self.training_session.status = "done"
        self.training_session.save()

def train(settings, model, training_session):
	thread = Thread(settings, model, training_session)
	thread.start()