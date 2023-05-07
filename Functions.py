from random import randint
from collections import deque

from flVertex import Vertex

# TODO: Graphical web interface using Flask


def generate_matrix(n: int, p: float) -> list[int]:
    """Generates [n]x[n] matrix with [p] chance of its elements being 1 and (1-[p]) chance of it being 0

    Returns:
        list[int]: Matrix describing graph
    """
    A = []
    p = p * 100
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            elif j > i:
                r = randint(1, 100)
                if r <= p:
                    row.append(1)
                else:
                    row.append(0)
            else:
                row.append(A[j][i])
        A.append(row)
    return A

def bfs(A: list[list[int]], start:int) -> list[list[int]]:
    """Breadth first search algorith generating layers of graph from matrix starting from integer start

    Args:
        A (list[list[int]]): matrix describing graph
        start (int): starting point

    Returns:
        list[list[int]]: list of lists describing each layer of graph
    """
    n = len(A)
    visited = [False] * n
    queue = deque([start])
    visited[start] = True
    layers = [[start]]
    while queue:
        layer = []
        for _ in range(len(queue)):
            vertex = queue.popleft()
            for neighbour in range(n):
                if A[vertex][neighbour] and not visited[neighbour]:
                    visited[neighbour] = True
                    queue.append(neighbour)
                    layer.append(neighbour)
        if layer:
            layers.append(layer)
    return layers


def create_graph(matrix: list[int]) -> dict[int : Vertex]:
    """Creates list of vertices and based on given argument [matrix] assigns it's neighbours indexes"""
    Graph: dict[int : Vertex] = {}
    for v in range(len(matrix)):
        vertex: Vertex = Vertex(v)
        vertex.get_neighbours(matrix)
        Graph[v] = vertex
    return Graph
