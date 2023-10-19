import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

STAR_WIDHT = 10
STAR_HEIGHT = 20
STAR_VEL = 10
FONT = pygame.font.SysFont("comicsans", 30)
bdg_image = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))

pygame.display.set_caption("Space Dodge")


def draw(player, stars, elapsed_time):
    WIN.blit(bdg_image, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.flip()


class App:
    def __init__(self) -> None:
        self._run = True
        self._star_add_increment = 500
        self._star_count = 0

    @property
    def star_add_increment(self):
        return self._star_add_increment

    @star_add_increment.setter
    def star_add_increment(self, value):
        self._star_add_increment = value

    @property
    def run(self):
        return self._run

    @property
    def star_count(self):
        return self._star_count

    @star_count.setter
    def star_count(self, value):
        self._star_count = value

    def run_loop(self):
        pass

    def render(self):
        pass


def main():
    app = App()

    stars = []
    hit = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    while app.run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        app.star_count += clock.tick(60)

        if app.star_count > app.star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDHT)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDHT, STAR_HEIGHT)
                stars.append(star)

            app.star_add_increment = max(200, app.star_add_increment - 50)
            app.star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lost!", 1, "yellow")
            WIN.blit(
                lost_text,
                (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, stars, elapsed_time)

    pygame.quit()


if __name__ == "__main__":
    main()
