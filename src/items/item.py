import pygame as pg
from entities.sprites import ActionEnum, Sprite_handler

class Item(pg.sprite.Sprite):

    def __init__(self, rect, sprite_groups=[], target_sprite_group=[], scale=1, **kwargs):
        super().__init__(sprite_groups)
        self.sprite_groups = sprite_groups
        self.sprite_groups.add(self)
        self.image_offset = pg.math.Vector2((0, 0))
        self.state = (ActionEnum.IDLE, 'down')
        self.sprite = Sprite_handler()
        self.target_sprite_group = target_sprite_group
        # scale rect
        self.rect = pg.rect.Rect(rect)
        self.rect.width *= scale
        self.rect.height *= scale
        self.is_active = False

    def add_drawing_sprite_group(self, sprite_group):
        sprite_group.add(self)

    def update(self):
        self.image = self.sprite.get_img(self.state)
        img_width, img_height = self.image.get_size()
        # Offset image to center it with the self.rect
        self.image_offset = pg.math.Vector2((img_width / 4, img_height / 4))
        if entity := self.check_collision():
            self.update_targets(entity)

    def check_collision(self):
        return pg.sprite.spritecollideany(self, self.target_sprite_group)

    def update_targets(self, target):
        pass