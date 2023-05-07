class Vertex:
    def __init__(self, index) -> None:
        self.index = index
        self.neighbours = []
        self.degrees = 0
        self.flag = 0
        self.final = False
        self.visited = False

    def get_neighbours(self, matrix):
        for i in range(len(matrix)):
            if matrix[self.index][i] == 1:
                self.neighbours.append(i)

    def __repr__(self):
        return str(self.index)

    def data_to_html(self):
        return f"""
            <div class="circle">{self.index}</div>

            <style>
            .circle {{
              width: 100px;
              height: 100px;
              border-radius: 50%;
              background-color: blue;
              display: flex;
              justify-content: center;
              align-items: center;
              font-size: 32px;
              color: white;
              margin: 20px;
            }}
            </style>
        """
