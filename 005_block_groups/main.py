import pygame
import random

SCREEN_WIDTH = SCREEN_HEIGHT = 400
SCREEN_COLOR = "gray"
FPS = 60


class Body:
    def __init__(self, peice, hide) -> None:
        self.piece = peice
        self.hide = hide


class Player(pygame.sprite.Sprite):
    def __init__(self, starter_x, player_number, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        HEAD_SIZE = 25
        CHEST_SIZE = 50
        ARM_LENGHT = 50
        ARM_THICKNESS = 20
        LEG_LENGHT = 100
        LEG_THICKNESS = 20

        self._starter_x = starter_x
        self._head = pygame.rect.Rect(self._starter_x, 50, HEAD_SIZE, HEAD_SIZE)
        self._chest = pygame.rect.Rect(
            self._head.x, self._head.y + self._head.height, CHEST_SIZE, CHEST_SIZE
        )
        if player_number == 1:
            self._arm = pygame.rect.Rect(
                self._chest.x + self._chest.width,
                self._head.y + self._head.height,
                ARM_LENGHT,
                ARM_THICKNESS,
            )
            self._leg2 = pygame.rect.Rect(
                self._chest.x + self._chest.width,
                self._chest.y + self._chest.height,
                LEG_LENGHT,
                LEG_THICKNESS,
            )
        else:
            self._arm = pygame.rect.Rect(
                self._head.x - ARM_LENGHT,
                self._head.y + self._head.height,
                ARM_LENGHT,
                ARM_THICKNESS,
            )
            self._leg2 = pygame.rect.Rect(
                self._chest.x - LEG_LENGHT,
                self._chest.y + self._chest.height,
                LEG_LENGHT,
                LEG_THICKNESS,
            )

        self._leg1 = pygame.rect.Rect(
            self._chest.x, self._chest.y + self._chest.height, LEG_THICKNESS, LEG_LENGHT
        )

        self.__set_rect()
        self.__set_image()

        self._body = [
            Body(self._head, False),
            Body(self._chest, False),
            Body(self._arm, True),
            Body(self._leg1, False),
            Body(self._leg2, True),
        ]

    def __set_image(self, image="sport.png"):
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            (self.rect.width, self.rect.height),
        )

    def __set_rect(self, additional_peice=None):
        union = pygame.rect.Rect.union(self._head, self._chest)
        union = pygame.rect.Rect.union(union, self._leg1)
        if additional_peice:
            union = pygame.rect.Rect.union(union, additional_peice)
        self.rect = union

    def __draw(self, screen, color, rect):
        pygame.draw.rect(screen, color, rect)
        self.image.set_colorkey((255, 255, 255))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __move(self, rect, direction):
        step = 1
        if direction == "right" and (self.rect.x + self.rect.width) <= SCREEN_WIDTH:
            rect.x += step
        if direction == "left" and 0 <= self.rect.x:
            rect.x -= step

    def set_rect(self, rect):
        self._head = rect

    def draw(self, screen):
        self.__draw(screen, "red", self.rect)

        for piece in self._body:
            if piece.hide is False:
                self.__draw(screen, "blue", piece.piece)

    def move(self, direction):
        for piece in self._body:
            self.__move(piece.piece, direction)
            self.__set_rect()

    def punch(self, screen):
        self.__set_image("boxing-fighter.png")
        self.__set_rect(self._arm)
        self.__draw(screen, "white", self._arm)

    def kick(self, screen):
        self.__set_rect(self._leg2)
        self.__draw(screen, "white", self._leg2)

    def rest(self):
        self.__set_rect()
        self.__set_image()


def __draw_text(FONT, screen):
    score_text = FONT.render(f"POW", 1, "white")
    screen.blit(
        score_text,
        (10, 10),
    )


def __get_collisions(obj, group, dokill):
    return len(pygame.sprite.spritecollide(obj, group, dokill))


def main():
    pygame.init()
    FONT = pygame.font.SysFont("comicsans", 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    directions = ["left", "right", "stop"]
    actions = ["punch", "kick", "rest"]

    player1_group = pygame.sprite.Group()
    player2_group = pygame.sprite.Group()
    player1 = Player(0, 1, player1_group)
    player2 = Player(200, 2, player2_group)

    players = []
    players.append(player1)
    players.append(player2)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()

        clock.tick(FPS)

        screen.fill(SCREEN_COLOR)
        player1.draw(screen)
        player2.draw(screen)

        for player in players:
            __moviment_player1(screen, player1, keys, player)
            __moviment_player2(screen, directions, actions, player2, player)

        collisions = __get_collisions(player1, player2_group, dokill=False)
        if collisions:
            __draw_text(FONT, screen)

        if not keys.count(True):
            for player in players:
                player.rest()

        pygame.display.flip()


def __moviment_player2(screen, directions, actions, player2, player):
    if player is player2:
        direction = random.choice(directions)
        action = random.choice(actions)
        player.move(direction)
        if action == "punch":
            player.punch(screen)
        elif action == "kick":
            player.kick(screen)
        else:
            pass


def __moviment_player1(screen, player1, keys, player):
    if player is player1:
        if keys[pygame.K_w]:
            player.move("right")
        if keys[pygame.K_q]:
            player.move("left")
        if keys[pygame.K_p]:
            player.punch(screen)
        if keys[pygame.K_k]:
            player.kick(screen)


if __name__ == "__main__":
    main()
