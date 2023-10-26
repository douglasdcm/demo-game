import pygame
from main import walk_x, SCREEN_WIDTH


def test_walk_x_is_width_minus_1():
    side = 20
    rect = pygame.rect.Rect((SCREEN_WIDTH - 1, 0, side, side))
    step = 10
    assert walk_x(rect, step, side) == SCREEN_WIDTH - step - 1


def test_walk_x_is_width_plus_1():
    side = 20
    rect = pygame.rect.Rect((SCREEN_WIDTH + 1, 0, side, side))
    step = 10
    assert walk_x(rect, step, side) == SCREEN_WIDTH - step + 1


def test_walk_x_is_width():
    side = 20
    rect = pygame.rect.Rect((SCREEN_WIDTH, 0, side, side))
    step = 10
    assert walk_x(rect, step, side) == SCREEN_WIDTH - step


def test_walk_x_is_0():
    side = 20
    rect = pygame.rect.Rect((0, 0, side, side))
    step = 10
    assert walk_x(rect, step, side) == 10
