import turtle
import random

screen = turtle.Screen()
screen.bgcolor("lightblue")
screen.setup(width=600, height=600)

def draw_platform():
    platform = turtle.Turtle()
    platform.speed(0)
    platform.penup()
    platform.color("gray")
    platform.goto(-300, -250)
    platform.pendown()
    platform.begin_fill()
    for _ in range(2):
        platform.forward(600)
        platform.right(90)
        platform.forward(20)
        platform.right(90)
    platform.end_fill()
    platform.hideturtle()

draw_platform()

# Create scoreboard
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))

def update_score():
    global score
    score += 1
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))

game_over_display = turtle.Turtle()
game_over_display.speed(0)
game_over_display.color("red")
game_over_display.penup()
game_over_display.hideturtle()

def show_game_over():
    game_over_display.goto(0, 0)
    game_over_display.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    screen.update()

# Create shapes to stack
def create_shape():
    shape = turtle.Turtle()
    shape_type = random.choice(["square", "circle", "triangle"])
    shape.shape(shape_type)
    shape.shapesize(stretch_wid=2, stretch_len=2)  
    shape.color(random.choice(["red", "green", "blue", "yellow"]))
    shape.penup()
    shape.goto(0, 250) 
    shape.dx = 0
    shape.dy = -5  
    return shape


def move_left():
    if player.xcor() > -290:
        player.setx(player.xcor() - 40)  

def move_right():
    if player.xcor() < 290:
        player.setx(player.xcor() + 40)  

player = create_shape()

screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

placed_shapes = []

# check for matches
def check_for_match():
    if len(placed_shapes) < 3:
        return

    grid = {}
    for shape in placed_shapes:
        x = int(shape.xcor() // 40) * 40  
        y = int(shape.ycor() // 40) * 40
        if (x, y) not in grid:
            grid[(x, y)] = shape
    
    # Check for matches horizontally, vertically, and diagonally
    def get_connected_shapes(start_x, start_y, dx, dy):
        color = grid[(start_x, start_y)].color()
        shape_type = grid[(start_x, start_y)].shape()
        connected = [(start_x, start_y)]
        x, y = start_x + dx, start_y + dy
        while (x, y) in grid and grid[(x, y)].color() == color and grid[(x, y)].shape() == shape_type:
            connected.append((x, y))
            x += dx
            y += dy
        return connected

    to_remove = set()
    match_found = False 
    for (x, y) in grid:
        if (x, y) in to_remove:
            continue
        horizontal = get_connected_shapes(x, y, 40, 0)
        vertical = get_connected_shapes(x, y, 0, 40)
        diagonal1 = get_connected_shapes(x, y, 40, 40)
        diagonal2 = get_connected_shapes(x, y, 40, -40)
        
        if len(horizontal) >= 3:
            to_remove.update(horizontal)
            match_found = True
        if len(vertical) >= 3:
            to_remove.update(vertical)
            match_found = True
        if len(diagonal1) >= 3:
            to_remove.update(diagonal1)
            match_found = True
        if len(diagonal2) >= 3:
            to_remove.update(diagonal2)
            match_found = True
    
    # Hide and remove the matched shapes
    if match_found:
        update_score()  
    for (x, y) in to_remove:
        shape = grid[(x, y)]
        shape.hideturtle()
        placed_shapes.remove(shape)

def apply_gravity():
    y = player.ycor() + player.dy
    collision = False

    if y <= -230:
        y = -230
        collision = True

    for shape in placed_shapes:
        if abs(player.xcor() - shape.xcor()) < 40 and player.ycor() - shape.ycor() <= 40:  
            y = shape.ycor() + 40
            collision = True
            break

    if collision:
        player.sety(y)
        player.dy = 0
        placed_shapes.append(player)
        check_for_match()
        check_for_loss()  
        if player.dy == 0:  
            spawn_new_shape()
    else:
        player.sety(y)

# Spawning new shapes
def spawn_new_shape():
    global player
    player = create_shape()

# loss condition
def check_for_loss():
    for shape in placed_shapes:
        if shape.ycor() > 200: 
            show_game_over()
            screen.bye()

def game_loop():
    apply_gravity()
    if player.ycor() < -300:
        screen.bye()
    else:
        screen.update()
        screen.ontimer(game_loop, 30)  

screen.tracer(0)
game_loop()

screen.mainloop()
