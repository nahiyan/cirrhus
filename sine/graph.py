import io
import threading

from django.http import HttpResponse

from libs import neuralnet as nn
from matplotlib import pyplot as plt

class Thread(threading.Thread):
    def __init__(self, model):
        threading.Thread.__init__(self)
        self.model = model

    def run(self):
        x, y = [], []

        for i in range(nn.number_of_input_layers(self.model)):
            x.append(nn.layer(0, self.model)[i][0])
            y.append(nn.last_layer(self.model)[i][0])

        plt.plot(x, y)
        plt.savefig('sine/images/graph.png')
        plt.close()


def sine(model):
    thread = Thread(model)
    thread.start()

    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # plt.close()
    # plt_bytes = buf.getvalue()
    # buf.close()

    # return HttpResponse(plt_bytes, content_type="image/png")