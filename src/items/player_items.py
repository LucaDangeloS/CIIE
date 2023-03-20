from entities.player import Player
from items.item import Item
import pygame as pg

class Heart(Item):
    def __init__(self, pos, sprite_groups=..., target_sprite_group=..., scale=1):
        sprite_path = '../sprites/items/heart'
        # offset position to center it
        pos = (pos[0] - 8, pos[1] - 8)
        item_rect = pg.rect.Rect(pos, (16, 16))
        super().__init__(item_rect, sprite_groups, target_sprite_group, scale=scale)
        self.sprite.load_regular_sprites(sprite_path, scale=scale)
        self.image = self.sprite.get_img(self.state)

    def update_targets(self, target: Player):
        target.heal(1)
        self.kill()