from ursina import Ursina
from ursina.prefabs.first_person_controller import FirstPersonController
from voxel import Voxel, TreeVoxel
from terrain import TerrainGenerator
from utils import apply_gravity, ecrireDansLeFichier
import config

app = Ursina()

def update():
    global block_pick
    for i in range(1, 8):
        if held_keys[str(i)]:
            block_pick = i

    for voxel in scene.entities:
        if isinstance(voxel, Voxel) and voxel.texture == config.textures['water']:
            apply_gravity(voxel)

player = FirstPersonController()
sky = Sky()
terrain_generator = TerrainGenerator()
terrain_generator.generate_terrain(config.terrain_size)
terrain_generator.create_mountain_with_cascade(base_position=(config.terrain_size // 2, 0, config.terrain_size // 2), mountain_height=5, cascade_height=8, cascade_width=2)

def fermer_application():
    with open(config.map_file_path, 'w') as map_file:
        for label, coordonnees in terrain_generator.block_coordinates:
            map_file.write(label + " " + coordonnees + '\n')
    application.quit()

app.on_window_close = fermer_application
app.run()
