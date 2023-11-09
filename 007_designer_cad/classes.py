import pygame

BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
MARGIN = 10
DEFAULT_BUTTON_COLOR = "gray"


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.image = pygame.transform.scale(
            pygame.image.load("error.png").convert(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )
        self.color = DEFAULT_BUTTON_COLOR

    def press(self):
        NotImplemented


class HelpButton(Button):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(MARGIN, MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.image = pygame.transform.scale(
            pygame.image.load("question.png").convert_alpha(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )

    def press(self):
        print("Click the shapes to draw\nESCAPE: aborts the current command")


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

    def press(self, params):
        return pygame.rect.Rect(params)


class ClearAllButton(Button):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(
            MARGIN, MARGIN * 3 + 2 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT
        )
        self.image = pygame.transform.scale(
            pygame.image.load("dust.png").convert_alpha(),
            (BUTTON_WIDTH, BUTTON_HEIGHT),
        )


class Canvas:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.__buttons_init()
        self.__commands = {
            "rect": self.button_rect.press,
            "help": self.button_help.press,
            "clear_all": self.clear_all,
        }
        self.current_action = None
        self.pressed_button = None
        self.mouse_positions = []
        self.__shapes = []

    def __buttons_init(self):
        self.button_rect = RectButton()
        self.__group_rect = pygame.sprite.GroupSingle()
        self.__group_rect.add(self.button_rect)

        self.button_help = HelpButton()
        self.__group_help = pygame.sprite.GroupSingle()
        self.__group_help.add(self.button_help)

        self.button_clear_all = ClearAllButton()
        self.__group_clear_all = pygame.sprite.GroupSingle()
        self.__group_clear_all.add(self.button_clear_all)

    def clear_all(self):
        self.__shapes = []

    def do_command(self, command, params=None):
        outcome = None
        action = self.__commands.get(command.lower())
        if params:
            outcome = action(params)
        else:
            outcome = action()
        self.__shapes.append(outcome)

    def press(self, mouse_pos):
        if self.button_rect.rect.collidepoint(mouse_pos):
            print("Requires two points")
            self.__press(self.button_rect)
            self.current_action = "rect"

        if self.button_help.rect.collidepoint(mouse_pos):
            self.__press(self.button_rect)
            self.current_action = "help"

        if self.button_clear_all.rect.collidepoint(mouse_pos):
            self.clear_all()
            self.current_action = None

    def __press(self, button: Button):
        button.color = "coral"
        self.pressed_button = button

    def draw(self):
        self.screen.fill("black")

        for shape in self.__shapes:
            if isinstance(shape, pygame.rect.Rect):
                pygame.draw.rect(self.screen, "blue", shape)

        for mouse_position in self.mouse_positions:
            pygame.draw.line(self.screen, "white", mouse_position, mouse_position)

        buttons = [self.button_clear_all, self.button_help, self.button_rect]

        for button in buttons:
            pygame.draw.rect(self.screen, button.color, button, border_radius=5)

            self.screen.blit(
                button.image,
                (button.rect.x, button.rect.y),
            )

        pygame.display.flip()

    def mouse_reset(self):
        self.mouse_positions = []

    def action_reset(self):
        self.current_action = None

    def reset_all(self):
        self.pressed_button.color = DEFAULT_BUTTON_COLOR
        self.mouse_reset()
        self.action_reset()

    def dump_to_file(self):
        with open("picture.txt", "w") as f:
            for shape in self.__shapes:
                f.write(f"{shape}\n")

    def handle_actions(self):
        if self.current_action == "rect" and len(self.mouse_positions) == 2:
            x1 = self.mouse_positions[0][0]
            y1 = self.mouse_positions[0][1]

            x2 = self.mouse_positions[1][0]
            y2 = self.mouse_positions[1][1]

            width = abs(x1 - x2)
            height = abs(y1 - y2)

            self.do_command(
                self.current_action, (*self.mouse_positions[0], width, height)
            )
            self.mouse_reset()

        if self.current_action == "help":
            self.do_command(self.current_action)
            self.reset_all()
