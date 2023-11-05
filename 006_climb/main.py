import pygame
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load("sport.png").convert_alpha()
        self.rect = pygame.rect.Rect(10, 50, 100, 10)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load("sport.png").convert_alpha()
        self.rect = pygame.rect.Rect(100, 100, 10, 10)


def main():
    def handle_events():
        pass

    def update():
        player.rect.bottom = floor.rect.top
        player.rect.left = floor.rect.left

    def draw():
        screen.fill("black")
        player_group.draw(screen)
        for floor in floors:
            pygame.draw.rect(screen, "red", floor.rect)
        pygame.draw.rect(screen, "blue", player.rect)

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player_group = pygame.sprite.GroupSingle()
    floor_group = pygame.sprite.Group()
    player = Player(player_group)
    floor = Floor(floor_group)

    floors = []
    for _ in range(3):
        floors.append(Floor(floor_group))

    for floor in floors:
        floor.rect.y = random.randint(0, SCREEN_HEIGHT)
        floor.rect.x = random.randint(0, SCREEN_WIDTH)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        handle_events()
        update()
        draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()
