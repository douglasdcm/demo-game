import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

STAR_WIDHT = 10
STAR_HEIGHT = 20
STAR_VEL = 10
FONT = pygame.font.SysFont("comicsans", 30)
bdg_image = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))

pygame.display.set_caption("Space Dodge")


def draw(player, stars):
    WIN.blit(bdg_image, (0, 0))
    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.flip()


def main():
    run = True

    star_add_increment = 500
    star_count = 0

    stars = []
    hit = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    while run:
        star_count += clock.tick(60)

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDHT)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDHT, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lost!", 1, "white")
            WIN.blit(
                lost_text,
                (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
