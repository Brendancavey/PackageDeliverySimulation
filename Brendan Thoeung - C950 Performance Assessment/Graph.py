###First Name: Brendan||||Last Name: Thoeung||||Student ID: 007494550

#Assistance zybooks and c950 webinar3

class Graph:
    def __init__(self):
        self.adjacency_matrix = {} #vertex dictionary {key:value}
        self.edge_weight = {} #edge dictionary {key:value}

    def add_vertex(self, new_vertex):
        self.adjacency_matrix[new_vertex] = []  #add new vertex as a key, and an empty list as its value pair

    def add_directed_edge(self, from_vertex, to_vertex, weight):
        self.edge_weight[(from_vertex, to_vertex)] = weight #add tuple (from_vertex, to_vertex) as a key, and the weight as its value pair
        self.adjacency_matrix[from_vertex].append(to_vertex) #find from_vertex key in adjacency list, append to its value pair(which is a list) to_vertex

    def add_undirected_edge(self, vertex_a, vertex_b, weight): #calls add_directed_edge function to add edge and direction in both directions since it is undirected
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def print_list(self):
        print(self.adjacency_matrix)

    def print_edge_list(self):
        print(self.edge_weight)

class Vertex:
    def __init__(self, label):
        self.label = label
        self.shortest_path = 1000
        self.previous_vertex = None
        self.vertex_id = None
        self.shortest_path_dict = {} #keeps track of the shortest path from current_vertex to a given vertex
        self.branching_path_list = []

    def __repr__(self):
        return str(self.label)
















