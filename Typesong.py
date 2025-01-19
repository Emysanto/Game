from random import randrange, choice
from turtle import *
from freegames import vector

# Define the songs (use lowercase and remove punctuation for simplicity)
songs = [
    "we will we will rock you",
    "let it be let it be let it be",
    "twinkle twinkle little star",
    "imagine all the people",
    "here comes the sun"
]

# Select a random song at the start
current_song = choice(songs)
lyrics_index = 0

targets = []
letters = []
score = 0
speed = 100  # Initial falling speed (in milliseconds)


def inside(point):
    """Return True if point on screen."""
    return -200 < point.x < 200 and -200 < point.y < 200


def draw():
    """Draw letters."""
    clear()

    for target, letter in zip(targets, letters):
        goto(target.x, target.y)
        write(letter, align='center', font=('Consolas', 20, 'normal'))

    update()


def move():
    """Move letters."""
    global lyrics_index, speed, score

    if randrange(20) == 0:
        x = randrange(-150, 150)
        target = vector(x, 200)
        targets.append(target)

        # Get the next letter from the current song
        while current_song[lyrics_index] == " ":
            lyrics_index = (lyrics_index + 1) % len(current_song)
        letter = current_song[lyrics_index]
        letters.append(letter)
        lyrics_index = (lyrics_index + 1) % len(current_song)

    for target in targets:
        target.y -= 1

    draw()

    for target in targets:
        if not inside(target):
            pos = targets.index(target)
            del targets[pos]
            del letters[pos]  # Remove letter if it falls out

    # Check if the song is completed
    if lyrics_index == 0 and not letters:
        print("Song completed!")
        score += 10  # Bonus points for completing the song
        print("Score:", score)
        reset_game()

    # Schedule the next move with adjusted speed
    ontimer(move, speed)


def press(key):
    """Press key."""
    global score

    if key in letters:
        score += 1
        pos = letters.index(key)
        del targets[pos]
        del letters[pos]
    else:
        score -= 1

    print('Score:', score)


def reset_game():
    """Reset the game with a new song and increase difficulty."""
    global current_song, lyrics_index, speed
    current_song = choice(songs)  # Select a new random song
    lyrics_index = 0
    speed = max(50, speed - 10)  # Increase speed (minimum 50ms)
    print("New song:", current_song)


setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
listen()

for letter in set("".join(songs)):  # Bind keys for all letters in all songs
    if letter != " ":
        onkey(lambda letter=letter: press(letter), letter)

move()
done()
