from ursina import Button, color, random
import config
from utils import apply_gravity, ecrireDansLeFichier

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass', has_stone=False):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=config.textures[texture],
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )
        self.has_stone = has_stone
        if self.position.y < config.water_level * config.tile_size:
            self.texture = config.textures['water']

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.add_voxel(config.block_pick)
            if key == 'right mouse down':
                self.remove_voxel()

    def add_voxel(self, block_type):
        block_types = ['grass', 'stone', 'brick', 'dirt', 'wood', 'water']
        texture = block_types[block_type - 1] if block_type <= 5 else 'water'
        voxel = Voxel(position=self.position + (0, 1, 0), texture=texture)
        if texture == 'water':
            apply_gravity(voxel)
        coordonnees = str(self.position + voxel.position)
        terrain_generator.add_block_coordinate("AJOUT", coordonnees)
        ecrireDansLeFichier("AJOUT " + coordonnees, config.file_path)

    def remove_voxel(self):
        coordonnees = str(self.position)
        terrain_generator.add_block_coordinate("DETRUIT", coordonnees)
        ecrireDansLeFichier("DETRUIT " + coordonnees, config.file_path)
        destroy(self)

class TreeVoxel(Voxel):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position, texture='wood')
