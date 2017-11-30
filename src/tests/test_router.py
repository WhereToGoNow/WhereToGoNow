from unittest import TestCase
from random import uniform
from time import time

import os
os.chdir('..')

from wheretogonow.core.router import Graph, Router


class TestRouter(TestCase):
    def test_time(self):
        num_nodes = 200
        list_max = 4
        length_max = 6
        time_max = 24

        graph = Graph(200)
        router = Router(graph)

        for v in xrange(num_nodes):
            graph.time_nodes[v] = uniform(2, 4)
            graph.eval_nodes[v] = uniform(4, 6)

            for v_next in xrange(v, num_nodes):
                t = uniform(3, 5)
                graph.time_edges[v][v_next] = t
                graph.time_edges[v_next][v] = t

        time_start = time()
        router.find_best_path(0, num_nodes - 1, list_max, length_max, time_max)
        time_end = time()

        self.assertTrue(time_end - time_start < 4)
