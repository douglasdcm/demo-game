import pygame
from constants import SCREEN_WIDTH


class Body:
    def __init__(self, peice, hide) -> None:
        self.piece = peice
        self.hide = hide


class Player(pygame.sprite.Sprite):
    def __init__(self, starter_x, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        HEAD_SIZE = 25
        CHEST_SIZE = 50
        self.ARM_LENGHT = 50
        self.ARM_THICKNESS = 20
        self.LEG_LENGHT = 100
        self.LEG_THICKNESS = 20
        self.step = 5

        self._starter_x = starter_x

        self._head = pygame.rect.Rect(self._starter_x, 50, HEAD_SIZE, HEAD_SIZE)
        self._chest = pygame.rect.Rect(
            self._head.left, self._head.bottom, CHEST_SIZE, CHEST_SIZE
        )

        self._leg1 = pygame.rect.Rect(
            self._chest.x,
            self._chest.y + self._chest.height,
            self.LEG_THICKNESS,
            self.LEG_LENGHT,
        )

        self._arm = None
        self._leg2 = None
        self.__set_rect()
        self.set_image()

        self._body = [
            Body(self._head, False),
            Body(self._chest, False),
            Body(self._leg1, False),
        ]

    def set_image(self, image="sport.png"):
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(),
            (self.rect.width, self.rect.height),
        )

    def __set_rect(self, additional_peice=None):
        union = pygame.rect.Rect.union(self._head, self._chest)
        union = pygame.rect.Rect.union(union, self._leg1)
        if additional_peice:
            self.rect = pygame.rect.Rect.union(union, additional_peice)
            return
        self.rect = union

    def update(self, screen):
        self.image.set_colorkey((255, 255, 255))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __move(self, rect, direction):
        if direction == "right" and self.rect.right <= SCREEN_WIDTH:
            rect.x += self.step
        if direction == "left" and 0 <= self.rect.left:
            rect.x -= self.step

    def set_rect(self, rect):
        self._head = rect

    def move(self, direction):
        for piece in self._body:
            self.__move(piece.piece, direction)
            self.__set_rect()

    def punch(self):
        self.__set_rect(self._arm)
        self.set_image("martial-arts.png")

    def kick(self):
        self.__set_rect(self._leg2)
        self.set_image("kicking.png")

    def rest(self):
        self.__set_rect()
        self.set_image()


class Player1(Player):
    def __init__(self, starter_x, *groups):
        super().__init__(starter_x, *groups)

        self._arm = pygame.rect.Rect(
            self._chest.right,
            self._chest.centery,
            self.ARM_LENGHT,
            self.ARM_THICKNESS,
        )
        self._leg2 = pygame.rect.Rect(
            self._chest.right,
            self._chest.bottom,
            self.LEG_LENGHT,
            self.LEG_THICKNESS,
        )
        self._body.append(Body(self._arm, True)),
        self._body.append(Body(self._leg2, True)),


class Player2(Player):
    def __init__(self, starter_x, *groups):
        super().__init__(starter_x, *groups)

        self.step = 20
        self._arm = pygame.rect.Rect(
            self._chest.left - self.ARM_LENGHT,
            self._chest.centery,
            self.ARM_LENGHT,
            self.ARM_THICKNESS,
        )
        self._leg2 = pygame.rect.Rect(
            self._chest.left - self.LEG_LENGHT,
            self._chest.bottom,
            self.LEG_LENGHT,
            self.LEG_THICKNESS,
        )
        self._body.append(Body(self._arm, True)),
        self._body.append(Body(self._leg2, True)),

    def set_image(self, image="sport.png"):
        image = pygame.image.load(image)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(
            image.convert_alpha(),
            (self.rect.width, self.rect.height),
        )
        self.image = image
