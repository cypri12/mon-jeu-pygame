import os
import pygame
import socket
import threading
import pytmx
import pyscroll
import time
import math
import random

# Initialiser Pygame
pygame.init()

# Obtenir la résolution de l'écran
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Charger les images des armes avec les chemins corrects
image_path1 = "C:\\Users\\cypri\\OneDrive\\arme 1 jeu multijoueur.jpg"
image_path2 = "C:\\Users\\cypri\\OneDrive\\arme 2 jeu multijoueur.jpg"
image_path3 = "C:\\Users\\cypri\\OneDrive\\arme 3 jeu multijoueur.jpg"

arme_1 = pygame.image.load(image_path1)
arme_2 = pygame.image.load(image_path2)
arme_3 = pygame.image.load(image_path3)

# Redimensionner les images (optionnel)
new_width = 200
new_height = 200
arme_1 = pygame.transform.scale(arme_1, (new_width, new_height))
arme_2 = pygame.transform.scale(arme_2, (new_width, new_height))
arme_3 = pygame.transform.scale(arme_3, (new_width, new_height))

# Charger les images des projectiles
proj_image1 = pygame.image.load("C:\\Users\\cypri\\OneDrive\\Images\\Screenshots\\Capture d'écran 2024-07-29 124703.png")
proj_image2 = pygame.image.load("C:\\Users\\cypri\\OneDrive\\Images\\Screenshots\\Capture d'écran 2024-07-29 141514.png")
proj_image3 = pygame.image.load("C:\\Users\\cypri\\OneDrive\\Images\\Screenshots\\Capture d'écran 2024-07-29 141532.png")

# Rendre le fond noir transparent pour les images des projectiles
proj_image1.set_colorkey((0, 0, 0))
proj_image2.set_colorkey((0, 0, 0))
proj_image3.set_colorkey((0, 0, 0))

# Charger l'image de l'ennemi
enemy_image_path = "C:\\Users\\cypri\\OneDrive\\Desktop\\boss enemis.png"
enemy_image = pygame.image.load(enemy_image_path)
enemy_image = pygame.transform.scale(enemy_image, (32, 32))  # Assurez-vous que la taille correspond à vos besoins

# Configuration de la fenêtre de jeu pour s'adapter à la taille de l'écran
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("2D Multiplayer Game")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Variables de jeu
health = 100
weapons = ["pistol", "shotgun", "rifle"]
current_weapon = 0

# Limite de munitions
ammo_limits = [50, 20, 20]

# Réseau
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('localhost', 5555))
except socket.error as e:
    print(f"Erreur de connexion: {e}")
    exit()

def handle_server():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except socket.error as e:
            print(f"Erreur de réception: {e}")
            client.close()
            break

thread = threading.Thread(target=handle_server)
thread.start()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image, walls):
        super().__init__()
        self.velocity = 3
        self.angle = angle
        self.walls = walls
        self.original_image = image
        self.image = self.original_image.copy()
        self.image = pygame.transform.rotate(self.image, -math.degrees(angle))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = math.cos(angle) * self.velocity
        self.dy = math.sin(angle) * self.velocity

        # Redéfinir la couleur de transparence après la rotation
        self.image.set_colorkey((0, 0, 0))

    def update(self):
        # Déplacer le projectile en fonction de son angle
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Supprimer le projectile s'il sort de l'écran ou s'il entre en collision avec un mur
        if (self.rect.x < 0 or self.rect.x > screen_width or
            self.rect.y < 0 or self.rect.y > screen_height):
            self.kill()
        else:
            for wall in self.walls:
                if self.rect.colliderect(wall):
                    self.kill()
                    break

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("C:\\Users\\cypri\\OneDrive\\Player.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.all_projectiles = pygame.sprite.Group()
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.current_weapon = 0
        self.weapon_images = [arme_1, arme_2, arme_3]
        self.projectile_images = [proj_image1, proj_image3, proj_image2]
        self.last_shot_time = 0
        self.shot_interval = 100  # Intervalle de tir pour la mitraillette (en millisecondes)
        self.shooting = False  # Variable pour gérer l'état de tir continu
        self.ammo_counts = ammo_limits.copy()  # Initialiser les munitions avec les limites
        self.angle = 0

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.update_angle()
        if self.shooting and self.current_weapon == 0:
            self.launch_projectile()

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name): 
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def update_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = math.atan2(rel_y, rel_x)

    def launch_projectile(self):
        if self.ammo_counts[self.current_weapon] == 0:
            return  # Ne pas tirer si pas de munitions

        current_time = pygame.time.get_ticks()
        if self.current_weapon == 0 and current_time - self.last_shot_time < self.shot_interval:
            return
        self.last_shot_time = current_time

        projectile_image = self.projectile_images[self.current_weapon]
        projectile = Projectile(self.rect.centerx, self.rect.centery, self.angle, projectile_image, walls)
        self.all_projectiles.add(projectile)
        self.ammo_counts[self.current_weapon] -= 1  # Décrémenter les munitions

    def move_right(self):
        self.save_location()
        self.position[0] += 1  # Adjust speed if necessary
        self.check_collision('horizontal')

    def move_left(self):
        self.save_location()
        self.position[0] -= 1  # Adjust speed if necessary
        self.check_collision('horizontal')

    def move_up(self):
        self.save_location()
        self.position[1] -= 1  # Adjust speed if necessary
        self.check_collision('vertical')

    def move_down(self):
        self.save_location()
        self.position[1] += 1  # Adjust speed if necessary
        self.check_collision('vertical')

    def check_collision(self, direction):
        self.rect.topleft = self.position
        collisions = [wall for wall in walls if self.rect.colliderect(wall)]
        if collisions:
            if direction == 'horizontal':
                self.position[0] = self.old_position[0]
            else:
                self.position[1] = self.old_position[1]
            self.rect.topleft = self.position

    def change_weapon(self, weapon_index):
        self.current_weapon = weapon_index

    def reload_weapon(self):
        self.ammo_counts[self.current_weapon] = ammo_limits[self.current_weapon]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100

    def update(self):
        if self.health <= 0:
            self.kill()
            spawn_enemy()  # Spawn a new enemy when one dies

def spawn_enemy():
    while True:
        # Générer une position éloignée du joueur
        offset_x = random.randint(-500, 500)  # Augmentez la plage pour plus de distance
        offset_y = random.randint(-500, 500)  # Augmentez la plage pour plus de distance
        x = player.position[0] + offset_x
        y = player.position[1] + offset_y

        # Assurez-vous que l'ennemi n'apparaît pas en dehors de l'écran ou dans un mur
        if 0 <= x <= screen_width - 32 and 0 <= y <= screen_height - 32:
            enemy_rect = pygame.Rect(x, y, 32, 32)
            if not any(wall.colliderect(enemy_rect) for wall in walls):
                enemy = Enemy(x, y)
                enemies.add(enemy)
                group.add(enemy)
                break

def draw_health_bar(screen, x, y, health):
    BAR_WIDTH = 100
    BAR_HEIGHT = 10
    fill = (health / 100) * BAR_WIDTH
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def draw_selected_weapon_border(screen, x, y, width, height):
    pygame.draw.rect(screen, RED, (x, y, width, height), 3)

def draw_ammo_bars(screen, ammo_counts):
    BAR_WIDTH = 100  # Largeur plus grande des barres
    BAR_HEIGHT = 10  # Hauteur plus grande des barres
    BAR_SPACING = 20  # Espacement entre les barres

    for i, ammo in enumerate(ammo_counts):
        if i == 0:                                                                                                                                                                                    
            max_ammo = ammo_limits[0]
        else:
            max_ammo = ammo_limits[1]

        fill = (ammo / max_ammo) * BAR_WIDTH
        # Positionner les barres au-dessus de chaque arme
        x = screen_width - (i + 1) * (new_width + 2 * BAR_SPACING) + new_width // 2 - BAR_WIDTH // 2
        y = screen_height - new_height - BAR_HEIGHT - 10  # Au-dessus de chaque arme
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)

tmx_data = pytmx.util_pygame.load_pygame("C:\\Users\\cypri\\OneDrive\\Desktop\\code\\carte.tmx")
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (screen_width, screen_height))

player = Player(50, 50)

walls = []
for obj in tmx_data.objects:
    if obj.type == "collision":
        walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
group.add(player)

# Créer des ennemis avec positionnement aléatoire
enemies = pygame.sprite.Group()
for _ in range(5):  # Réduisez ce nombre pour avoir moins d'ennemis
    spawn_enemy()

# Boucle principale du jeu
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.change_weapon(0)
            if event.key == pygame.K_2:
                player.change_weapon(1)
            if event.key == pygame.K_3:
                player.change_weapon(2)
            if event.key == pygame.K_r:
                time.sleep(0.75)
                player.reload_weapon()  # Recharger l'arme actuelle
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shooting = True
            player.launch_projectile()  # Pour tirer immédiatement avec les armes 2 et 3
        if event.type == pygame.MOUSEBUTTONUP:
            player.shooting = False
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (screen_width, screen_height))
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
            group.add(player)
            group.add(enemies)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Utiliser 'A' pour aller à gauche
        player.move_left()
        player.change_animation('left')
    if keys[pygame.K_d]:  # Utiliser 'D' pour aller à droite
        player.move_right()
        player.change_animation('right')
    if keys[pygame.K_w]:  # Utiliser 'W' pour aller en haut
        player.move_up()
        player.change_animation('up')
    if keys[pygame.K_s]:  # Utiliser 'S' pour aller en bas
        player.move_down()
        player.change_animation('down')

    # Mise à jour de la position de la caméra
    group.center(player.rect.center)  # Centrer la caméra sur le joueur
    player.save_location()
    screen.fill(WHITE)  # Effacer l'écran
    group.draw(screen)
    player.all_projectiles.draw(screen)  # Dessiner les projectiles
    group.update()
    player.all_projectiles.update()  # Mettre à jour les projectiles

    # Vérifier les collisions entre les projectiles et les ennemis
    for projectile in player.all_projectiles:
        for enemy in enemies:
            if projectile.rect.colliderect(enemy.rect):
                enemy.health -= 5  # Réduire la santé de l'ennemi
                projectile.kill()

    # Dessiner les images des armes en bas à droite
    arme_x1 = screen_width - new_width
    arme_y1 = screen_height - new_height
    arme_x2 = arme_x1 - new_width - 10  # Positionner la deuxième arme à côté de la première (ajouter un espace de 10 pixels entre les deux)
    arme_y2 = screen_height - new_height
    arme_x3 = arme_x2 - new_width - 10  # Positionner la troisième arme à côté de la deuxième (ajouter un espace de 10 pixels entre les deux)
    arme_y3 = screen_height - new_height

    screen.blit(arme_1, (arme_x1, arme_y1))
    screen.blit(arme_2, (arme_x2, arme_y2))
    screen.blit(arme_3, (arme_x3, arme_y3))

    # Dessiner le cadre autour de l'arme sélectionnée
    if player.current_weapon == 0:
        draw_selected_weapon_border(screen, arme_x1, arme_y1, new_width, new_height)
    elif player.current_weapon == 1:
        draw_selected_weapon_border(screen, arme_x2, arme_y2, new_width, new_height)
    elif player.current_weapon == 2:
        draw_selected_weapon_border(screen, arme_x3, arme_y3, new_width, new_height)

    draw_health_bar(screen, 10, 10, health)
    draw_ammo_bars(screen, player.ammo_counts)  # Dessiner les barres de munitions

    pygame.display.flip()

    # Envoyer la position et l'arme actuelle au serveur
    try:
        client.send(f"{player.position[0]},{player.position[1]},{weapons[player.current_weapon]}".encode('utf-8'))
    except socket.error as e:
        print(f"Erreur d'envoi de données: {e}")
        run = False

pygame.quit()
