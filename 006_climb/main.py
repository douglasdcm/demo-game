import pygame
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

CEIL = 40
LEVELS = int(SCREEN_HEIGHT / CEIL) - 1
FPS = 60
KEY_PRESSED_DELAY = 1000


class Floor(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load("sport.png").convert_alpha()
        self.rect = pygame.rect.Rect(10, 50, 50, 10)
        self.step = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load("sport.png").convert_alpha()
        self.rect = pygame.rect.Rect(100, 100, 10, 10)
        self.gravity = 0
        self.floor = None

    def jump(self):
        self.rect.y -= 50

    def fall(self):
        if self.rect.bottom == self.floor.rect.top:
            self.gravity = 0
            return
        self.gravity += 2
        self.rect.y += self.gravity


class Game:
    def __init__(self):
        pass

    def init(self):
        self.reset = False
        pygame.init()
        pygame.display.set_caption("Climb")

        self.FONT = pygame.font.SysFont("comicsans", 30)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player_group = pygame.sprite.GroupSingle()
        self.floor_group = pygame.sprite.Group()
        self.player = Player(self.player_group)
        self.floor_index = -1

        self.floors = []
        for _ in range(LEVELS):
            self.floors.append(Floor(self.floor_group))

        level = CEIL
        for floor in self.floors:
            floor.rect.y = level
            floor.rect.x = random.randint(0, SCREEN_WIDTH - floor.rect.width)
            level += CEIL

        self.player.floor = self.floors[self.floor_index]
        self.player.rect.bottom = self.player.floor.rect.top

    def update(self):
        self.clock.tick(FPS)
        self.player.fall()

        if self.player.rect.top > SCREEN_HEIGHT:
            self.reset = True

        self.player.rect.centerx = self.player.floor.rect.centerx
        for floor_ in self.floors:
            if floor_.rect.left < 0 or floor_.rect.right > SCREEN_HEIGHT:
                floor_.step = -floor_.step

            floor_.rect.x += floor_.step

            try:
                next_floor = self.floors[self.floor_index - 1]
            except:
                self.reset = True
                return
            if self.player.rect.bottom < self.player.floor.rect.top and (
                self.player.rect.left > next_floor.rect.left
                and self.player.rect.right < next_floor.rect.right
            ):
                self.player.floor = next_floor
                self.floor_index -= 1

            self.player.gravity = 0

    def draw(self):
        self.screen.fill("black")
        self.player_group.draw(self.screen)
        for floor in self.floors:
            pygame.draw.rect(self.screen, "red", floor.rect)
        pygame.draw.rect(self.screen, "blue", self.player.rect)
        pygame.display.flip()

    def execute(self):
        self.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.player.jump()

            self.update()
            self.draw()
            if self.reset:
                text = self.FONT.render(("Finished"), 1, "white")
                self.screen.blit(
                    text,
                    ((SCREEN_WIDTH - text.get_width()) / 2, 100),
                )
                pygame.display.flip()

                pygame.time.wait(1000)
                self.init()


def main():
    Game().execute()


if __name__ == "__main__":
    main()
