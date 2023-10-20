import pygame
from pygame.locals import *


class App:
    def __init__(self) -> None:
        self._running = True
        self._display_surf = None
        self._size = self.weight, self.height = 240, 180
        self._xpos = 50
        self._ypos = 50
        self._step_x = 10
        self._step_y = 10
        self._bdg_image = pygame.image.load("background.png")

    def on_init(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("minimal program")

        self._display_surf = pygame.display.set_mode(
            self._size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self._display_surf.blit(self._bdg_image, (0, 0))
        pygame.display.flip()

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self._display_surf.blit(self._bdg_image, (0, 0))

        if self._xpos > self.weight - 64 or self._xpos < 0:
            self._step_x = -self._step_x

        if self._ypos > self.height - 64 or self._ypos < 0:
            self._step_y = -self._step_y

        self._xpos += self._step_x
        self._ypos += self._step_y

        image = pygame.image.load("01_image.png")
        image.set_colorkey((255, 0, 255))
        self._display_surf.blit(image, (self._xpos, self._ypos))

    def on_render(self):
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running == False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
