import pygame
import time
import random

pygame.init()


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

STAR_WIDHT = 10
STAR_HEIGHT = 20
FONT = pygame.font.SysFont("comicsans", 30)
CONCURRENT_STARS = 3

pygame.display.set_caption("Space Dodge")


def __generate_stars(app, stars, player):
    STAR_VEL = 10

    for star in stars[:]:
        star.y += STAR_VEL
        if star.y > app.height:
            stars.remove(star)
        elif star.y + star.height >= player.y and star.colliderect(player):
            stars.remove(star)
            app.hit = True
            break


class App:
    def __init__(self) -> None:
        self._run = True
        self._star_add_increment = 500
        self._star_count = 0
        self._hit = False
        self._WIDTH, self._HEIGHT = 800, 600
        self._win = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        self._bdg_image = pygame.transform.scale(
            pygame.image.load("space.jpg"), (self._WIDTH, self._HEIGHT)
        )

    @property
    def win(self):
        return self._win

    @property
    def width(self):
        return self._WIDTH

    @property
    def height(self):
        return self._HEIGHT

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    @property
    def star_add_increment(self):
        return self._star_add_increment

    @star_add_increment.setter
    def star_add_increment(self, value):
        self._star_add_increment = value

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        self._run = value

    @property
    def star_count(self):
        return self._star_count

    @star_count.setter
    def star_count(self, value):
        self._star_count = value

    def run_loop(self):
        pass

    def draw(self, player, stars, elapsed_time):
        self._win.blit(self._bdg_image, (0, 0))

        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
        self._win.blit(time_text, (10, 10))

        pygame.draw.rect(self._win, "blue", player)

        for star in stars:
            pygame.draw.rect(self._win, "white", star)

        pygame.display.flip()

    def update(self):
        pygame.display.update()

    def quit(self):
        pygame.quit()

    def lose(self):
        DELAY = 2000
        lost_text = FONT.render("You lost!", 1, "yellow")
        self.win.blit(
            lost_text,
            (
                self._WIDTH / 2 - lost_text.get_width() / 2,
                self._HEIGHT / 2 - lost_text.get_height() / 2,
            ),
        )
        self.update()
        pygame.time.delay(DELAY)


class Player:
    def body(self, app):
        return pygame.Rect(200, app.height - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move_left(self):
        pass


class Star:
    def __init__(self, app) -> None:
        self._app = app

    @property
    def x(self):
        return random.randint(0, self._app.width - STAR_WIDHT)

    @property
    def y(self):
        pass

    def body(self):
        return pygame.Rect(self.x, -STAR_HEIGHT, STAR_WIDHT, STAR_HEIGHT)


def main():
    app = App()

    stars = []

    player = Player().body(app)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    while app.run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        app.star_count += clock.tick(60)

        if app.star_count > app.star_add_increment:
            for _ in range(CONCURRENT_STARS):
                star = Star(app).body()
                stars.append(star)

            app.star_add_increment = max(200, app.star_add_increment - 50)
            app.star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= app.width:
            player.x += PLAYER_VEL

        __generate_stars(app, stars, player)

        if app.hit:
            app.lose()
            break

        app.draw(player, stars, elapsed_time)

    app.quit()


if __name__ == "__main__":
    main()
