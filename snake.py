import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, direX=1, direY=0, color=(255, 0, 0)):
        self.pos = start
        self.direX = 1
        self.direY = 0
        self.color = color

    def move(self, direx, direy):
        self.direX = direx
        self.direY = direy
        self.pos = (self.pos[0] + self.direX, self.pos[1] + self.direY)

    def draw(self, surface, head=False):
        global eating
        dis = self.w // self.rows
        i = self.pos[0]  # rows
        j = self.pos[1]  # columns

        pygame.draw.rect(surface, self.color, (i*dis, j*dis, dis, dis))

        if head:
            """draw eyes"""
            center = dis//2
            radius = 3
            eye1 = (i*dis + center - radius, j*dis+8)
            eye2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), eye1, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye2, radius)
            """draw mouth"""
            if eating:
                center = dis // 2
                radius = 6
                mouth = (i * dis + center + 2, j * dis + 18)
                pygame.draw.circle(surface, (0, 0, 0), mouth, radius)
            else:
                center = dis // 2
                posY = j * dis + 18
                posX = i * dis + center
                pygame.draw.line(surface, (0, 0, 0), (posX - 3, posY), (posX + 3, posY))


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direX = 0
        self.direY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direX = -1
                    self.direY = 0
                    self.turns[self.head.pos[:]] = [self.direX, self.direY]
                elif keys[pygame.K_RIGHT]:
                    self.direX = 1
                    self.direY = 0
                    self.turns[self.head.pos[:]] = [self.direX, self.direY]
                elif keys[pygame.K_UP]:
                    self.direX = 0
                    self.direY = -1
                    self.turns[self.head.pos[:]] = [self.direX, self.direY]
                elif keys[pygame.K_DOWN]:
                    self.direX = 0
                    self.direY = 1
                    self.turns[self.head.pos[:]] = [self.direX, self.direY]

        for index, cube in enumerate(self.body):
            posCube = cube.pos[:]
            if posCube in self.turns:
                turn = self.turns[posCube]
                cube.move(turn[0], turn[1])
                if index == len(self.body)-1:
                    self.turns.pop(posCube)
            else:
                if cube.direX == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows-1, cube.pos[1])
                elif cube.direX == 1 and cube.pos[0] >= cube.rows-1:
                    cube.pos = (0, cube.pos[1])
                elif cube.direY == 1 and cube.pos[1] >= cube.rows-1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.direY == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows-1)
                else:
                    cube.move(cube.direX, cube.direY)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direX = 0
        self.direY = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.direX, tail.direY

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].direX = dx
        self.body[-1].direY = dy

    def draw(self, surface):
        for index, cube in enumerate(self.body):
            """If its the head then draw eyes and mouth"""
            if index == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


def redraw_window(surface):
    global width, rows, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    pygame.display.update()


def random_snack(item):
    global rows
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, snake, snack, eating
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('Ugly Snake')
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(snake), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    ticks = 5
    while flag:
        print(ticks)
        pygame.time.delay(50)
        clock.tick(ticks)
        snake.move()
        if snake.body[0].pos == snack.pos:
            eating = True
            ticks += 0.5
            snake.add_cube()
            snack = Cube(random_snack(snake), color=(0, 255, 0))
        else:
            eating = False

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x+1:])):
                score = len(snake.body)
                message_box("Final Score", score)
                snake.reset((10, 10))
                break

        redraw_window(win)


main()
