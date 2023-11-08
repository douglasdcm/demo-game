import pygame


BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
MARGIN = 10


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.image = pygame.transform.scale(
            pygame.image.load("error.png").convert(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )

    def press(self):
        NotImplemented


class MenuButton(Button):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(MARGIN, MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.image = pygame.transform.scale(
            pygame.image.load("question.png").convert_alpha(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )


class RectButton(Button):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(
            MARGIN, MARGIN * 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
        )
        self.image = pygame.transform.scale(
            pygame.image.load("rectangle.png").convert_alpha(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )


class Canvas:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.menu_button = MenuButton()
        self.rect_button = RectButton()
        self.__menu_group = pygame.sprite.GroupSingle()
        self.__menu_group.add(self.menu_button)
        self.__rect_group = pygame.sprite.GroupSingle()
        self.__rect_group.add(self.rect_button)
        self.__commands = {"rect": self.__draw_rect, "menu": self.__open_menu}
        self.current_action = None
        self.mouse_positions = []
        self.__shapes = []

    def __draw_rect(self, params):
        rect = pygame.rect.Rect(params)
        self.__shapes.append(rect)
        return rect

    def __open_menu(self):
        msg = "Click the shapes to draw"
        print(msg)
        return msg

    def do_command(self, command, params=None):
        action = self.__commands.get(command.lower())
        if params:
            return action(params)
        return action()

    def press(self, mouse_pos):
        if self.rect_button.rect.collidepoint(mouse_pos):
            return "rect"

        if self.menu_button.rect.collidepoint(mouse_pos):
            return "menu"

    def draw(self):
        self.screen.fill("gray")
        for shape in self.__shapes:
            if isinstance(shape, pygame.rect.Rect):
                pygame.draw.rect(self.screen, "blue", shape)

        self.screen.blit(
            self.menu_button.image,
            (self.menu_button.rect.x, self.menu_button.rect.y),
        )

        self.screen.blit(
            self.rect_button.image,
            (self.rect_button.rect.x, self.rect_button.rect.y),
        )

        pygame.display.flip()

    def action_reset(self):
        self.current_action = None
        self.mouse_positions = []

    def dump_to_file(self):
        with open("picture.txt", "w") as f:
            for shape in self.__shapes:
                f.write(f"{shape}\n")


def __handle_actions(canvas: Canvas):
    if canvas.current_action == "rect" and len(canvas.mouse_positions) == 2:
        width = abs(canvas.mouse_positions[0][0] - canvas.mouse_positions[1][0])
        height = abs(canvas.mouse_positions[0][1] - canvas.mouse_positions[1][1])
        canvas.do_command(
            canvas.current_action, (*canvas.mouse_positions[0], width, height)
        )
        canvas.action_reset()

    if canvas.current_action == "menu":
        canvas.do_command(canvas.current_action)
        canvas.action_reset()


def main():
    canvas = Canvas()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                canvas.dump_to_file()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if canvas.current_action:
                    canvas.mouse_positions.append(event.pos)
                else:
                    canvas.current_action = canvas.press(event.pos)

        __handle_actions(canvas)

        canvas.draw()


if __name__ == "__main__":
    main()
