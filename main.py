import pygame


def main():
    screen_width = 240
    screen_height = 180

    xpos = 50
    ypos = 50
    step_x = 10
    step_y = 10

    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    screen = pygame.display.set_mode((screen_width, screen_height))

    bdg_image = pygame.image.load("background.png")
    screen.blit(bdg_image, (0, 0))

    image = pygame.image.load("01_image.png")
    image.set_colorkey((255, 0, 255))
    screen.blit(image, (xpos, ypos))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if xpos > screen_width - 64 or xpos < 0:
            step_x = -step_x

        if ypos > screen_height - 64 or ypos < 0:
            step_y = -step_y

        xpos += step_x
        ypos += step_y

        screen.blit(bdg_image, (0, 0))
        screen.blit(image, (xpos, ypos))

        pygame.display.flip()


if __name__ == "__main__":
    main()
