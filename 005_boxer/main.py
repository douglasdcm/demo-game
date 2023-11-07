import pygame
import random
from classes import Player1, Player2

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER1_INITIAL_POSITION,
    PLAYER2_INITIAL_POSITION,
    PLAYER2_TIMER,
    KEY_PRESSED_DELAY,
    FPS,
    SCREEN_COLOR,
    DEBUG,
)


def __debug(screen, rect):
    pygame.draw.rect(screen, "blue", rect)


def __draw_text(FONT, screen, text):
    score_text = FONT.render(text, 1, "white")
    screen.blit(
        score_text,
        (10, 10),
    )


def __get_collisions(obj, group, dokill):
    return len(pygame.sprite.spritecollide(obj, group, dokill))


def __moviment_player2(directions, actions, player2, player1_group):
    collisions = 0
    direction = random.choice(directions)
    action = random.choice(actions)
    player2.move(direction)
    if action == "punch":
        player2.punch()
        collisions = __get_collisions(player2, player1_group, dokill=False)
    elif action == "kick":
        player2.kick()
        collisions = __get_collisions(player2, player1_group, dokill=False)
    else:
        pass

    return collisions


def __player1_attack(player1, keys, player2_group):
    collisions = 0
    if keys[pygame.K_p]:
        player1.punch()
        collisions = __get_collisions(player1, player2_group, dokill=False)
    if keys[pygame.K_k]:
        player1.kick()
        collisions = __get_collisions(player1, player2_group, dokill=False)
    return collisions


def __player1_movement(player1, keys):
    if keys[pygame.K_w]:
        player1.move("right")
    if keys[pygame.K_q]:
        player1.move("left")


def __draw_instructions(FONT, screen):
    texts = ["s: start", "q: move left", "w: move right", "p: punch", "k: kick"]
    pos_y = 100
    for text in texts:
        text = FONT.render((text), 1, "white")
        screen.blit(
            text,
            ((SCREEN_WIDTH - text.get_width()) / 2, pos_y),
        )
        pos_y += 40
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Boxe")

    FONT = pygame.font.SysFont("comicsans", 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    start = False
    while start == False:
        __draw_instructions(FONT, screen)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            start = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    game_event = pygame.USEREVENT + 1

    pygame.time.set_timer(
        game_event,
        PLAYER2_TIMER,
    )
    pygame.time.set_timer(pygame.KEYDOWN, 500)

    directions = ["left", "right", "stay"]
    actions = ["punch", "kick", "rest"]

    player1_group = pygame.sprite.GroupSingle()
    player2_group = pygame.sprite.GroupSingle()
    player1 = Player1(PLAYER1_INITIAL_POSITION, player1_group)
    player2 = Player2(PLAYER2_INITIAL_POSITION, player2_group)

    players = []
    players.append(player1)
    players.append(player2)

    clock = pygame.time.Clock()

    player1_score = player2_score = 0
    pygame.key.set_repeat(KEY_PRESSED_DELAY)
    while True:
        clock.tick(FPS)
        player2_point = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == game_event:
                player2_point = __moviment_player2(
                    directions, actions, player2, player1_group
                )
                player2_score += player2_point
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player1_score += __player1_attack(player1, keys, player2_group)

        keys = pygame.key.get_pressed()
        __player1_movement(player1, keys)

        screen.fill(SCREEN_COLOR)
        if DEBUG:
            __debug(screen, player1.rect)
            __debug(screen, player2.rect)
        else:
            player1_group.draw(screen)
            player2_group.draw(screen)
        player1.update(screen)
        player2.update(screen)
        text = f"P1 {player1_score} / P2 {player2_score}"
        __draw_text(FONT, screen, text)

        for player in players:
            player.rest()

        pygame.display.flip()


if __name__ == "__main__":
    main()
