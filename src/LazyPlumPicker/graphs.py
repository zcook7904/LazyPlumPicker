from collections import namedtuple

class Edge(namedtuple('Edge', 'tail head weight', defaults=[1])):
    """Edge between two vertices or nodes. Nodes are assumed to be string names"""

    def __eq__(self, other):
        if self.tail == other.tail and self.head == other.head:
            return True

        elif self.tail == other.head and self.head == other.tail:
            return True

        return False

    def __hash__(self):
        return hash([self.tail, self.head].sort())

    def add_direction(self, tail_first: bool = True):
        if tail_first:
            return DirectedEdge(self.tail, self.head, self.weight)

        else:
            return DirectedEdge(self.head, self.tail, self.weight)


class DirectedEdge(namedtuple('DirectedEdge', 'tail head weight', defaults=[1])):
    """DirectedEdge between two vertices or nodes. Nodes are assumed to be string names"""

    def __eq__(self, other):
        if self.tail == other.tail and self.head == other.head:
            return True

        return False

    def __hash__(self):
        return hash((self.tail, self.head, 1))

    def remove_direction(self) -> Edge:
        return Edge(self.tail, self.head, self.weight)

class Graph:
    """Class containing an undirected simple graph"""

    _directed = False


    def __init__(self, vertices: set = None, edges: set = None):
        if isinstance(vertices, set):
            self.vertices = vertices
        elif vertices:
            self.vertices = set(vertices)
        else:
            self.vertices = set()


        if edges:
            self.edges = set()
            self.add_edge(edges)
        else:
            self.edges = set()

    def add_vertex(self, *vertices: str) -> bool:
        """Add a vertex to the graph. Input is a string name of the new vertex. Returns true if the vertex is added and
        False if the vertex name already exists in the set."""
        order_before = self.order

        if isinstance(vertices[0], str):
            for vertex in vertices:
                self.vertices.add(vertex)

        elif isinstance(vertices[0], list) or isinstance(vertices[0], set) or isinstance(vertices[0], tuple):
            for vertex_list in vertices:
                for vertex in vertex_list:
                    if isinstance(vertex, str):
                        self.vertices.add(vertex)
                    else:
                        raise TypeError('Vertices should be strings')
        else:
            raise TypeError('Variable passed to add_vertex should be string(s) '
                            'or collection of list/tuple/set(s) of strings')

        if len(self.vertices) > order_before:
            # return true if number of vertices increase
            return True
        return False

    def add_edge(self, *edges):
        """Adds an Edge object to the graph. Can pass multiple edges or
        collection of list/tuple/set(s) of Edge objects. The function will also add new vertices if the Edge contains
        a vertex that does not currently exist in the graph.
        Returns true if an edge is added."""
        size_before = self.size
        def _add_edge(edges):
            for edge in edges:

                if isinstance(edge, DirectedEdge):
                    edge = edge.remove_direction()

                if not isinstance(edge, Edge):
                    raise ValueError('Variable passed to add_edge should be Graph.Edge objects '
                            'or collection of list/tuple/set(s) of Graph.Edge objects')

                for vertex in edge[:-1]:
                    if vertex not in self.vertices:
                        self.add_vertex(vertex)

                self.edges.add(edge)

        if isinstance(edges[0], list) or isinstance(edges[0], set) or (isinstance(edges[0], tuple)
                                                                       and not isinstance(edges[0], Edge)):

            for edge_list in edges:
                _add_edge(edge_list)
        else:
            _add_edge(edges)

        if len(self.edges) > size_before:
            return True

        return False

    def neighbors(self, vertex: str):
        """Returns a set of all of the nieghbors to the given vertex.
        Returns none if vertex is not in graph and an empty set if no neighbors exist."""
        if vertex in self.vertices:
            neighbor_set = set()
            for edge in self.edges:
                if vertex in edge:
                    # gives the opposite 'bit' index
                    # returns 0 if 1, 1 if 0
                    other_vertex_index = int(not bool(edge.index(vertex)))

                    neighbor_node = edge[other_vertex_index]
                    neighbor_set.add(neighbor_node)
            return neighbor_set

        print(f'Vertex {vertex} not in graph')
        return None

    def degree(self, vertex: str):
        return len(neighbors(vertex))

    @property
    def order(self):
        """The cardinality of (or number of nodes contained by) the vertex set"""
        return len(self.vertices)

    @property
    def size(self):
        """The cardinality of (or number of edges contained by) the edge set"""
        return len(self.edges)

    def are_adjacent(self, vertex1: str, vertex2: str):
        """Returns true if both vertices are contained in the graph and are adjacent (connected by an edge) to eachother."""
        if vertex1 not in self.vertices:
            raise ValueError('The first vertex is not contained in the graph')

        if vertex2 not in self.vertices:
            raise ValueError('The second vertex is not contained in the graph')

        for edge in self.edges:
            if vertex1 in edge[:-1] and vertex2 in edge[:-1]:
                return True

        # none found
        return False


class Digraph(Graph):
    """Class containing a simple directed graph."""
    _directed = True

    def add_edge(self, *edges):
        """Adds an Edge object to the graph. Can pass multiple edges or
        collection of list/tuple/set(s) of Edge objects. The function will also add new vertices if the Edge contains
        a vertex that does not currently exist in the graph.
        Returns true if an edge is added."""
        size_before = self.size
        if isinstance(edges[0], DirectedEdge):
            for edge in edges:
                for vertex in edge[:-1]:
                    if vertex not in self.vertices:
                        self.add_vertex(vertex)

                self.edges.add(edge)

        elif isinstance(edges[0], list) or isinstance(edges[0], set) or isinstance(edges[0], tuple):
            for edge_list in edges:
                for edge in edge_list:
                    if isinstance(edge, DirectedEdge):
                        self.edges.add(edge)
                    else:
                        raise TypeError('Edges should be a Graph.DirectedEdge object')
        else:
            raise TypeError('Variable passed to add_edge should be Graph.DirectedEdge objects '
                            'or collection of list/tuple/set(s) of Graph.DirectedEdge objects')

        if len(self.edges) > size_before:
            return True

        return False

    def _neighbors(self, vertex: str, check_if_head: bool):
        """Factory for in_ and out_neighbors."""

        if vertex in self.vertices:
            neighbor_set = set()
            for edge in self.edges:
                # checks if the vertex is a head of the edge
                if check_if_head:
                    if vertex == edge.head:
                        neighbor_node = edge.tail
                        neighbor_set.add(neighbor_node)
                else:
                    if vertex == edge.tail:
                        neighbor_node = edge.head
                        neighbor_set.add(neighbor_node)
            return neighbor_set

    def in_neighbors(self, vertex: str) -> int:
        """Returns all in-neigbors of the passed vertex"""
        return _neighbors(self, vertex, True)

    def out_neighbors(self, vertex: str) -> int:
        """Returns all out-neigbors of the passed vertex"""
        return _neighbors(self, vertex, False)

    def in_degree(self, vertex: str) -> int:
        if vertex in self.vertices:
            return len(in_neighbors(self, vertex))

    def out_degree(self, vertex: str) -> int:
        if vertex in self.vertices:
            return len(out_neighbors(self, vertex))

def is_walk(edges: list) -> bool:
    """Determines if a list of edges are a walk"""

    if not isinstance(edges[0], DirectedEdge):
        raise TypeError('All edges should be DirectedEdge object instances')

    previous_head = edges[0].head
    for edge in edges[1:]:
        if not isinstance(edge, DirectedEdge):
            raise TypeError('All edges should be DirectedEdge object instances')

        if previous_head == edge.tail:
            previous_head = edge.head

        else:
            return False

    return True

def is_trail(edges: list) -> bool:
    """Determines if a list of directed edges is a path (no repeated edges)"""
    if is_walk(edges):
        graph = Graph(edges=edges)
        if graph.size == len(edges):
            return True

    return False

def is_closed(edges: list) -> bool:
    first_edge = edges[0]
    last_edge = edges[-1]

    if not (isinstance(first_edge, DirectedEdge) or isinstance(last_edge, DirectedEdge)):
        raise TypeError('All edges should be DirectedEdge object instances')

    if first_edge.tail == last_edge.head:
        return True

    return False

def is_path(edges: list) -> bool:
    """Determine if a list of directed edges are a path"""
    if is_walk(edges):
        graph = Graph(edges=edges)
        if is_closed(edges):
            if graph.order == len(edges):
                return True
        else:
            if graph.order == len(edges) + 1:
                return True


    return False

def is_connected(graph: Graph):
    """Determines if a graph is connected."""
    for vertex in graph.vertices:
        if graph.degree(vertex) == 0:
            return False

if __name__ == '__main__':
    pass