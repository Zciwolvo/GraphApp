from random import randint

class Vertex:
    def __init__(self, index) -> None:
        self.index = index
        self.neighbours = []
        self.degrees = 0
        self.flag = 0
        self.final = False
        self.visited = False
        self.x = randint(0, 1000)
        self.y = randint(100, 700)


    def get_neighbours(self, matrix):
        for i in range(len(matrix)):
            if matrix[self.index][i] == 1:
                self.neighbours.append(i)

    def __repr__(self):
        return str(self.index)
