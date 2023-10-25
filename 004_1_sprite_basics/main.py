import pygame
import random

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_BACKGROUND = "black"
FPS = 2


class Object1(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.rect = None
        self.image = None

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Object2(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.rect = None
        self.image = None

    def draw(self, screen):
        pygame.draw.rect(screen, "red", self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))


def has_collided(obj, group, dokill):
    collisions = len(pygame.sprite.spritecollide(obj, group, dokill))
    return collisions > 0


def main():
    pygame.init()
    FONT = pygame.font.SysFont("comicsans", 30)

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    groupA = pygame.sprite.Group()
    groupB = pygame.sprite.Group()
    obj1 = Object1(groupA)
    obj2 = Object2(groupB)
    obj3 = Object2(groupB)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        clock.tick(FPS)

        screen.fill(SCREEN_BACKGROUND)

        ROOT = 100
        x = random.randint(0, SCREEN_WIDTH - ROOT)
        y = random.randint(0, SCREEN_HEIGHT - ROOT)
        rect1 = pygame.rect.Rect(x, y, ROOT, ROOT)

        x = random.randint(0, SCREEN_WIDTH - ROOT)
        y = random.randint(0, SCREEN_HEIGHT - ROOT)
        rect2 = pygame.rect.Rect(x, y, ROOT, ROOT)

        x = random.randint(0, SCREEN_WIDTH - ROOT)
        y = random.randint(0, SCREEN_HEIGHT - ROOT)
        rect3 = pygame.rect.Rect(x, y, ROOT, ROOT)

        obj1.rect = rect1
        obj2.rect = rect2
        obj3.rect = rect3

        obj1.image = pygame.transform.scale(
            pygame.image.load("happiness.png"),
            (rect1.width, rect1.height),
        )
        obj2.image = pygame.transform.scale(
            pygame.image.load("sad-face.png"),
            (rect2.width, rect2.height),
        )
        obj3.image = pygame.transform.scale(
            pygame.image.load("sad-face.png"),
            (rect2.width, rect2.height),
        )

        obj1.draw(screen)
        obj2.draw(screen)
        obj3.draw(screen)
        pygame.display.flip()

        if has_collided(obj1, groupB, dokill=False) is True:
            time_text = FONT.render(f"Collision", 1, "white")
            screen.blit(
                time_text,
                ((SCREEN_WIDTH - time_text.get_width()) / 2, SCREEN_HEIGHT / 2),
            )
            pygame.display.flip()
            pygame.time.wait(2000)


if __name__ == "__main__":
    main()
