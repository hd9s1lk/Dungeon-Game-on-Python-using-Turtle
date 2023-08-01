import turtle
import math
import random
import winsound
import time

window = turtle.Screen()
window.title("Dungeon Game by Henrique!")
turtle.screensize(canvwidth= 700, canvheight=700, bg="black")
window.tracer(0)

running = True

turtle.register_shape("chest.gif")
turtle.register_shape("head.gif")
turtle.register_shape("creeper.gif")



class Bloco(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

#Gold
pen = turtle.Turtle()
pen.speed(0)
pen.color("yellow")
pen.penup()
pen.setposition(240, 300)
goldstring = "Gold: 0"
pen.write(goldstring, False, align="left", font=("Arial", 14, "normal"))
pen.hideturtle()


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("head.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def cima(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def baixo(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def direita(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def esquerda(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
    
    def distance(self,other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self, x,y):
        turtle.Turtle.__init__(self)
        self.shape("chest.gif")
        self.color("yellow")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("creeper.gif")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else: 
            dx = 0
            dy = 0

        if self.close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            if player.xcor() > self.xcor():
                self.direction = "right"
            if player.ycor() > self.ycor():
                self.direction = "up"
            if player.ycor() < self.ycor():
                self.direction = "down"
        
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])
        turtle.ontimer(self.move, t=random.randint(100,300))

    def close(self,other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 100:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()


player = Player()
bloco = Bloco()

enemies = []
treasures = []
levels = [""]
walls = []

level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP     XXXXXXXXXXE     XX",
"X      XXXXXXXXXX      XX",
"X      XXXXXXXXXX      XX",
"X                      XX",
"X                      XX",
"X                      XX",
"X      XXXXXXXXXX      XX",
"X      XXXXXXXXXXXXXXXXXX",
"X      XXXXXXXXXXXXXXXXXX",
"X      XXXXXXXXXXXT     X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X                       X",
"X                       X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X      XXXXXXXXXXX      X",
"X     EXXXXXXXXXXXE     X",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]

levels.append(level_1)

#função que cria os mapas
def setup_dungeon(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = -288 + (y * 24)
            if character == "X":
                bloco.goto(screen_x,screen_y)
                bloco.stamp()
                walls.append((screen_x,screen_y))
            if character == "P":
                player.goto(screen_x,screen_y)
            if character == "T":
                treasures.append(Treasure(screen_x,screen_y))
            if character == "E":
                enemies.append(Enemy(screen_x,screen_y))
            
            
               

setup_dungeon(level_1)

#movimento jogador principal
window.listen()
window.onkey(player.cima, "w")
window.onkey(player.baixo, "s")
window.onkey(player.esquerda, "a")
window.onkey(player.direita, "d")

#movimento inimigo

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)



while running:

    for treasure in treasures:
        if player.distance(treasure):
            player.gold += treasure.gold
            print("Gold: {}" .format(player.gold))
            pen.clear()
            pen.write("Gold: {}" .format(player.gold), False, align="left", font=("Arial", 14, "normal"))
            winsound.PlaySound("Super-Mario-Bros.-Coin-Sound-Effect.wav", winsound.SND_ASYNC)
            treasure.destroy()
            treasures.remove(treasure)

    for enemy in enemies:
        if player.distance(enemy):
            winsound.PlaySound("Arcade-Retro-Game-Over.wav", winsound.SND_ASYNC)
            print("You Died!")
            time.sleep(2.5)
            exit()
            



    window.update()

window.mainloop()


