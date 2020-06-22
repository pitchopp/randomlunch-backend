import copy
import random


class UndirectedGraph:
    def __init__(self, nodes, connections=None):
        self.nodes = nodes
        if connections:
            self.connections = connections
        else:
            self.connections = []

    def __len__(self):
        return len(self.nodes)

    def add_connection(self, connection: set):
        if connection not in self.connections:
            self.connections.append(connection)

    def remove_connection(self, connection: set):
        self.connections.remove(connection)

    def is_isolated(self, node):
        for connection in self.connections:
            if node in connection:
                return False
        return True

    def is_connected(self):
        for node in self.nodes:
            if self.is_isolated(node):
                return False
        return True

    def get_isolated_nodes(self):
        for node in self.nodes:
            if self.is_isolated(node):
                yield node

    def get_neighbors(self, node):
        for connection in self.connections:
            elements = list(connection)
            if elements[0] == node:
                yield elements[1]
            elif elements[1] == node:
                yield elements[0]

    def get_random_neighbor(self, node):
        return random.choice(list(self.get_neighbors(node)))

    def get_number_of_neighbors(self, node):
        return len([x for x in self.connections if node in x])

    def remove_node(self, node):
        self.nodes.remove(node)
        self.connections = [x for x in self.connections if node not in x]

    def get_random_weakest_node(self):
        if len(self) == 0:
            return None
        weakests = []
        nb_connections = 999999999
        for node in self.nodes:
            nb = self.get_number_of_neighbors(node)
            if nb < nb_connections:
                weakests = [node]
                nb_connections = nb
            elif nb == nb_connections:
                weakests.append(node)
        random_weak = weakests[random.randrange(0, len(weakests))]
        return random_weak


def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)


def old_get_random_couples(list_persons):
    while len(list_persons) > 1:
        person_1 = pop_random(list_persons)
        person_2 = pop_random(list_persons)
        yield person_1, person_2


def get_random_couples(list_persons):
    # return old_get_random_couples(list_persons)
    connections = []
    nodes = []
    for person in list_persons:
        nodes.append(person)
        for meetable in person.get_meetable_persons(list_persons):
            if {person, meetable} not in connections:
                connections.append({person, meetable})
    graph = UndirectedGraph(nodes=nodes, connections=connections)
    print(graph.is_connected(), list(graph.get_isolated_nodes()))
    while len(graph) > 0 and graph.is_connected():
        weakest = graph.get_random_weakest_node()
        neighbors = list(graph.get_neighbors(weakest))
        graph.remove_node(weakest)
        teammate = None
        while len(neighbors) > 0:
            random_neighbor = random.choice(neighbors)
            tmp_graph = copy.deepcopy(graph)
            tmp_graph.remove_node(random_neighbor)
            if tmp_graph.is_connected():
                teammate = random_neighbor
                break
            else:
                neighbors.remove(random_neighbor)
        graph.remove_node(teammate)
        yield teammate, weakest
