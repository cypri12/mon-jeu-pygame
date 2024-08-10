from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import opensimplex
import random

app = Ursina()

terrain_size = 20
tile_size = 1
height_range = (1, 10)
min_altitude = 0  # Altitude minimale pour la surface solide
tree_probability = 0.1  # Probabilité qu'un bloc soit un arbre
stone_probability = 0.5  # Probabilité qu'un bloc d'herbe ait de la pierre en dessous
water_level = 3  # Niveau de l'eau
lake_probability = 0.1  # Probabilité de génération d'un lac

# Configuration de la fenêtre
window.borderless = False

# Chargement des textures
def load_texture_safely(file_path):
    try:
        return load_texture(file_path)
    except:
        print(f"Erreur de chargement de la texture: {file_path}")
        return None

grass_texture = load_texture_safely('assets/grass_block.png')
stone_texture = load_texture_safely('assets/stone_block.png')
brick_texture = load_texture_safely('assets/brick_block.png')
dirt_texture = load_texture_safely('assets/dirt_block.png')
water_texture = load_texture_safely('assets/eau.jpg')
sky_texture = load_texture_safely('assets/skybox.png')
bois_texture = load_texture_safely('assets/bois.jfif')
porte_texture = load_texture_safely('assets/terre.jpg')

block_pick = 1

def update():
    global block_pick
    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3
    if held_keys['4']:
        block_pick = 4
    if held_keys['5']:
        block_pick = 5
    if held_keys['6']:
        block_pick = 6
    if held_keys['7']:
        block_pick = 7

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture, has_stone=False):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )
        self.has_stone = has_stone
        if self.position.y < water_level * tile_size:
            self.texture = water_texture

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.add_voxel()
            elif key == 'right mouse down':
                self.remove_voxel()

    def add_voxel(self):
        texture = grass_texture
        if block_pick == 2:
            texture = stone_texture
        elif block_pick == 3:
            texture = brick_texture
        elif block_pick == 4:
            texture = dirt_texture
        elif block_pick == 5:
            texture = bois_texture
        elif block_pick == 6:
            texture = water_texture
        elif block_pick == 7:
            texture = bois_texture

        voxel = Voxel(position=self.position + (0, 1, 0), texture=texture)
        terrain_generator.block_coordinates.append(voxel.position)
        print("Ajout d'un bloc à la position :", voxel.position)

    def remove_voxel(self):
        print("Suppression d'un bloc à la position :", self.position)
        self.enabled = False  # Désactiver le bloc
        destroy(self)  # Supprimer le bloc de la scène
        terrain_generator.block_coordinates.remove(self.position)
        terrain_generator.save_block_coordinates()

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=500,
            double_sided=True
        )

class TreeVoxel(Button):
    def __init__(self, position=(0, 0, 0), texture=bois_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered and key == 'right mouse down':
            self.remove_voxel()

    def remove_voxel(self):
        print("Suppression d'un arbre à la position :", self.position)
        self.enabled = False  # Désactiver le bloc
        destroy(self)  # Supprimer le bloc de la scène
        terrain_generator.block_coordinates.remove(self.position)
        terrain_generator.save_block_coordinates()

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class TerrainGenerator:
    def __init__(self):
        self.block_coordinates = []

    def generate_terrain(self, size):
        self.noise = opensimplex.OpenSimplex(random.randint(0, 100))
        for i in range(size):
            for j in range(size):
                noise_val = self.noise.noise2(i / 10, j / 10)
                height = map_range(noise_val, -1, 1, *height_range)
                for h in range(int(height)):
                    if h >= min_altitude:
                        position = (i * tile_size, h * tile_size, j * tile_size)
                        texture = dirt_texture if random.random() < stone_probability and h != int(height) - 1 else grass_texture
                        voxel = Voxel(position=position, texture=texture)
                        self.block_coordinates.append(position)

                        if random.random() < tree_probability and h == int(height) - 1:
                            TreeVoxel(position=position + (0, 1, 0))

                        if random.random() < lake_probability and h > 4:
                            voxel = Voxel(position=position, texture=water_texture)
                        else:
                            voxel = Voxel(position=position, texture=grass_texture)

                        if position[1] < water_level * tile_size:
                            voxel.texture = water_texture

    def save_block_coordinates(self):
        with open('block_coordinates.txt', 'w') as file:
            for position in self.block_coordinates:
                file.write(f"{position[0]},{position[1]},{position[2]}\n")

    def load_block_coordinates(self):
        with open('block_coordinates.txt', 'r') as file:
            for line in file:
                x, y, z = map(float, line.strip().split(','))
                Voxel(position=(x, y, z), texture=grass_texture)
                self.block_coordinates.append((x, y, z))

player = FirstPersonController()
sky = Sky()
terrain_generator = TerrainGenerator()
terrain_generator.generate_terrain(terrain_size)
terrain_generator.save_block_coordinates()
terrain_generator.load_block_coordinates()

app.run()
