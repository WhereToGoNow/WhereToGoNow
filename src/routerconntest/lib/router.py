"""Implemenation of routing algorithm.

We assume that evaluation of each node and time of each node & each edge
is given. Currently, 'point' of the path is given as

point = sum of (eval of v) * weight_eval_nodes for nodes v in P
      + sum of (time of v) * weight_time_nodes for nodes v in P
      + sum of (time of e) * weight_time_edges for edges e in P
"""

weight_eval_nodes = 1.0
weight_time_nodes = -0.2
weight_time_edges = -0.03


# ============================================================

class Graph(object):
    def __init__(self, num_nodes):
        """Constructor."""
        # Nodes: V = {0, 1, ..., (num_nodes - 1)}
        # Edges: E = {i, j in V | (i -> j)}
        self.num_nodes = num_nodes
        self.time_nodes = [0] * self.num_nodes
        self.eval_nodes = [0] * self.num_nodes

        # If we initialize the 2D list like A = [[x] * w] * h,
        # every row points to the same object ([x] * w) and we're screwed.
        # (Changing an element of any row will affect other rows too.)
        self.time_edges = [[0] * self.num_nodes
                           for _ in range(self.num_nodes)]


# ============================================================

class Path(object):
    def __init__(self, graph, nodes, initialize=True):
        """Constructor."""
        self.graph = graph
        self.nodes = nodes
        self.length = len(nodes)
        self.time = 0
        self.point = 0

        if not initialize:
            return

        # calculate the time and the point
        # (1) for each node v
        for i in range(self.length):
            v = self.nodes[i]

            self.time += self.graph.time_nodes[v]
            self.point += self.graph.eval_nodes[v] * weight_eval_nodes \
                          + self.graph.time_nodes[v] * weight_time_nodes

        # (2) for each edge (v_1 -> v_2)
        for i in range(self.length - 1):
            v_1, v_2 = self.nodes[i], self.nodes[i + 1]

            self.time += self.graph.time_edges[v_1][v_2]
            self.point += self.graph.time_edges[v_1][v_2] * weight_time_edges

    def add_node(self, pos, v):
        """Add `v` at position `pos`."""
        self.nodes.insert(pos, v)
        self.length += 1

        v_prev = self.nodes[pos - 1]
        v_next = self.nodes[pos + 1]

        # (1) add the node v
        self.time += self.graph.time_nodes[v]
        self.point += self.graph.eval_nodes[v] * weight_eval_nodes \
                      + self.graph.time_nodes[v] * weight_time_nodes

        # (2) add the edges (v_prev -> v) and (v -> v_next)
        self.time += self.graph.time_edges[v_prev][v] \
                     + self.graph.time_edges[v][v_next]

        self.point += self.graph.time_edges[v_prev][v] * weight_time_edges \
                      + self.graph.time_edges[v][v_next] * weight_time_edges

        # (3) remove the edge (v_prev -> v_next)
        self.time -= self.graph.time_edges[v_prev][v_next]
        self.point -= self.graph.time_edges[v_prev][v_next] * weight_time_edges

    def copy(self):
        """Copy the path. (Reuse the time and the point.)"""
        path_copy = Path(self.graph, self.nodes[:], initialize=False)
        path_copy.time = self.time
        path_copy.point = self.point

        return path_copy

    def __repr__(self):
        return '[' + ' -> '.join('%d' % v for v in self.nodes) + ']'


# ============================================================

class Router(object):
    def __init__(self, graph, verbose=False):
        """Constructor."""
        self.graph = graph
        self.verbose = verbose

    def find_best_path(self, v_start, v_end, length_max, time_max):
        path = Path(self.graph, [v_start, v_end])

        if self.verbose:
            print('> %s\n  (Point: %.3f, Time: %.3f)'
                  % (path, path.point, path.time))

        for i in range(length_max - 2):
            path = self.find_next_path(path, time_max)

            if self.verbose:
                print('> %s\n  (Point: %.3f, Time: %.3f)'
                      % (path, path.point, path.time))

        return path

    def find_next_path(self, path, time_max):
        """Given a path, try to add a node in the middle of the path.
        Find the best one among them.
        """
        path_best = path
        not_used = [True] * self.graph.num_nodes

        # exclude the nodes included in the path
        for v in path.nodes:
            not_used[v] = False

        # find the best path
        for v in range(self.graph.num_nodes):
            if not_used[v]:
                for pos in range(1, path.length):
                    path_new = path.copy()
                    path_new.add_node(pos, v)

                    if path_new.time > time_max:
                        continue

                    if path_new.point > path_best.point:
                        path_best = path_new

        return path_best
