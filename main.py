import pygame
import random
from random import randint

WIDTH = 800
HEIGHT = 800
FPS = 10

CELLCOUNTX = 40
CELLCOUNTY = 40
CELLSIZEXPX = WIDTH // CELLCOUNTX
CELLSIZEXPY = HEIGHT // CELLCOUNTY

FOODCOLOR = (100, 0, 0)
LINECOLOR = (100, 100, 100)
SNAKECOLOR = (0, 100, 0)
BLACK = (0, 0, 0)

# --------------------------------------------------------------------------------------------------------------
class Food:
    x = randint(0, CELLCOUNTX - 1)
    y = randint(0, CELLCOUNTY - 1)

    def reGen(self):
        self.x = randint(0, CELLCOUNTX - 1)
        self.y = randint(0, CELLCOUNTY - 1)


# --------------------------------------------------------------------------------------------------------------
class Snake:
    segments = [[randint(0, CELLCOUNTX - 1), randint(0, CELLCOUNTY - 1)]]
    size = 1
    direction = 0  # 0 - ^ 1 - -> 2 - \/ 3 - <-

    def changeDirection(self, buffDirection):
        self.direction = buffDirection

    def step(self, newDirection=direction):
        if abs(self.direction - newDirection) != 2 and newDirection != -1:
            self.direction = newDirection
        for i in range(0, len(self.segments) - 1):
            self.segments[i][0] = self.segments[i + 1][0]
            self.segments[i][1] = self.segments[i + 1][1]
        if self.direction == 0:
            self.segments[len(snake.segments) - 1][1] -= 1
        if self.direction == 1:
            self.segments[len(snake.segments) - 1][0] += 1
        if self.direction == 2:
            self.segments[len(snake.segments) - 1][1] += 1
        if self.direction == 3:
            self.segments[len(snake.segments) - 1][0] -= 1

    def eat(self, newDirection=direction):
        if abs(self.direction - newDirection) != 2 and newDirection != -1:
            self.direction = newDirection
        self.size += 1
        self.segments.append(
            [
                self.segments[len(snake.segments) - 1][0],
                self.segments[len(snake.segments) - 1][1],
            ]
        )
        if self.direction == 0:
            self.segments[len(snake.segments) - 1][1] -= 1
        if self.direction == 1:
            self.segments[len(snake.segments) - 1][0] += 1
        if self.direction == 2:
            self.segments[len(snake.segments) - 1][1] += 1
        if self.direction == 3:
            self.segments[len(snake.segments) - 1][0] -= 1

    def reGen(self):
        self.size = 1
        self.direction = 0
        self.segments.clear()
        self.segments.append([randint(0, CELLCOUNTX - 1), randint(0, CELLCOUNTY - 1)])

    def testCollision(this):
        for i in range(0, len(snake.segments) - 1):
            if (
                snake.segments[i][0] == snake.segments[len(snake.segments) - 1][0]
                and snake.segments[i][1] == snake.segments[len(snake.segments) - 1][1]
            ):
                return True
        return False


# --------------------------------------------------------------------------------------------------------------
def drawFildGrid(screen):
    for x in range(CELLSIZEXPX, WIDTH, CELLSIZEXPX):
        pygame.draw.line(screen, LINECOLOR, (x, 0), (x, WIDTH))
    for y in range(CELLSIZEXPY, HEIGHT, CELLSIZEXPY):
        pygame.draw.line(screen, LINECOLOR, (0, y), (HEIGHT, y))


def drawSnake(screen, snake):
    for i in range(0, len(snake.segments) - 1):
        pygame.draw.rect(
            screen,
            SNAKECOLOR,
            (
                snake.segments[i][0] * CELLSIZEXPX + 1,
                snake.segments[i][1] * CELLSIZEXPY + 1,
                CELLSIZEXPX - 1,
                CELLSIZEXPY - 1,
            ),
        )
    pygame.draw.rect(
        screen,
        SNAKECOLOR,
        (
            snake.segments[len(snake.segments) - 1][0] * CELLSIZEXPX + 1,
            snake.segments[len(snake.segments) - 1][1] * CELLSIZEXPY + 1,
            CELLSIZEXPX - 1,
            CELLSIZEXPY - 1,
        ),
    )


def drawFood(screen, food):
    pygame.draw.rect(
        screen,
        FOODCOLOR,
        (
            food.x * CELLSIZEXPX + 1,
            food.y * CELLSIZEXPY + 1,
            CELLSIZEXPX - 1,
            CELLSIZEXPY - 1,
        ),
    )


def testEating(food, snake):
    if (
        food.x == snake.segments[len(snake.segments) - 1][0]
        and food.y == snake.segments[len(snake.segments) - 1][1]
    ):
        return True
    return False


def testOut(snake):
    for n in snake.segments:
        if n[0] > CELLCOUNTX - 1 or n[0] < 0 or n[1] > CELLCOUNTY - 1 or n[1] < 0:
            return True
    return False


# --------------------------------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
running = True
snake = Snake()
food = Food()
# --------------------------------------------------------------------------------------------------------------
while running:
    clock.tick(FPS)
    newDirection = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                newDirection = 3
            elif event.key == pygame.K_RIGHT:
                newDirection = 1
            elif event.key == pygame.K_UP:
                newDirection = 0
            elif event.key == pygame.K_DOWN:
                newDirection = 2
            elif event.key == pygame.K_u:
                FPS += 5
            elif event.key == pygame.K_j:
                FPS -= 5

    if testOut(snake) or snake.testCollision():
        snake.reGen()

    if testEating(food, snake):
        snake.eat(newDirection)
        food.reGen()
    else:
        snake.step(newDirection)

    screen.fill(BLACK)
    drawFildGrid(screen)
    drawSnake(screen, snake)
    drawFood(screen, food)
    pygame.display.flip()

pygame.quit()
