import pygame
from main import Canvas


def test_click_rect_button():
    canvas = Canvas()
    mouse_pos = (canvas.rect_button.rect.x, canvas.rect_button.rect.y)
    actual = canvas.press(mouse_pos)
    assert actual == "rect"


def test_click_menu_button():
    canvas = Canvas()
    mouse_pos = (canvas.menu_button.rect.x, canvas.menu_button.rect.y)
    actual = canvas.press(mouse_pos)
    assert actual == "menu"


def test_open_menu():
    canvas = Canvas()
    command = "menu"
    actual = canvas.do_command(command)
    assert actual == "commands: 'rect', 'menu'"


def test_draw_rect():
    canvas = Canvas()
    command = "rect"
    params = (10, 20, 30, 40)
    actual = canvas.do_command(command, params)
    assert isinstance(actual, pygame.rect.Rect)
    assert actual.x == 10
