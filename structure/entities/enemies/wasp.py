from entities.enemy import Enemy


class Wasp(Enemy):

    def __init__(self, collision_sprites, sprite_path, entity_rect, sprite_scale=1):
        super.__init__(collision_sprites, sprite_path, entity_rect, sprite_scale)
        self.state = 'idle'
        self.bahavior = MeleeBehaviour()