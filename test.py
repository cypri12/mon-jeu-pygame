from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import opensimplex
import random
import time

app = Ursina()

# Configuration du terrain
chunk_size = 5
tile_size = 1
height_range = (1, 10)
water_level = 3
tree_probability = 0.05
lake_probability = 0.05
stone_probability = 0.3
file_path = 'coordonée.txt'
map_file_path = 'map_coordonée.txt'

textures = {
    'grass': load_texture('assets/grass_block.png'),
    'stone': load_texture('assets/stone_block.png'),
    'brick': load_texture('assets/brick_block.png'),
    'dirt': load_texture('assets/dirt_block.png'),
    'water': load_texture('assets/eau.jpg'),
    'sky': load_texture('assets/skybox.png'),
    'wood': load_texture('assets/bois.jfif'),
}

block_pick = 1
window.borderless = False

def apply_gravity(voxel):
    below_position = voxel.position + Vec3(0, -1, 0)
    if below_position.y >= 0 and not any(v.position == below_position for v in scene.entities if isinstance(v, Voxel)):
        voxel.position = below_position

def update():
    global block_pick
    for i in range(1, 8):
        if held_keys[str(i)]:
            block_pick = i

    # Appliquer la gravité uniquement sur les voxels d'eau
    for voxel in [v for v in scene.entities if isinstance(v, Voxel) and v.texture == textures['water']]:
        apply_gravity(voxel)

    # Mise à jour des chunks autour du joueur
    terrain_generator.update_chunks(player.position)

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass', has_stone=False):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=textures[texture],
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )
        self.has_stone = has_stone
        if self.position.y < water_level * tile_size:
            self.texture = textures['water']

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.add_voxel(block_pick)
            if key == 'right mouse down':
                self.remove_voxel()

    def add_voxel(self, block_type):
        block_types = ['grass', 'stone', 'brick', 'dirt', 'wood', 'water']
        texture = block_types[block_type - 1] if block_type <= 5 else 'water'
        voxel = Voxel(position=self.position + (0, 1, 0), texture=texture)
        if texture == 'water':
            apply_gravity(voxel)
        coordonnees = str(self.position + voxel.position)
        terrain_generator.add_block_change("AJOUT", coordonnees)

    def remove_voxel(self):
        coordonnees = str(self.position)
        terrain_generator.add_block_change("DETRUIT", coordonnees)
        destroy(self)

class TreeVoxel(Voxel):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position, texture='wood')

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=textures['sky'],
            scale=500,
            double_sided=True
        )

class Chunk(Entity):
    def __init__(self, position=(0, 0, 0), noise=None):
        super().__init__(parent=scene, position=position)
        self.noise = noise
        self.voxels = []
        self.generate_chunk()

    def generate_chunk(self):
        for i in range(chunk_size):
            for j in range(chunk_size):
                noise_val = self.noise.noise2(i / 10, j / 10)
                height = map_range(noise_val, -1, 1, *height_range)
                for h in range(int(height)):
                    if h >= 0:
                        position = (self.position[0] + i * tile_size, self.position[1] + h * tile_size, self.position[2] + j * tile_size)
                        texture = 'grass'
                        if random.random() < stone_probability and h != int(height) - 1:
                            voxel = Voxel(position=position, texture='stone', has_stone=True)
                        else:
                            voxel = Voxel(position=position, texture=texture, has_stone=False)

                        if random.random() < tree_probability:
                            TreeVoxel(position=position)

                        if h > 4 and random.random() < lake_probability:
                            voxel = Voxel(position=position, texture='water', has_stone=False)
                            apply_gravity(voxel)

                        if position[1] < water_level * tile_size:
                            voxel.texture = textures['water']
                            apply_gravity(voxel)

                        coordonnees = str(position)
                        terrain_generator.add_block_change("AJOUT", coordonnees)
                        self.voxels.append(voxel)

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class TerrainGenerator:
    def __init__(self):
        self.block_changes = []
        self.chunks = []
        self.chunk_size = chunk_size * tile_size
        self.loaded_chunks = set()
        self.chunk_range = 2  # Rayon de chunks autour du joueur
        self.last_save_time = time.time()  # Initialiser le temps de dernière sauvegarde

    def add_block_change(self, label, position):
        self.block_changes.append((label, position))

    def save_changes(self):
        with open(file_path, 'a') as file:
            for label, coordonnees in self.block_changes:
                file.write(f"{label} {coordonnees}\n")
        self.block_changes = []  # Réinitialiser après enregistrement

    def generate_chunk(self, position):
        noise = opensimplex.OpenSimplex(random.randint(0, 100))
        chunk = Chunk(position=position, noise=noise)
        self.chunks.append(chunk)

    def update_chunks(self, player_position):
        chunk_x = int(player_position.x / self.chunk_size) * self.chunk_size
        chunk_z = int(player_position.z / self.chunk_size) * self.chunk_size
        chunk_positions = {(chunk_x + dx * self.chunk_size, 0, chunk_z + dz * self.chunk_size)
                           for dx in range(-self.chunk_range, self.chunk_range + 1)
                           for dz in range(-self.chunk_range, self.chunk_range + 1)}

        # Charger les chunks nécessaires
        new_chunks = chunk_positions - self.loaded_chunks
        for pos in new_chunks:
            self.generate_chunk(pos)

        # Décharger les chunks éloignés
        self.loaded_chunks = {pos for pos in self.loaded_chunks if pos in chunk_positions}

        # Sauvegarder les changements toutes les quelques secondes
        if time.time() - self.last_save_time > 10:
            self.save_changes()
            self.last_save_time = time.time()

player = FirstPersonController()
sky = Sky()
terrain_generator = TerrainGenerator()

# Génération initiale des chunks autour du joueur
terrain_generator.update_chunks(player.position)

def fermer_application():
    terrain_generator.save_changes()  # Sauvegarde finale avant fermeture
    with open(map_file_path, 'w') as map_file:
        for label, coordonnees in terrain_generator.block_changes:
            map_file.write(f"{label} {coordonnees}\n")
    application.quit()

app.on_window_close = fermer_application
app.run()
