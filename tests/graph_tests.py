import unittest
import base

import os
import sys

# adds python module to path
path_to_append = os.path.join('.', 'src')
sys.path.append(path_to_append)

from LazyPlumPicker import graphs

class EdgeTestCase(unittest.TestCase):
    def test_edge_equivalence(self):
        edge1 = graphs.Edge('a', 'b')
        edge2 = graphs.Edge('a', 'b')
        self.assertEqual(edge1, edge2)

        edge3 = graphs.Edge('b', 'a')
        self.assertEqual(edge1, edge3)

        edge4 = graphs.Edge('b', 'c')
        self.assertNotEqual(edge1, edge4)

    def test_directed_edge_equivalence(self):
        edge1 = graphs.DirectedEdge('a', 'b')
        edge2 = graphs.DirectedEdge('a', 'b')
        self.assertEqual(edge1, edge2)

        edge3 = graphs.DirectedEdge('b', 'a')
        self.assertNotEqual(edge1, edge3)

        edge4 = graphs.DirectedEdge('b', 'c')
        self.assertNotEqual(edge1, edge4)

class GraphTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_graph = graphs.Graph()

    def test_empty_graph(self):
        self.assertEqual(self.test_graph.vertices, set())
        self.assertEqual(self.test_graph.edges, set())

    def test_add_vertex(self):
        self.test_graph.add_vertex('a')
        self.assertEqual(self.test_graph.vertices, set(['a']))
        self.test_graph.add_vertex('b')
        self.assertEqual(self.test_graph.vertices, set(['a', 'b']))

    def test_add_existing_vertex(self):
        #should return False when attempting to add vertex that is already in graph
        self.test_graph.add_vertex('a')
        self.assertFalse(self.test_graph.add_vertex('a'))
        self.assertEqual(self.test_graph.vertices, set(['a']))

    def test_add_multiple_vertices(self):
        self.test_graph.add_vertex(['a', 'b'])
        self.assertEqual(self.test_graph.vertices, set(['a', 'b']))

        self.test_graph.add_vertex('c', 'd')
        self.assertEqual(self.test_graph.vertices, set(['a', 'b', 'c', 'd']))

    def test_add_non_string_vertex(self):
        with self.assertRaises(TypeError):
            self.test_graph.add_vertex(2)

        with self.assertRaises(TypeError):
            self.test_graph.add_vertex(['a', 2])

    def test_add_edge(self):
        new_edge_1 = graphs.Edge('a', 'b')
        self.test_graph.add_edge(new_edge_1)
        self.assertEqual(self.test_graph.edges, set([new_edge_1]))
        self.assertEqual(self.test_graph.vertices, set(['a', 'b']))

        new_edge_2 = graphs.Edge('a', 'c')
        self.test_graph.add_edge(new_edge_2)
        self.assertEqual(self.test_graph.edges, set([new_edge_1, new_edge_2]))
        self.assertEqual(self.test_graph.vertices, set(['a', 'b', 'c']))

    def test_add_existing_edge(self):
        edge = graphs.Edge('a', 'b')
        self.test_graph.add_edge(edge)
        self.assertFalse(self.test_graph.add_edge(edge))
        self.assertEqual(self.test_graph.edges, set([edge]))
        self.assertEqual(self.test_graph.vertices, set(['a', 'b']))

    def test_add_non_edge(self):
        with self.assertRaises(ValueError):
            self.test_graph.add_edge(2)

        with self.assertRaises(ValueError):
            self.test_graph.add_edge(['a', 2])

    def test_graph_order(self):
        self.test_graph.add_vertex('a')
        self.test_graph.add_vertex('b')
        self.assertEqual(self.test_graph.order, 2)

    def test_graph_size(self):
        edge = graphs.Edge('a', 'b')
        self.test_graph.add_edge(edge)
        edge = graphs.Edge('b', 'c')
        self.test_graph.add_edge(edge)
        self.assertEqual(self.test_graph.size, 2)

    def test_are_adjacent(self):
        self.test_graph.add_edge(graphs.Edge('a', 'b'))
        self.test_graph.add_vertex('c')
        self.assertTrue(self.test_graph.are_adjacent('a', 'b'))
        self.assertFalse(self.test_graph.are_adjacent('a', 'c'))

    def test_are_adjacent_raise_ValueError(self):
        self.test_graph.add_vertex('a')
        with self.assertRaises(ValueError):
            self.test_graph.are_adjacent('a', 'c')

    def test_remove_vertex(self):
        self.test_graph.add_vertex('a', 'b')
        self.test_graph.remove_vertex('a')

        self.assertEqual(self.test_graph.vertices, set(['b']))
        with self.assertRaises(KeyError):
            self.test_graph.remove_vertex('c')

# class DigraphTestCase(unittest.TestCase):
#     # runs all graph test cases + those included below
#     def setUp(self) -> None:
#         self.test_graph = graphs.Digraph()

class WalkTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.edges = [graphs.DirectedEdge('a', 'b'), graphs.DirectedEdge('b', 'c'), graphs.DirectedEdge('c', 'd')]

    def test_is_walk(self):
        self.assertTrue(graphs.is_walk(self.edges))
        self.edges.append(graphs.DirectedEdge('d', 'b'))
        self.assertTrue(graphs.is_walk(self.edges))

        self.edges.append(graphs.DirectedEdge('f', 'a'))
        self.assertFalse(graphs.is_walk(self.edges))

    def test_is_trail(self):
        self.assertTrue(graphs.is_trail(self.edges))

        self.edges.append(graphs.DirectedEdge('d', 'b'))
        self.assertTrue(graphs.is_trail(self.edges))

        self.edges.append(graphs.DirectedEdge('b', 'c'))
        self.assertFalse(graphs.is_trail(self.edges))

        self.edges.append(graphs.DirectedEdge('c', 'b'))
        self.assertFalse(graphs.is_trail(self.edges))

    def test_is_path(self):
        self.assertTrue(graphs.is_path(self.edges))

        self.edges.append(graphs.DirectedEdge('d', 'b'))
        self.assertFalse(graphs.is_path(self.edges))

        self.edges.append(graphs.DirectedEdge('b', 'c'))
        self.assertFalse(graphs.is_path(self.edges))

        self.edges.append(graphs.DirectedEdge('c', 'b'))
        self.assertFalse(graphs.is_path(self.edges))

    def test_closed_path(self):
        self.edges.append(graphs.DirectedEdge('d', 'a'))
        self.assertTrue(graphs.is_path(self.edges))

if __name__ == '__main__':
    unittest.main()
