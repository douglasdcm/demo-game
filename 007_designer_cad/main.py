import pygame
from classes import Canvas


def main():
    canvas = Canvas()
    canvas.load_file()
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
                    canvas.press(event.pos)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    canvas.reset_all()

        canvas.handle_actions()
        canvas.draw()


if __name__ == "__main__":
    main()
