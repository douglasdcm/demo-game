import pygame
import time
import random

pygame.init()


FONT = pygame.font.SysFont("comicsans", 30)
CONCURRENT_STARS = 3
DEBUG = False

pygame.display.set_caption("Space Dodge")


def debug_with_rect(app, rect):
    if DEBUG is True:
        pygame.draw.rect(app.win, "blue", rect)


def __generate_stars(app, stars, player_rect):
    for star in stars[:]:
        star_rect = star.rect()
        if star_rect.y > app.height:
            stars.remove(star)
        elif star_rect.y + star_rect.height >= player_rect.y and star_rect.colliderect(
            player_rect
        ):
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

    def draw(self, stars, elapsed_time, player):
        self._win.blit(self._bdg_image, (0, 0))

        time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
        self._win.blit(time_text, (10, 10))

        player.draw()

        for star in stars:
            star.draw()

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
    def __init__(self, app) -> None:
        self._app = app
        self._WIDTH = 40
        self._HEIGHT = 60
        self._VELOCITY = 5
        self._x = 200
        self._y = self._app.height - self._HEIGHT
        self._image = pygame.transform.scale(
            pygame.image.load("space-shuttle.png"),
            (self._WIDTH, self._HEIGHT),
        )
        self._rect = pygame.Rect(
            self._x,
            self._y,
            self._WIDTH,
            self._HEIGHT,
        )

    def rect(self):
        return self._rect

    def draw(self):
        debug_with_rect(self._app, self._rect)
        self._app.win.blit(self._image, (self._rect.x, self._rect.y))

    def move(self):
        player_rect = self._rect
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.x - self._VELOCITY >= 0:
            player_rect.x -= self._VELOCITY

        if (
            keys[pygame.K_RIGHT]
            and player_rect.x + self._VELOCITY + player_rect.width <= self._app.width
        ):
            player_rect.x += self._VELOCITY


class Star:
    def __init__(self, app) -> None:
        self._app = app
        self._WIDTH = 20
        self._HEIGHT = 20
        self._VELOCITY = 10
        self._x = random.randint(0, self._app.width - self._WIDTH)
        self._y = 0
        self._image = pygame.transform.scale(
            pygame.image.load("asteroid.png"),
            (self._WIDTH, self._HEIGHT),
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._WIDTH

    @property
    def height(self):
        return self._HEIGHT

    @property
    def velocity(self):
        return self._VELOCITY

    def update_y(self):
        self._y += self.velocity

    def rect(self):
        self.update_y()
        return pygame.Rect(self.x, self.y, self._WIDTH, self._HEIGHT)

    def draw(self):
        debug_with_rect(self._app, self.rect())
        self._app.win.blit(self._image, (self._x, self._y))


def main():
    app = App()

    stars = []

    player = Player(app)
    player_rect = player.rect()

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    image = pygame.image.load("space-shuttle.png")
    app.win.blit(image, (50, 50))

    while app.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.run = False
                break

        clock.tick(60)
        elapsed_time = time.time() - start_time
        app.star_count += clock.tick(60)

        if app.star_count > app.star_add_increment:
            for _ in range(CONCURRENT_STARS):
                star = Star(app)
                stars.append(star)

            app.star_add_increment = max(200, app.star_add_increment - 50)
            app.star_count = 0

        __generate_stars(app, stars, player_rect)

        player.move()

        if app.hit:
            app.lose()
            break

        app.draw(stars, elapsed_time, player)

    app.quit()


if __name__ == "__main__":
    main()
