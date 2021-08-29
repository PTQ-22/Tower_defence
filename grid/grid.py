import pygame
from game.colors import ColorsRGB


class Grid:

    def __init__(self):
        self.width = 20
        self.height = 13
        self.rect_size = 68
        self.line_size = 2
        self.square_size = self.rect_size + self.line_size
        self.start_x = 5
        self.start_y = 5
        self.array_2d = [
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["s", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "e"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"]
        ]
        self.moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]
        self.dist = []
        self.predecessors = []
        self.start = (6, 0)
        self.end = (6, 19)

    def bfs(self):
        queue = [self.start]
        self.dist[self.start[0]][self.start[1]] = 0
        while len(queue) != 0:
            v = queue[0]
            queue.pop(0)
            for x, y in self.moves:
                u = (v[0] + x, v[1] + y)
                if u[0] < 0 or u[1] < 0 or u[0] >= self.height or u[1] >= self.width:
                    continue
                if self.array_2d[u[0]][u[1]] in ["#", "t"]:
                    continue
                if self.dist[u[0]][u[1]] == -1:
                    self.dist[u[0]][u[1]] = self.dist[v[0]][v[1]] + 1
                    self.predecessors[u[0]][u[1]] = v
                    queue.append(u)
                    if self.array_2d[u[0]][u[1]] == "e":
                        return True

        return False

    def get_path(self):
        self.dist = [
            [-1 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.predecessors = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        if not self.bfs():
            return False
        path = [self.end]
        c = self.end
        while self.predecessors[c[0]][c[1]] != 0:
            path.append(self.predecessors[c[0]][c[1]])
            c = self.predecessors[c[0]][c[1]]

        path.pop()
        self.clear_old_path()
        for y, x in reversed(path):
            if self.array_2d[y][x] == ".":
                self.array_2d[y][x] = "p"
        return list(reversed(path))

    def draw(self, win):
        for rect_y in range(self.start_y, self.start_y + self.square_size * self.height, self.square_size):
            for rect_x in range(self.start_x, self.square_size * self.width, self.square_size):
                x = rect_x // self.square_size
                y = rect_y // self.square_size
                if self.array_2d[y][x] == "#":  # barrier
                    color = ColorsRGB.BLACK
                elif self.array_2d[y][x] == "s":  # start
                    color = ColorsRGB.MAGENTA
                    # start = (y, x)
                elif self.array_2d[y][x] == "e":  # end
                    color = ColorsRGB.GREEN
                else:
                    color = ColorsRGB.LIGHT_GREY
                pygame.draw.rect(win, color, (rect_x, rect_y, self.rect_size, self.rect_size))

    def clear_old_path(self):
        for rect_y in range(self.start_y, self.start_y + self.square_size * self.height, self.square_size):
            for rect_x in range(self.start_x, self.square_size * self.width, self.square_size):
                x = rect_x // self.square_size
                y = rect_y // self.square_size
                if self.array_2d[y][x] == "p":  # barrier
                    self.array_2d[y][x] = "."
