from ursina import Entity
from voxel import Voxel
from utils import map_range, apply_gravity
import config

class Chunk(Entity):
    def __init__(self, position=(0, 0, 0), noise=None):
        super().__init__(
            parent=scene,
            position=position
        )
        self.noise = noise
        self.voxels = []

    def generate_chunk(self):
        for i in range(config.chunk_size):
            for j in range(config.chunk_size):
                noise_val = self.noise.noise2(i / 10, j / 10)
                height = map_range(noise_val, -1, 1, *config.height_range)
                for h in range(int(height)):
                    if h >= 0:
                        position = (self.position[0] + i * config.tile_size, self.position[1] + h * config.tile_size, self.position[2] + j * config.tile_size)
                        texture = 'grass'
                        if random.random() < config.stone_probability and h != int(height) - 1:
                            voxel = Voxel(position=position, texture='stone', has_stone=True)
                        else:
                            voxel = Voxel(position=position, texture=texture, has_stone=False)

                        if random.random() < config.tree_probability:
                            TreeVoxel(position=position)

                        if h > 4 and random.random() < config.lake_probability:
                            voxel = Voxel(position=position, texture='water', has_stone=False)
                            apply_gravity(voxel)
                        else:
                            voxel = Voxel(position=position, texture='grass', has_stone=False)

                        if position[1] < config.water_level * config.tile_size:
                            voxel.texture = config.textures['water']
                            apply_gravity(voxel)

                        coordonnees = str(position)
                        terrain_generator.add_block_coordinate("AJOUT", coordonnees)
                        self.voxels.append(voxel)
