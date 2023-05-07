from random import randint
from collections import deque

from vertex import Vertex

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
                r = randint(0, 100)
                if r <= p:
                    row.append(1)
                else:
                    row.append(0)
            else:
                row.append(A[j][i])
        A.append(row)
    return A

def bfs(A, start) -> list[list[int]]:
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

def all_paths(graph: dict[int, Vertex], layers) -> list[list[int]]:
    """Returns all possible paths between vertices in adjacent layers in graph"""
    if len(layers) < 2:
        return []
    paths = []
    for vertex1 in layers[0]:
        visited = set()
        stack = [(vertex1, [vertex1])]
        while stack:
            curr_vertex, curr_path = stack.pop()
            visited.add(curr_vertex)
            if curr_vertex in layers[-1]:
                paths.append(curr_path)
            else:
                for neighbour in graph[curr_vertex].neighbours:
                    if neighbour not in visited and neighbour in layers[len(curr_path)]:
                        stack.append((neighbour, curr_path + [neighbour]))
    return paths


def create_vertices(matrix: list[int]) -> list[Vertex]:
    """Creates list of vertices and based on given argument [matrix] assigns it's neighbours indexes"""
    Vertices: list[Vertex] = []
    for v in range(n):
        Vertices.append(Vertex(v))
        Vertices[v].get_neighbours(matrix)
    return Vertices


def save_as_txt(matrix: list[int], deg: dict) -> None:
    """Generates txt filled based on given matrix"""
    with open("./output.txt", "w") as f:
        f.write("")  # Clears file
    with open("./output.txt", "a") as f:
        for a in matrix:
            f.writelines(str(a))
            f.write("\n")
        f.write(str(deg))
        f.write("\n")
        f.write(str(sorted(deg.items(), reverse=True, key=lambda x: x[1])))


if __name__ == "__main__":
    # n = int(input("Matrix size: "))
    # p = float(input("Chance: "))
    # s = int(input("Choose initial point: "))
    n = 6
    p = 0.4
    s = 0
    A = generate_matrix(n, p)
    A = [
        [0, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 0],
    ]
    Vertices = create_vertices(A)
    graph = {v.index: v for v in Vertices}

    layers = bfs(A, s)
    print(layers)


    paths = all_paths(graph, layers)
    print(paths)
    



    #deg = {}
    #for v in Vertices:
    #    deg[("index: " + str(v.index))] = v.degrees
    # print("Vertices:", deg)
    # print("Vertices sorted:", sorted(deg.items(), reverse=True, key=lambda x: x[1]))
    #save_as_txt(A, deg)
    # for i in A:
    #    print(i)
    #for i in range(n):
    #    print("Vertex:", i)
    #    print(Vertices[i].neighbours)
    #    print(Vertices[i].degrees)
    #    print("=====================")
