import pygame
import random

# Colors
black = (0, 0, 0)
gray_white = (220, 220, 220)
red = (255, 0, 0)
blue = (8, 211, 247)

# Set Screen
HEIGHT, WIDTH, SIZE = 20, 20, 35
pygame.init()
screen = pygame.display.set_mode((HEIGHT * SIZE, WIDTH * SIZE))
font = pygame.font.Font('freesansbold.ttf', 20)
FPS = 30
clock = pygame.time.Clock()
background = pygame.Surface((HEIGHT * SIZE, WIDTH * SIZE))
background.fill((255, 255, 255))

# Set Variables
score = 0
body = [(0, 0)]
length = 1

def main():

    global length, score
    food = food_pos(body)

    while True:

        clock.tick(FPS)
        screen.fill(gray_white)

        # Get move
        move = backtrack(the_pos=body[0], the_food=food, the_body=body)

        try:
            body.insert(0, (move[0], move[1]))

        # No move possible
        except TypeError:
            print("GameOver")
            break

        # Ate food
        if body[0] == food:
            food = food_pos(body)
            length += 1
            score += 1
            print(f"Score: {score}")

        # delete tail
        while len(body) > length:
            del body[-1]

        # Draw score
        the_score = font.render(f"Score: {score}", True, black)
        score_rect = the_score.get_rect()
        score_rect.center = (80, 30)
        screen.blit(background, (0, 0))
        screen.blit(the_score, score_rect)


        # draw food
        pygame.draw.rect(screen, red, (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE))

        # draw snake
        for k, pos in enumerate(body):
            # head with different color than body
            if k == 0:
                pygame.draw.rect(screen, blue, (pos[0] * SIZE, pos[1] * SIZE, SIZE, SIZE))
            # body with different color than head
            else:
                pygame.draw.rect(screen, black, (pos[0] * SIZE, pos[1] * SIZE, SIZE, SIZE))


        # update screen
        pygame.display.flip()


def heuristic(pos, goal):
    """
    return  number of steps
    from pos (x , y) to goal (i , j)
    """
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])



def food_pos(snake, faraway = False):
    """
    return random food position
    if 'faraway' is True , it returns a faraway food position relative to head of snake
    """

    while True:
        position = random.randrange(HEIGHT), random.randrange(WIDTH)

        if faraway:
            if position not in snake and heuristic(body[0], position) > 15:
                return position
        else:
            if position not in snake:
                return position




def over_borders(pos):
    """
    return True if over-borders
    else return None
    """
    pos = list(pos)

    if pos[0] > HEIGHT - 1 :
        return True

    elif pos[0] < 0:
        return True

    elif pos[1] < 0:
        return True

    elif pos[1] > WIDTH - 1:
        return True

    return None

def possibilities(pos, food):
    """
    returns a list of all possible coordinates according to number of steps to food
    first index is closest to food
    """
    possible = [
        (0,1),
        (0,-1),
        (1,0),
        (-1,0)
    ]
    coordinates = {}
    for x, y in possible:
        new_coord = tuple(sum(z) for z in zip(pos,(x,y) ))
        if over_borders(new_coord):
            continue
        steps = heuristic(new_coord, food)
        coordinates.update({new_coord: steps})

    coordinates = dict(sorted(coordinates.items(), key=lambda item: item[1]))

    return list(coordinates.keys())


def backtrack(the_pos, the_food, the_body, visited=None, sec_food = 0, change= None):
    """
    returns most efficient move using backtrack algorithm
    if no possible move return None
    'sec_food' makes sure that the snake doesn't surround itself and loses, by looking for another 'food'
    """
    if visited is None:
        visited = [
            [],
            []
        ]

    if change is None:
        change = [0]

    # Found first food
    if the_pos == the_food and sec_food == 0:
        sec_food = 1

    # Get second food
    if the_pos == the_food and change[0] == 0:
        the_food = food_pos(body,faraway=True)
        change[0] = 1

    # Recursion Base
    if the_pos == the_food and sec_food == 1:
        return the_pos

    # Append visited moves
    visited[sec_food].append(the_pos)

    # Iterate through possible moves
    for coordinate in possibilities(the_pos, the_food):
        my_body = the_body.copy()

        # Already visited
        if sec_food == 0 and coordinate in visited[0]:
            continue
        if sec_food == 1 and coordinate in visited[1]:
            continue

        # Don't touch the body
        if coordinate not in the_body:

            # Update body of snake in recursion
            if coordinate not in my_body:
                my_body.insert(0, coordinate)
                del my_body[-1]

            result = backtrack(coordinate, the_food, my_body, visited, sec_food=sec_food, change=change)

            if result is not None:
                return coordinate

    return None

if __name__ == "__main__":
    main()
