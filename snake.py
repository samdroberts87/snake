from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 460
SPEED = 100
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOUR = "#00FF00"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"


class Snake:
    def __init__(self):
        self.body_parts = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")


def next_turn(snake, food):
    global SPEED
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        if score < high_score:
            label.config(text="Score: {}".format(score))
        else:
            label.config(text="New High score: {}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global high_score
    if score > high_score:
        high_score = score
    label.config(text=f"Score: {score}. \nPress 'R' to play again.")
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("consolas", 70), text="GAME OVER!",
                       fill="red", tag="gameover")


def reset_game(event):
    global score
    global direction
    global snake
    global food

    score = 0
    direction = "down"
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)


window = Tk()
window.title("SNAKE")
window.resizable(False, False)

score = 0
high_score = 0

direction = "down"

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("r", reset_game)  # Bind 'r' key to reset the game

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
