from tkinter import *

import random

WIDTH = 1000
HEIGHT = 600
CELL_SIZE = 20
FRUITS_AMOUNT = 5
TIMINGS = 50
FIELD_WIDTH = WIDTH // CELL_SIZE
FIELD_HEIGHT = HEIGHT // CELL_SIZE

class Game(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Snake game, everyone")
        self.c = Canvas(width = WIDTH, height = HEIGHT)
        self.c.pack()
        
        self.MainSnake = self.RandomSnake()
        
        self.fruits = []
        
        self.root.bind("<Key>", self.MainSnake.changeDirect)


        self.lost = False
        self.loop = None
        self.main()  


    def main(self):
        self.MainSnake.Move()
        self.Check4Lose()
        self.CreateANewFruit()
        self.SnakeEatFruit()
        if not self.lost:
            self.loop = self.root.after(TIMINGS, self.main)

    def RandomSnake(self):
        xCreate = random.randint(1, FIELD_WIDTH - 1)
        yCreate = random.randint(1, FIELD_HEIGHT - 1)
        sizeCreate = random.randint(3, 5)
        dxCreate = random.randint(0,1)
        dyCreate = 1 - dxCreate
        _Snake = Snake(self, xCreate, yCreate, sizeCreate, dxCreate, dyCreate)
        return _Snake

    def CreateANewFruit(self):
        if (len(self.fruits) < FRUITS_AMOUNT):
            self.fruits.append(Fruit(self))

    def SnakeEatFruit(self):
        for i in range(len(self.fruits)):
            if self.MainSnake.GetHeadsX() == self.fruits[i].x and self.MainSnake.GetHeadsY() == self.fruits[i].y:
                self.MainSnake.SnakeAteSomething()
                self.c.delete(self.fruits[i].instance)
                self.fruits.pop(i)
                break

    def Check4Lose(self):
        state = self.MainSnake.SnakeAteItself()
        #print(state)
        if state == True:
            print("lose")
            if self.loop is not None:
                self.root.after_cancel(self.loop)
                self.loop = None
                self.lost = True


class SnakePiece(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SnakeHead(SnakePiece):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


class Snake(object):
    def __init__(self, game, x, y, size, dx, dy):
        self.game = game
        self.size = size
        self.CantChange = False
        self.body = [SnakeHead(x, y, dx, dy)]
        #print("head = {} , {}".format(x,y))
        for pt in range(1, self.size):
            #print("piece {} = {} , {}".format(pt, x + pt*dx, y + pt*dy))
            self.body.append(SnakePiece(x - pt*dx, y - pt*dy))
        
        self.rects = [self.game.c.create_rectangle(self.body[0].x * CELL_SIZE, 
                                                            self.body[0].y * CELL_SIZE,
                                                            (self.body[0].x + 1) * CELL_SIZE, 
                                                            (self.body[0].y + 1) * CELL_SIZE, 
                                                            fill = "blue")]
        for i in range(1, self.size):
            self.rects.append (self.game.c.create_rectangle(self.body[i].x * CELL_SIZE, 
                                                            self.body[i].y * CELL_SIZE,
                                                            (self.body[i].x + 1) * CELL_SIZE, 
                                                            (self.body[i].y + 1) * CELL_SIZE, 
                                                            fill="#"+("%06x"%random.randint(0,16777215))))
    def Move(self):
        self.CantChange = False
        for i in reversed(range(1, self.size)):
            self.game.c.move(self.rects[i], 
                            (self.body[i - 1].x - self.body[i].x)*CELL_SIZE,
                            (self.body[i - 1].y - self.body[i].y)*CELL_SIZE)

            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        
        if self.body[0].x + self.body[0].dx < FIELD_WIDTH and self.body[0].x + self.body[0].dx > 0 and  self.body[0].y + self.body[0].dy < FIELD_HEIGHT and self.body[0].y + self.body[0].dy > 0:
            self.body[0].y = (self.body[0].y + self.body[0].dy)
            self.body[0].x = (self.body[0].x + self.body[0].dx)
            self.game.c.move(self.rects[0], self.body[0].dx * CELL_SIZE, self.body[0].dy * CELL_SIZE)
        
        else:
            x = self.body[0].x
            y = self.body[0].y
            self.body[0].y = (self.body[0].y + self.body[0].dy) % FIELD_HEIGHT
            self.body[0].x = (self.body[0].x + self.body[0].dx) % FIELD_WIDTH
            self.game.c.move (self.rects[0], 
                             (self.body[0].x - x)*CELL_SIZE,
                             (self.body[0].y - y)*CELL_SIZE)

    def changeDirect(self, event):
        if self.CantChange == True:
            return None
        if (event.keycode == 37 or event.keycode == 65) and self.body[0].dx == 0:
            self.body[0].dx = -1
            self.body[0].dy = 0
        elif (event.keycode == 39 or event.keycode == 68) and self.body[0].dx == 0:
            self.body[0].dx = 1
            self.body[0].dy = 0
        elif (event.keycode == 38 or event.keycode == 87) and self.body[0].dy == 0:
            self.body[0].dx = 0
            self.body[0].dy = -1
        elif (event.keycode == 40 or event.keycode == 83) and self.body[0].dy == 0:
            self.body[0].dx = 0
            self.body[0].dy = 1
        self.CantChange = True

    def GetHeadsX(self):
        return self.body[0].x;
    def GetHeadsY(self):
        return self.body[0].y;

    def SnakeAteSomething(self):
        self.body.append(SnakePiece(self.body[-1].x, self.body[-1].y))
        self.rects.append(self.game.c.create_rectangle(self.body[-1].x * CELL_SIZE, 
                                                        self.body[-1].y * CELL_SIZE,
                                                        (self.body[-1].x + 1) * CELL_SIZE, 
                                                        (self.body[-1].y + 1) * CELL_SIZE, 
                                                        fill="#"+("%06x"%random.randint(0,16777215))))

        self.size = self.size + 1

    def SnakeAteItself(self):
        for i in range(1, self.size):
            if (self.body[0].x == self.body[i].x) and (self.body[0].y == self.body[i].y):
                return True
        return False

class Fruit(object):
    def __init__(self, game):
        self.game = game
        self.x = random.randint(1, FIELD_WIDTH - 1)
        self.y = random.randint(1, FIELD_HEIGHT - 1)
        self.draw()
    
    def draw(self):
        self.instance = self.game.c.create_oval(self.x * CELL_SIZE, 
                                           self.y * CELL_SIZE,
                                           (self.x + 1) * CELL_SIZE, 
                                           (self.y + 1) * CELL_SIZE, 
                                           fill = "#"+("%06x"%random.randint(0,16777215)))




game = Game()
game.root.mainloop()