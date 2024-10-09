from heapq import heapify, heappop, heappush


graph = {
    # Aragón
    "Huesca": {
        "Zaragoza": 71,
        "Lleida": 122
    },
    "Teruel": {
        "Zaragoza": 171,
        "Castellón de la Plana": 159,
        "Valencia": 141
    },
    "Zaragoza": {
        "Huesca": 71,
        "Teruel": 171,
        "Lleida": 142,
        "Tarragona": 211
    },
    # Comunidad Valenciana
    "Alicante": {
        "Valencia": 160
    },
    "Castellón de la Plana": {
        "Teruel": 159,
        "Valencia": 64
    },
    "Valencia": {
        "Alicante": 160,
        "Castellón de la Plana": 64,
        "Teruel": 141
    },
    # Cataluña
    "Barcelona": {
        "Girona": 100,
        "Lleida": 160,
        "Tarragona": 98
    },
    "Girona": {
        "Barcelona": 100
    },
    "Lleida": {
        "Huesca": 122,
        "Zaragoza": 142,
        "Barcelona": 160,
        "Tarragona": 108
    },
    "Tarragona": {
        "Zaragoza": 211,
        "Barcelona": 98,
        "Lleida": 108,
        "Castellón de la Plana": 64
    }
}

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph
    
    def add_edge(self,node1,node2,weight):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight

    def shortest_distances(self,source:str):
        distances = {node:float("inf") for node in self.graph}
        distances[source] = 0
        # Initialize a priority queue
        pq = [(0, source)]
        heapify(pq)

        # Create a set to hold visited nodes
        visited = set()
    
        while pq:  # While the priority queue isn't empty
            current_distance, current_node = heappop(pq)

            if current_node in visited:
                continue 
            visited.add(current_node)

            for neighbor, weight in self.graph[current_node].items():
                # Calculate the distance from current_node to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))
            predecessors = {node: None for node in self.graph}

            for node, distance in distances.items():
              for neighbor, weight in self.graph[node].items():
                if distances[neighbor] == distance + weight:
                    predecessors[neighbor] = node
        return distances, predecessors
    
    def shortest_path(self, source: str, target: str):
        # Generate the predecessors dict
            _, predecessors = self.shortest_distances(source)

            path = []
            current_node = target

        # Backtrack from the target node using predecessors
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]

        # Reverse the path and return it
            path.reverse()

            return path
G = Graph(graph=graph)

G.graph

distances = G.shortest_distances("Lleida")
print(distances, "\n")

distances, predecessors = G.shortest_distances("Girona")

print(predecessors)
print(predecessors["Girona"])
to_F = distances["Alicante"]

print(f"The shortest distance from Girona to Alicante is {to_F}")

print(G.shortest_path("Girona", "Alicante"))