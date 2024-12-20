import pygame, math


class Cell:
    def __init__(self, row, col, x, y, size) -> None:
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.size = size
        self.visited = False
        self.nWall = True
        self.sWall = True
        self.wWall = True
        self.eWall = True
        self.color = (0, 0, 0)
        self.border_color = (255, 255, 255)

        # *A Star
        self.blocked = False
        self.parent_row = row
        self.parent_col = col
        self.f = 0
        self.g = 0
        self.h = 0

    def contains(self, point):
        return (
            point[0] >= self.x
            and point[0] <= self.x + self.size
            and point[1] >= self.y
            and point[1] <= self.y + self.size
        )

    def show_rect(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 0)

    def show_borders(self, win):
        if self.nWall:
            pygame.draw.line(
                win, self.border_color, (self.x, self.y), (self.x + self.size, self.y)
            )
        if self.sWall:
            pygame.draw.line(
                win,
                self.border_color,
                (self.x, self.y + self.size),
                (self.x + self.size, self.y + self.size),
            )
        if self.wWall:
            pygame.draw.line(
                win, self.border_color, (self.x, self.y), (self.x, self.y + self.size)
            )
        if self.eWall:
            pygame.draw.line(
                win,
                self.border_color,
                (self.x + self.size, self.y),
                (self.x + self.size, self.y + self.size),
            )


class Grid:
    def __init__(self, x, y, width, height, cellSize) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.cells = []
        self.make_grid()

        # * dfs and bfs and A star
        self.currentCell = 0
        self.target = 0
        self.stack = []
        self.closed = []
        self.open = []
        self.first_loop = True
        self.found = False

    def make_grid(self):
        num_width = self.width // self.cellSize
        num_height = self.height // self.cellSize

        for y in range(num_height):
            row = []
            for x in range(num_width):
                cellX = x * self.cellSize + self.x
                cellY = y * self.cellSize + self.y
                c = Cell(y, x, cellX, cellY, self.cellSize)
                row.append(c)
            self.cells.append(row)

    def show_grid(self, win):
        for i in self.cells:
            for c in i:
                c.show_rect(win)

        for i in self.cells:
            for c in i:
                c.show_borders(win)

    def is_valid(self, row, col):
        return (
            (row >= 0)
            and (row < len(self.cells))
            and (col >= 0)
            and (col < len(self.cells[0]))
        )

    def find_least_f(self):
        point = 0
        smallest = -1
        for p in self.open:
            if smallest == -1 or p.f < smallest:
                point = p
                smallest = p.f
        self.open.remove(point)
        return point

    def get_h(self, cell):
        x = cell.col
        y = cell.row
        x2 = self.target.col
        y2 = self.target.row
        h = math.sqrt(abs(x2 - x) ** 2 + abs(y2 - y) ** 2)
        return h

    def process_successors(self, p):
        r = p.row
        c = p.col
        successors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) and (j == 0):
                    continue
                if self.is_valid(r + i, c + j):
                    successors.append(self.cells[r + i][c + j])

        for s in successors:
            if self.target == s:
                print("target found")
                self.found = True
                self.trace_path(s)
            if (s in self.closed) or (s.blocked):
                continue
            a = abs(s.row - p.row)
            b = abs(s.col - p.col)
            if (a == 1) and (b == 1):
                g = p.g + math.sqrt(2)
            else:
                g = p.g + 1
            h = self.get_h(s)
            f = g + h
            if (s in self.open) and (f < s.f):
                s.parent_row = p.row
                s.parent_col = p.col
                s.f = f
            elif s not in self.open:
                s.f = f
                s.parent_row = p.row
                s.parent_col = p.col
                s.color = (255, 255, 0)
                self.open.append(s)
            else:
                continue

    def trace_path(self, target=None):
        finished = False
        if target != None:
            self.trace_current = target
        if not finished:
            self.trace_current.color = (0, 255, 0)
            if self.trace_current.f == 0:
                finished = True
            self.trace_current = self.cells[self.trace_current.parent_row][
                self.trace_current.parent_col
            ]

    def a_star_step(self, row, col, targetRow, targetCol, started):
        if self.first_loop:
            self.first_loop = False
            cell = self.cells[row][col]
            cell.color = (0, 255, 0)
            self.open.append(cell)
            self.target = self.cells[targetRow][targetCol]
            self.target.color = (0, 0, 255)
        if started:
            if len(self.open) > 0 and not self.found:
                p = self.find_least_f()
                p.color = (155, 0, 155)
                self.closed.append(p)

                self.process_successors(p)
            elif not self.found:
                print("sorry the target was not found")
            elif self.found:
                self.trace_path()

    def add_other_cells(self):
        y = self.currentCell.row
        x = self.currentCell.col
        width = len(self.cells[0])
        height = len(self.cells)
        if x + 1 < width:
            cell = self.cells[y][x + 1]
            if not cell.visited and (cell not in self.stack):
                self.stack.append(cell)
        if y + 1 < height:
            cell = self.cells[y + 1][x]
            if not cell.visited and (cell not in self.stack):
                self.stack.append(cell)
        if x - 1 >= 0:
            cell = self.cells[y][x - 1]
            if not cell.visited and (cell not in self.stack):
                self.stack.append(cell)
        if y - 1 >= 0:
            cell = self.cells[y - 1][x]
            if not cell.visited and (cell not in self.stack):
                self.stack.append(cell)

    def df_search_step(self, row, col, targetRow, targetCol):
        # * starting the algorithim
        if self.currentCell == 0:
            self.stack.append(self.cells[row][col])
            self.target = self.cells[targetRow][targetCol]
            self.target.color = (0, 0, 255)
        # * taking the cell from the stack
        if len(self.stack) > 0:
            self.currentCell = self.stack.pop()

            # * proccessing the current cell
            self.currentCell.color = (200, 0, 200)
            self.currentCell.visited = True

            # * if found the target
            if self.currentCell == self.target:
                print("found cell")
                self.found = True
                self.stack.clear()
                self.currentCell.color = (0, 255, 0)

            # * adding the other cells
            if not self.found:
                self.add_other_cells()

    def df_search_full(self, row, col, targetRow, targetCol):
        # * starting the algorithim
        if self.currentCell == 0:
            self.stack.append(self.cells[row][col])
            self.target = self.cells[targetRow][targetCol]
            self.target.color = (0, 0, 255)
        # * taking the cell from the stack
        while len(self.stack) > 0:
            self.currentCell = self.stack.pop()

            # * proccessing the current cell
            self.currentCell.color = (200, 0, 200)
            self.currentCell.visited = True

            # * if found the target
            if self.currentCell == self.target:
                print("found cell")
                self.found = True
                self.stack.clear()
                self.currentCell.color = (0, 255, 0)

            # * adding the other cells
            if not self.found:
                self.add_other_cells()

    def bf_search_step(self, row, col, targetRow, targetCol):
        # * starting the algorithim
        if self.currentCell == 0:
            self.stack.append(self.cells[row][col])
            self.target = self.cells[targetRow][targetCol]
            self.target.color = (0, 0, 255)
        # * taking the cell from the que
        if len(self.stack) > 0:
            self.currentCell = self.stack.pop(0)

            # * proccessing the current cell
            self.currentCell.color = (200, 0, 200)
            self.currentCell.visited = True

            # * if found the target
            if self.currentCell == self.target:
                print("found cell")
                self.found = True
                self.stack.clear()
                self.currentCell.color = (0, 255, 0)

            # * adding the other cells
            if not self.found:
                self.add_other_cells()

    def bf_search_full(self, row, col, targetRow, targetCol):
        # * starting the algorithim
        if self.currentCell == 0:
            self.stack.append(self.cells[row][col])
            self.target = self.cells[targetRow][targetCol]
            self.target.color = (0, 0, 255)
        # * taking the cell from the que
        while len(self.stack) > 0:
            self.currentCell = self.stack.pop(0)

            # * proccessing the current cell
            self.currentCell.color = (200, 0, 200)
            self.currentCell.visited = True

            # * if found the target
            if self.currentCell == self.target:
                print("found cell")
                self.found = True
                self.stack.clear()
                self.currentCell.color = (0, 255, 0)

            # * adding the other cells
            if not self.found:
                self.add_other_cells()
