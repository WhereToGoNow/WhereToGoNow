from lib.router import Graph, Router

# location / time / eval
spots = [
    ('new york, ny', 5, 8),
    ('montreal, quebec', 4, 9),
    ('toronto, ont', 5, 6),
    ('chicago, il', 4, 10),
    ('winnipeg, mb', 3, 7),
    ('los angeles, ca', 5, 7)
]


def generate_route():
    num_nodes = len(spots)
    v_start = 0
    v_end = num_nodes - 1
    length_max = num_nodes
    time_max = 80

    graph = Graph(num_nodes)
    router = Router(graph, verbose=False)

    for v in range(num_nodes):
        graph.time_nodes[v] = spots[v][1]
        graph.eval_nodes[v] = spots[v][2]

        for v_next in range(num_nodes):
            if v_next == v + 1:
                graph.time_edges[v][v_next] = 5
            else:
                graph.time_edges[v][v_next] = 7

    path = router.find_best_path(v_start, v_end, length_max, time_max)

    node_start = path.nodes[0]
    node_end = path.nodes[-1]
    node_middle = path.nodes[1:-1]

    return {
        'start': spots[node_start][0],
        'end': spots[node_end][0],
        'middle': [spots[v][0] for v in node_middle]
    }
