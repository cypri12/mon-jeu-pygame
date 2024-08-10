import pygame
import random
from tkinter import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import opensimplex
import random

def Snake():


    pygame.init()

    # Couleurs
    blanc = (255, 255, 255)
    rouge = (213, 50, 80)
    bleu = (50, 153, 213)
    gris_clair = (200, 200, 200)

    # Dimensions de l'écran
    largeur_ecran = 900
    hauteur_ecran = 800

    # Paramètres du serpent
    taille_serpent = 20  # Taille de chaque segment du serpent
    vitesse_serpent = 20

    # Initialisation de l'écran
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption('Snake Game')

    horloge = pygame.time.Clock()

    # Charger les images
    img_snake = pygame.image.load('assets/snake-graphics.png')
    img_segment = pygame.Surface((taille_serpent, taille_serpent))  # Créer une surface pour le segment du serpent
    img_segment.fill((0, 255, 0))  # Remplir la surface de couleur verte
    img_pomme = img_snake.subsurface((0, 200, 80, 55)).convert_alpha()  # Découper la pomme
    taille_pomme = img_pomme.get_rect().size  # Obtenir la taille de la pomme

    # Font pour afficher le score
    font_score = pygame.font.SysFont(None, 30)

    # Fonction pour afficher un message à l'écran
    def message(msg, couleur):
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(msg, True, couleur)
        ecran.blit(mesg, [largeur_ecran / 6, hauteur_ecran / 3])

    # Fonction de dessin de grille
    def draw_grid():
        for x in range(0, largeur_ecran, taille_serpent):
            pygame.draw.line(ecran, gris_clair, (x, 0), (x, hauteur_ecran))
        for y in range(0, hauteur_ecran, taille_serpent):
            pygame.draw.line(ecran, gris_clair, (0, y), (largeur_ecran, y))

    # Fonction pour vérifier la collision entre la pomme et le serpent
    def check_collision_pomme(x1, y1, nourriturex, nourriturey, taille_pomme):
        if (nourriturex <= x1 < nourriturex + taille_pomme[0]) and (nourriturey <= y1 < nourriturey + taille_pomme[1]):
            return True
        return False

    # Fonction principale du jeu
    def jeu():
        game_over = False
        game_close = False

        x1 = largeur_ecran / 2
        y1 = hauteur_ecran / 2

        x1_changement = 0
        y1_changement = 0
        direction = 'RIGHT'

        liste_serpent = []
        longueur_serpent = 1

        nourriturex = random.randint(taille_serpent, largeur_ecran - taille_serpent)
        nourriturey = random.randint(taille_serpent, hauteur_ecran - taille_serpent)
        nourriturex = round(nourriturex / taille_serpent) * taille_serpent
        nourriturey = round(nourriturey / taille_serpent) * taille_serpent

        score = 0

        while not game_over:

            while game_close:
                ecran.fill(blanc)
                message(f"Vous avez perdu ! Score: {score}. Appuyez sur Q-Quitter ou C-Continuer", rouge)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            jeu()
                            return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        x1_changement = -taille_serpent
                        y1_changement = 0
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        x1_changement = taille_serpent
                        y1_changement = 0
                        direction = 'RIGHT'
                    elif event.key == pygame.K_UP and direction != 'DOWN':
                        y1_changement = -taille_serpent
                        x1_changement = 0
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        y1_changement = taille_serpent
                        x1_changement = 0
                        direction = 'DOWN'

            if x1 >= largeur_ecran or x1 < 0 or y1 >= hauteur_ecran or y1 < 0:
                game_close = True
            x1 += x1_changement
            y1 += y1_changement
            ecran.fill(bleu)

            draw_grid()

            ecran.blit(img_pomme, (nourriturex, nourriturey))
            tete_serpent = [x1, y1]
            liste_serpent.append(tete_serpent)
            if len(liste_serpent) > longueur_serpent:
                del liste_serpent[0]

            for bloc in liste_serpent[:-1]:
                if bloc == tete_serpent:
                    game_close = True

            for x, y in liste_serpent:
                ecran.blit(img_segment, (x, y))

            # Affichage du score
            score_text = font_score.render(f"Score: {score}", True, blanc)
            ecran.blit(score_text, (10, 10))

            pygame.display.update()

            if check_collision_pomme(x1, y1, nourriturex, nourriturey, taille_pomme):
                score += 10
                nourriturex = random.randint(taille_serpent, 700 - taille_serpent)
                nourriturey = random.randint(taille_serpent, 700 - taille_serpent)
                nourriturex = round(nourriturex / taille_serpent) * taille_serpent
                nourriturey = round(nourriturey / taille_serpent) * taille_serpent
                longueur_serpent += 1

            horloge.tick(vitesse_serpent)

        pygame.quit()
        quit()

    jeu()


def launch_minecraft():
    app = Ursina()

    terrain_size = 20  # Réduction de la taille du terrain
    tile_size = 1
    height_range = (1, 10)
    min_altitude = 0
    tree_probability = 0.1
    stone_probability = 0.5
    window.borderless = False

    grass_texture = load_texture('assets/grass_block.png')
    stone_texture = load_texture('assets/stone_block.png')
    brick_texture = load_texture('assets/brick_block.png')
    dirt_texture = load_texture('assets/dirt_block.png')
    water_texture = load_texture('assets/eau.jpg')
    sky_texture = load_texture('assets/skybox.png')
    bois_texture = load_texture('assets/bois.jfif')
    porte_texture = load_texture('assets/terre.jpg')
    block_pick = 1
    sol1 = dirt_texture
    water_level = 3
    lake_probability = 0.1
    terrain = terrain_size
    file_path = 'coordonée.txt'
    map_file_path = 'map_coordonée.txt'  # Le fichier pour enregistrer toutes les coordonnées de la carte

    map_coordinates = []  # Liste pour stocker toutes les coordonnées de la carte

    def apply_gravity(voxel):
        below_position = voxel.position + Vec3(0, -1, 0)
        if below_position.y >= 0 and not any(v.position == below_position for v in scene.entities if isinstance(v, Voxel)):
            voxel.position = below_position
            print(f"Eau tombée à la position: {voxel.position}")

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

        # Appliquer la gravité à chaque bloc d'eau
        for voxel in scene.entities:
            if isinstance(voxel, Voxel) and voxel.texture == water_texture:
                apply_gravity(voxel) 


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
                    if block_pick == 1:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=grass_texture)
                    elif block_pick == 2:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=stone_texture)
                    elif block_pick == 3:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=brick_texture)
                    elif block_pick == 4:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=dirt_texture)
                    elif block_pick == 5:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=bois_texture)
                    elif block_pick == 6:
                        voxel = Voxel(position=self.position + (0, 1, 0), texture=water_texture)
                        apply_gravity(voxel)  # Appliquer la gravité au nouveau bloc d'eau
                    elif block_pick == 7:
                        voxel = TreeVoxel(position=self.position + (0, 1, 0), texture=bois_texture)

                    print("AJOUT : Ajout d'un bloc à la position :", voxel.position)

                    coordonnees = str(self.position + voxel.position)
                    terrain_generator.add_block_coordinate("AJOUT", coordonnees)  # Ajouter les coordonnées des blocs ajoutés
                    ecrireDansLeFichier("AJOUT " + coordonnees, file_path)  # Ajouter les coordonnées au fichier avec l'étiquette "AJOUT"

                if key == 'right mouse down':
                    print("DETRUIT : Suppression d'un bloc à la position :", self.position)
                    coordonnees = str(self.position)
                    terrain_generator.add_block_coordinate("DETRUIT", coordonnees)  # Ajouter les coordonnées des blocs détruits
                    ecrireDansLeFichier("DETRUIT " + coordonnees, file_path)  # Ajouter les coordonnées au fichier avec l'étiquette "DETRUIT"
                    destroy(self)


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
                model=bois_texture,
                origin_y=0.5,
                texture=texture,
                color=color.color(0, 0, random.uniform(0.9, 1)),
                scale=0.5
            )

        def input(self, key):
            if self.hovered:
                if key == 'right mouse down':
                    print("DETRUIT : Suppression d'un arbre à la position :", self.position)
                    coordonnees = str(self.position)
                    terrain_generator.add_block_coordinate("DETRUIT", coordonnees)  # Ajouter les coordonnées des blocs détruits
                    ecrireDansLeFichier("DETRUIT " + coordonnees, file_path)  # Ajouter les coordonnées au fichier avec l'étiquette "DETRUIT"
                    destroy(self)


    def map_range(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def ecrireDansLeFichier(coordonnees, file_path):
        with open(file_path, 'a') as File:  # Utiliser 'a' pour ajouter au fichier plutôt que de le remplacer
            File.write(coordonnees + '\n')  # Ajouter un retour à la ligne pour chaque coordonnée


    class TerrainGenerator:
        def __init__(self):
            self.block_coordinates = []

        def add_block_coordinate(self, label, position):
            self.block_coordinates.append((label, position))

        def generate_terrain(self, size):
            self.noise = opensimplex.OpenSimplex(random.randint(0, 100))

            for i in range(terrain):
                for j in range(terrain):
                    noise_val = self.noise.noise2(i / 10, j / 10)
                    height = map_range(noise_val, -1, 1, *height_range)
                    for h in range(int(height)):
                        if h >= min_altitude:
                            full = 0
                            position = (i * tile_size, h * tile_size, j * tile_size)
                            texture = grass_texture
                            if random.random() < stone_probability and h != int(height) - 1:
                                voxel = Voxel(position=position, texture=stone_texture, has_stone=True)
                                full = 1
                            else:
                                voxel = Voxel(position=position, texture=texture, has_stone=False)
                                full = 1

                            if random.random() < tree_probability:
                                TreeVoxel(position=position, texture=bois_texture)

                            if full == 0 and h > 4:
                                if random.random() < lake_probability:
                                    voxel = Voxel(position=position, texture=water_texture, has_stone=False)
                                    apply_gravity(voxel)  # Appliquer la gravité à l'eau générée
                                else:
                                    voxel = Voxel(position=position, texture=grass_texture, has_stone=False)

                            if position[1] < water_level * tile_size:
                                voxel.texture = water_texture
                                apply_gravity(voxel)  # Appliquer la gravité à l'eau générée

                            coordonnees = str(position)
                            terrain_generator.add_block_coordinate("AJOUT", coordonnees)  

            
            cascade_height = 8
            cascade_width = 2
            for i in range(cascade_width):
                for h in range(cascade_height):
                    position = (terrain_size // 2 + i, h, terrain_size // 2)
                    voxel = Voxel(position=position, texture=water_texture)
                    apply_gravity(voxel)
                    coordonnees = str(position)
                    terrain_generator.add_block_coordinate("AJOUT", coordonnees)
                    ecrireDansLeFichier("AJOUT " + coordonnees, file_path)

        def print_map_coordinates(self, size):
            for i in range(terrain):
                for j in range(terrain):
                    for h in range(int(height_range[1])):
                        position = (i * tile_size, h * tile_size, j * tile_size)
                        coordonnees = str(position)
                        terrain_generator.add_block_coordinate("AJOUT", coordonnees)  


    player = FirstPersonController()
    sky = Sky()

    terrain_generator = TerrainGenerator()
    terrain_generator.generate_terrain(terrain_size)
    terrain_generator.print_map_coordinates(terrain_size)


    def fermer_application():
        # Écrire toutes les coordonnées de la carte dans le fichier map_file_path
        with open(map_file_path, 'w') as map_file:
            for label, coordonnees in terrain_generator.block_coordinates:
                map_file.write(label + " " + coordonnees + '\n')

        print("Fermeture de l'application...")
        application.quit()

    # Fermer l'application proprement lorsqu'elle est fermée
    app.on_window_close = fermer_application

    app.run()

root = Tk()
root.title("Platforme de jeux")
root.geometry("500x500")
root.minsize(200, 200)
root.config(background='white')

def mincraft():
    launch_minecraft()

def snake():
    Snake()

menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
# Crée une fenêtre pour Minecraft
file_menu.add_command(label="Minecraft", command=mincraft)
file_menu.add_command(label="snake", command=Snake)   
file_menu.add_command(label="Evaluation")
menu_bar.add_cascade(label="Menu", menu=file_menu)
root.config(menu=menu_bar)

root.mainloop()
