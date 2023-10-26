import pygame
import random

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_BACKGROUND = "black"
FPS = 2
SQUARE_SIDE = 50
ENEMIES = 10
ENEMIES_STEP_X = (35, 85)
ENEMIES_STEP_Y = (25, 75)


class Character(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.rect = pygame.rect.Rect(0, 0, SQUARE_SIDE, SQUARE_SIDE)
        self.image = pygame.transform.scale(
            pygame.image.load("sad-face.png"),
            (self.rect.width, self.rect.height),
        )
        self.step_x = 10
        self.step_y = 10
        self.color = "red"

    def walk_x(self):
        if (
            self.rect.x > (SCREEN_WIDTH - self.rect.width - self.step_x)
            or self.rect.x + self.step_x < 0
        ):
            self.step_x = -self.step_x
        self.rect.x += self.step_x

    def walk_y(self):
        if (
            self.rect.y > (SCREEN_HEIGHT - self.rect.height - self.step_y)
            or self.rect.y + self.step_y < 0
        ):
            self.step_y = -self.step_y
        self.rect.y += self.step_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))


def has_collided(obj, group, dokill):
    collisions = len(pygame.sprite.spritecollide(obj, group, dokill))
    return collisions > 0


def main():
    pygame.init()
    FONT = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    player = Character(player_group)
    player.color = "blue"
    player.step = 50
    player.rect = pygame.rect.Rect(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SQUARE_SIDE, SQUARE_SIDE
    )
    player.image = pygame.transform.scale(
        pygame.image.load("happiness.png"),
        (player.rect.width, player.rect.height),
    )

    enemies = []
    for _ in range(ENEMIES):
        enemy = Character(enemies_group)
        enemy.step_x = random.randint(*ENEMIES_STEP_X)
        enemy.step_y = random.randint(*ENEMIES_STEP_Y)
        enemies.append(enemy)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        clock.tick(FPS)

        screen.fill(SCREEN_BACKGROUND)

        for enemy in enemies:
            enemy.walk_x()
            enemy.walk_y()
            enemy.draw(screen)

            player.draw(screen)

            pygame.display.flip()

            if has_collided(player, enemies_group, dokill=False) is True:
                time_text = FONT.render(f"Collision", 1, "white")
                screen.blit(
                    time_text,
                    ((SCREEN_WIDTH - time_text.get_width()) / 2, SCREEN_HEIGHT / 2),
                )
                pygame.display.flip()
                # pygame.time.wait(2000)


if __name__ == "__main__":
    main()
