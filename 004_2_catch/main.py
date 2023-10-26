import pygame
import random
import time

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_BACKGROUND = "black"

DELAY = 4000

FPS = 60
SQUARE_SIDE = 50

PLAYER_VELOCITY = 5

ENEMIES_QUANTITY = 15
ENEMIES_STEP = (10, 20)
ENEMY_VELOCITY = 0.25


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


class Player(Character):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self._VELOCITY = PLAYER_VELOCITY

    def move(self):
        player_rect = self.rect
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.x - self._VELOCITY >= 0:
            player_rect.x -= self._VELOCITY

        if (
            keys[pygame.K_RIGHT]
            and player_rect.x + self._VELOCITY + player_rect.width <= SCREEN_WIDTH
        ):
            player_rect.x += self._VELOCITY


def __setup_game():
    pygame.init()
    pygame.display.set_caption("Catch me")
    FONT = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return FONT, clock, screen


def __setup_enemies(enemies_group):
    enemies = []
    for _ in range(ENEMIES_QUANTITY):
        enemy = Character(enemies_group)
        enemy.step_x = random.randint(*ENEMIES_STEP) * ENEMY_VELOCITY
        enemy.step_y = random.randint(*ENEMIES_STEP) * ENEMY_VELOCITY
        enemies.append(enemy)
    return enemies


def __setup_player():
    player_group = pygame.sprite.Group()
    player = Player(player_group)
    player.color = "blue"
    player.step = 50
    player.rect = pygame.rect.Rect(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SQUARE_SIDE, SQUARE_SIDE
    )
    player.image = pygame.transform.scale(
        pygame.image.load("happiness.png"),
        (player.rect.width, player.rect.height),
    )

    return player


def __draw_statistics(FONT, screen, demage, elapsed_time):
    score_text = FONT.render(
        f"Demage: {demage} | Time: {round(elapsed_time)}s", 1, "white"
    )
    screen.blit(
        score_text,
        (10, 10),
    )


def __restore_player(player):
    player.color = "blue"
    player.image = pygame.transform.scale(
        pygame.image.load("happiness.png"),
        (player.rect.width, player.rect.height),
    )


def __penalty(player, demage):
    player.color = "yellow"
    player.image = pygame.transform.scale(
        pygame.image.load("pain.png"),
        (player.rect.width, player.rect.height),
    )


def __quit(FONT, screen, demage, elapsed_time):
    score_text = FONT.render(
        f"Score: {round(elapsed_time) - round(demage/10)}", 1, "green"
    )
    screen.blit(
        score_text,
        ((SCREEN_WIDTH - score_text.get_width()) / 2, SCREEN_HEIGHT / 2),
    )
    pygame.display.flip()
    pygame.time.delay(DELAY)


def __draw_instructions(FONT, screen):
    score_text = FONT.render(("""s: start | q: quit | LEFT/RIGHT: move"""), 1, "white")
    screen.blit(
        score_text,
        ((SCREEN_WIDTH - score_text.get_width()) / 2, SCREEN_HEIGHT / 2),
    )
    pygame.display.flip()


def get_collisions(obj, group, dokill):
    return len(pygame.sprite.spritecollide(obj, group, dokill))


def main():
    keys = None
    FONT, clock, screen = __setup_game()
    start = False

    while start == False:
        __draw_instructions(FONT, screen)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            start = True

        if keys[pygame.K_q]:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    player = __setup_player()

    enemies_group = pygame.sprite.Group()
    enemies = __setup_enemies(enemies_group)
    demage = 0
    collisions = 0
    start_time = time.time()
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            __quit(FONT, screen, demage, elapsed_time)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                __quit(FONT, screen, demage, elapsed_time)
                return

        screen.fill(SCREEN_BACKGROUND)

        clock.tick(FPS)

        elapsed_time = time.time() - start_time

        for enemy in enemies:
            enemy.walk_x()
            enemy.walk_y()

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        player.move()

        pygame.display.flip()

        collisions = get_collisions(player, enemies_group, dokill=False)

        if collisions:
            demage += 1
            __penalty(player, demage)
        else:
            __restore_player(player)

        __draw_statistics(FONT, screen, demage, elapsed_time)
        pygame.display.flip()


if __name__ == "__main__":
    main()
