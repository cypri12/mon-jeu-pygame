from chunk import Chunk
import opensimplex
import random
import config

class TerrainGenerator:
    def __init__(self):
        self.block_coordinates = []
        self.chunks = []

    def add_block_coordinate(self, label, position):
        self.block_coordinates.append((label, position))

    def generate_terrain(self, size):
        self.noise = opensimplex.OpenSimplex(random.randint(0, 100))
        for x in range(0, size, config.chunk_size):
            for z in range(0, size, config.chunk_size):
                chunk_position = (x * config.tile_size, 0, z * config.tile_size)
                chunk = Chunk(position=chunk_position, noise=self.noise)
                chunk.generate_chunk()
                self.chunks.append(chunk)

    def create_mountain_with_cascade(self, base_position, mountain_height, cascade_height, cascade_width):
        for h in range(mountain_height):
            for i in range(-2, 3):
                for j in range(-2, 3):
                    position = (base_position[0] + i, base_position[1] + h, base_position[2] + j)
                    Voxel(position=position, texture='stone')
                    coordonnees = str(position)
                    self.add_block_coordinate("AJOUT", coordonnees)
                    ecrireDansLeFichier("AJOUT " + coordonnees, config.file_path)

        for i in range(cascade_width):
            position = (base_position[0] + i, base_position[1] + mountain_height, base_position[2])
            voxel = Voxel(position=position, texture='water')
            apply_gravity(voxel)
            coordonnees = str(position)
            self.add_block_coordinate("AJOUT", coordonnees)
            ecrireDansLeFichier("AJOUT " + coordonnees, config.file_path)

        for h in range(cascade_height):
            for i in range(cascade_width):
                position = (base_position[0] + i, base_position[1] + mountain_height - h, base_position[2])
                if any(v.position == position for v in scene.entities if isinstance(v, Voxel)):
                    voxel = Voxel(position=position, texture='water')
                    apply_gravity(voxel)
                    coordonnees = str(position)
                    self.add_block_coordinate("AJOUT", coordonnees)
                    ecrireDansLeFichier("AJOUT " + coordonnees, config.file_path)
