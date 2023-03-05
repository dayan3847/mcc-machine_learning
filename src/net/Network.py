from typing import List

import numpy as np
from networkx import DiGraph

from src.net.Neuron import Neuron
from src.net.NeuronInput import NeuronInput
from src.net.NeuronPerceptron import NeuronPerceptron

from src.net.Perceptron import Perceptron


class Network:
    _graph: DiGraph
    _neurons: List[List[Neuron]]
    _neurons_input: List[NeuronInput]  # _neurons[0]
    _neurons_output: List[NeuronPerceptron]  # _neurons[-1]

    def __init__(self, topology: List[int]):
        if len(topology) < 2:
            raise Exception("Network must have at least 2 layers")
        self._graph = DiGraph()
        self._neurons = []
        # Input Neuron:
        self._neurons_input = []
        input_layer_count: int = topology[0]
        for i in range(input_layer_count):
            node_input: NeuronInput = NeuronInput(self._graph)
            self._graph.add_node(node_input)
            self._neurons_input.append(node_input)
        self._neurons.append(self._neurons_input)
        # Hidden Neuron:
        for i_layer_count in topology[1:-1]:
            neurons_layer_i = []
            for i in range(i_layer_count):
                neuron: NeuronPerceptron = NeuronPerceptron(self._graph, self.generate_weight())
                self._graph.add_node(neuron)
                neurons_layer_i.append(neuron)
                self.connect_neuron_with_layer(neuron, i - 1)
            self._neurons.append(neurons_layer_i)
        # Output Neuron:
        self._neurons_output = []
        output_layer_count: int = topology[-1]
        for i in range(output_layer_count):
            neuron: NeuronPerceptron = NeuronPerceptron(self._graph, self.generate_weight())
            self._graph.add_node(neuron)
            self._neurons_output.append(neuron)
            self.connect_neuron_with_layer(neuron, -2)

    def propagate(self, features: List[float]) -> List[float]:
        # Clear neurons values:
        for layer in self._neurons:
            for neuron in layer:
                neuron.set_value()
        # Set network input values:
        for f in features:
            for neuron in self._neurons_input:
                neuron.set_value(f)

        return [o_neuron.get_value() for o_neuron in self._neurons_output]

    def generate_weight(self) -> float:
        return np.random.uniform(-.5, .5)

    def generate_weights(self, count: int) -> List[float]:
        return [self.generate_weight() for _ in range(count)]

    def connect_neuron_with_layer(self, neuron: Neuron, layer_index: int):
        for neuron_prev in self._neurons[layer_index]:
            self._graph.add_edge(neuron_prev, neuron, weight=self.generate_weight())
