import unittest
import blossom

class TestBlossom(unittest.TestCase):

    def test1(self):

        # INPUT:
        #       ,-2 
        #    ,-1---3
        #   0  |`-4 
        #    `-5    

        # EXPECTED:
        #       ,-2  |       2  |       2
        #      1   3 |    1---3 |    1   3
        #   0     4  | 0     4  | 0   `-4
        #    `-5     |  `-5     |  `-5    

        graph = blossom.Graph()
        graph.add_edge((0, 1))
        graph.add_edge((0, 5))
        graph.add_edge((1, 2))
        graph.add_edge((1, 3))
        graph.add_edge((1, 4))
        graph.add_edge((1, 5))
        matching = blossom.Matching()
        matching.add_vertices(graph.get_vertices())
        expected = set()
        expected.add((
            (0, 5),
            (1, 2),
        ))
        expected.add((
            (0, 5),
            (1, 3),
        ))
        expected.add((
            (0, 5),
            (1, 4),
        ))
        actual = tuple(sorted(blossom.get_maximum_matching(graph, matching).edges))
        self.assertTrue(actual in expected)

    def test2(self):

        # INPUT:
        #    ,-1--2--3 
        #   0  |  |    
        #    `-5--4    

        # EXPECTED:
        #    ,-1  2--3  
        #   0
        #      5--4

        graph = blossom.Graph()
        graph.add_edge((0, 1))
        graph.add_edge((0, 5))
        graph.add_edge((1, 2))
        graph.add_edge((1, 5))
        graph.add_edge((2, 3))
        graph.add_edge((2, 4))
        graph.add_edge((4, 5))
        matching = blossom.Matching()
        matching.add_vertices(graph.get_vertices())
        expected = set()
        expected.add((
            (0, 1),
            (2, 3),
            (4, 5),
        ))
        actual = tuple(sorted(blossom.get_maximum_matching(graph, matching).edges))
        self.assertTrue(actual in expected)

    def test3(self):

        # INPUT:
        #    ,-1--2 
        #   0  |  |
        #    `-4--3

        # EXPECTED:
        #      1  2 |    1--2 |    1  2 |  ,-1  2 |    1--2 |  ,-1  2
        #   0  |  | | 0       | 0     | | 0       | 0       | 0     |
        #      4  3 |    4--3 |  `-4  3 |    4--3 |  `-4  3 |    4  3

        graph = blossom.Graph()
        graph.add_edge((0, 1))
        graph.add_edge((0, 4))
        graph.add_edge((1, 2))
        graph.add_edge((1, 4))
        graph.add_edge((2, 3))
        graph.add_edge((3, 4))
        matching = blossom.Matching()
        matching.add_vertices(graph.get_vertices())
        expected = set()
        expected.add((
            (1, 4),
            (2, 3),
        ))
        expected.add((
            (1, 2),
            (3, 4),
        ))
        expected.add((
            (0, 4),
            (2, 3),
        ))
        expected.add((
            (0, 1),
            (3, 4),
        ))
        expected.add((
            (0, 4),
            (1, 2),
        ))
        expected.add((
            (0, 1),
            (2, 3),
        ))
        actual = tuple(sorted(blossom.get_maximum_matching(graph, matching).edges))
        self.assertTrue(actual in expected)

    def test4(self):

        # INPUT:
        #       ,---.
        #    ,-1--2--3
        #   0  |  |  |
        #    `-5--4-'

        # EXPECTED:
        #              |     ,---.  |           
        #    ,-1  2--3 |    1  2  3 |    1--2  3
        #   0          | 0     |    | 0        |
        #      5--4    |  `-5  4    |  `-5  4-' 

        graph = blossom.Graph()
        graph.add_edge((0, 1))
        graph.add_edge((0, 5))
        graph.add_edge((1, 2))
        graph.add_edge((1, 3))
        graph.add_edge((1, 5))
        graph.add_edge((2, 3))
        graph.add_edge((2, 4))
        graph.add_edge((3, 4))
        graph.add_edge((4, 5))
        matching = blossom.Matching()
        matching.add_vertices(graph.get_vertices())
        expected = set()
        expected.add((
            (0, 1),
            (2, 3),
            (4, 5),
        ))
        expected.add((
            (0, 5),
            (1, 3),
            (2, 4),
        ))
        expected.add((
            (0, 5),
            (1, 2),
            (3, 4),
        ))
        actual = tuple(sorted(blossom.get_maximum_matching(graph, matching).edges))
        self.assertTrue(actual in expected)

if __name__ == '__main__':
    unittest.main()

