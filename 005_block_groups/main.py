import pygame

SCREEN_WIDTH = SCREEN_HEIGHT = 400
FPS = 20


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self._head = pygame.rect.Rect(50, 50, 25, 25)
        self._chest = pygame.rect.Rect(
            self._head.x, self._head.y + self._head.height, 50, 50
        )
        self._arm = pygame.rect.Rect(
            self._head.x + self._head.width, self._head.y + self._head.height, 50, 20
        )
        self._leg1 = pygame.rect.Rect(
            self._chest.x, self._chest.y + self._chest.height, 20, 100
        )
        self._leg2 = pygame.rect.Rect(
            self._chest.x, self._chest.y + self._chest.height, 100, 20
        )

        self._body = [
            {"piece": self._head, "hide": False},
            {"piece": self._chest, "hide": False},
            {"piece": self._arm, "hide": True},
            {"piece": self._leg1, "hide": False},
            {"piece": self._leg2, "hide": True},
        ]

        self._punch = False
        self._kick = False

    def __draw(self, screen, color, rect):
        pygame.draw.rect(screen, color, rect)

    def __move(self, rect, direction):
        step = 10
        if direction == "right":
            rect.x += step
        else:
            rect.x -= step

    def set_rect(self, rect):
        self._head = rect

    def draw(self, screen):
        for piece in self._body:
            if piece["hide"] is False:
                self.__draw(screen, "blue", piece["piece"])

    def move(self, direction):
        for piece in self._body:
            self.__move(piece["piece"], direction)

    def punch(self, screen):
        if not self._punch:
            self.__draw(screen, "white", self._arm)
        self._punch = not self._punch

    def kick(self, screen):
        if not self._kick:
            self.__draw(screen, "white", self._leg2)
        self._kick = not self._kick


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    group = pygame.sprite.Group()
    player1 = Player(group)

    blocks = []
    blocks.append(player1)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()

        clock.tick(FPS)

        screen.fill("gray")
        player1.draw(screen)

        for player in blocks:
            if keys[pygame.K_w]:
                player.move("right")
            if keys[pygame.K_q]:
                player.move("left")
            if keys[pygame.K_p]:
                player.punch(screen)
            if keys[pygame.K_k]:
                player.kick(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
