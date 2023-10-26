import pygame
from main import Object1, Object2, has_collided


def test_obj1_ollides_many_objects_when_many_objects_in_group():
    groupA = pygame.sprite.Group()
    groupB = pygame.sprite.Group()
    object1 = Object1(groupA)
    object2 = Object2(groupB)
    object3 = Object2(groupB)
    object4 = Object2(groupB)

    rect1 = pygame.rect.Rect(0, 0, 1, 1)
    rect2 = pygame.rect.Rect(9, 9, 1, 1)
    object1.rect = rect1
    object2.rect = rect2
    object3.rect = rect1
    object4.rect = rect1

    assert has_collided(object1, groupB, dokill=1) is True


def test_obj1_ollides_obj2_when_many_objects_in_group():
    groupA = pygame.sprite.Group()
    groupB = pygame.sprite.Group()
    object1 = Object1(groupA)
    object2 = Object2(groupB)
    object3 = Object2(groupB)

    rect1 = pygame.rect.Rect(0, 0, 1, 1)
    rect2 = pygame.rect.Rect(9, 9, 1, 1)
    object1.rect = rect1
    object2.rect = rect2
    object3.rect = rect1

    assert has_collided(object1, groupB, dokill=1) is True


def test_obj1_not_collides_obj2_when_no_intersection():
    group1 = pygame.sprite.Group()
    group2 = pygame.sprite.Group()
    object1 = Object1(group1)
    object2 = Object2(group2)

    rect1 = pygame.rect.Rect(0, 0, 1, 1)
    rect2 = pygame.rect.Rect(9, 9, 1, 1)
    object1.rect = rect1
    object2.rect = rect2

    assert has_collided(object1, group2, dokill=1) is False


def test_obj1_collides_obj2_when_has_the_same_rect():
    group1 = pygame.sprite.Group()
    group2 = pygame.sprite.Group()
    object1 = Object1(group1)
    object2 = Object2(group2)

    rect = pygame.rect.Rect(0, 0, 1, 1)
    object1.rect = rect
    object2.rect = rect

    assert has_collided(object1, group2, dokill=1) is True


def test_obj1_collides_obj1():
    group1 = pygame.sprite.Group()
    object1 = Object1(group1)
    rect = pygame.rect.Rect(0, 0, 1, 1)
    object1.rect = rect

    assert has_collided(object1, group1, dokill=1) is True
