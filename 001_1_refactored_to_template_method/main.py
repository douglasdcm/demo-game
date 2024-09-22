import pygame
import time


class GameTemplate:
    def __init__(self) -> None:
        self.screen_width = 240
        self.screen_height = 180
        self.xpos = 50
        self.ypos = 50
        self.step_x = 10
        self.step_y = 10
        self.screen = None
        self.bdg_image = None
        self.image = None

    def initialize(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bdg_image = pygame.image.load("background.png")
        self.image = pygame.image.load("01_image.png")
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("minimal program")
        self.screen.blit(self.bdg_image, (0, 0))
        self.image.set_colorkey((255, 0, 255))
        self.screen.blit(self.image, (self.xpos, self.ypos))

    def events(self):
        raise NotImplementedError

    def loop(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def pacing(self):
        pass

    def play(self):
        self.events()
        self.loop()
        self.render()
        self.pacing()


class Game(GameTemplate):
    def __init__(self) -> None:
        super().__init__()
        self.running = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def loop(self):
        if self.xpos > self.screen_width - 64 or self.xpos < 0:
            self.step_x = -self.step_x

        if self.ypos > self.screen_height - 64 or self.ypos < 0:
            self.step_y = -self.step_y

        self.xpos += self.step_x
        self.ypos += self.step_y
        return self.xpos, self.ypos

    def render(self):
        self.screen.blit(self.bdg_image, (0, 0))
        self.screen.blit(self.image, (self.xpos, self.ypos))
        pygame.display.flip()

    def pacing(self):
        time.sleep(0.1)


def main():
    game = Game()
    game.initialize()
    while game.running:
        game.play()
    return


if __name__ == "__main__":
    main()
