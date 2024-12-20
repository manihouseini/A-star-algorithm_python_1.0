import pygame, setting
from sys import exit
import dfsANDbfs as grid
from utility import pygame_tools, tools

pygame.init()


class App:
    def __init__(self, WIDTH, HEIGHT, FPS) -> None:
        self.get_inputs()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CLOCK = pygame.time.Clock()
        self.FPS = FPS
        self.running = True

    def get_inputs(self):
        print(
            "left click on a cell to make it blocked off. right click to unblock. middle mouse, or 'f' to start the algorithim."
        )
        self.CELL_SIZE = int(tools.take_input("please enter the cell size (20): >", 20))

    def setup(self):
        self.grid = grid.Grid(0, 0, self.WIDTH, self.HEIGHT, self.CELL_SIZE)
        self.started = False

    def update(self):
        self.WIN.fill((255, 255, 255))
        self.grid.a_star_step(
            1, 1, len(self.grid.cells) - 2, len(self.grid.cells[0]) - 2, self.started
        )
        self.grid.show_grid(self.WIN)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.started = True
        if pygame.mouse.get_pressed()[1]:
            self.started = True
        if pygame.mouse.get_pressed()[2]:
            for i in self.grid.cells:
                for cell in i:
                    if cell.contains(pygame.mouse.get_pos()):
                        cell.color = (0, 0, 0)
                        cell.blocked = False
        if pygame.mouse.get_pressed()[0]:
            for i in self.grid.cells:
                for cell in i:
                    if cell.contains(pygame.mouse.get_pos()):
                        cell.color = (255, 255, 255)
                        cell.blocked = True

    def run(self):
        self.setup()
        while self.running:
            self.events()

            self.update()

            self.CLOCK.tick(self.FPS)
            pygame.display.set_caption(str(self.CLOCK.get_fps()))
            pygame.display.flip()


app = App(setting.window["width"], setting.window["height"], setting.window["fps"])
app.run()
