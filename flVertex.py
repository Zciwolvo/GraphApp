from random import randint


class Vertex:
    def __init__(self, index) -> None:
        self.index = index
        self.neighbours = []
        self.degrees = 0
        self.visited = False
        self.x = randint(50, 1000)
        self.y = randint(100, 700)

    def get_neighbours(self, matrix):
        for i in range(len(matrix)):
            if matrix[self.index][i]:
                self.neighbours.append(i)
        self.degrees = len(self.neighbours)

    def __repr__(self):
        return str(self.index)
