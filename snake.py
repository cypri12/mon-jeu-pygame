import pygame
import random

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
vitesse_serpent = 10

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
            nourriturex = random.randint(taille_serpent, largeur_ecran - taille_serpent)
            nourriturey = random.randint(taille_serpent, hauteur_ecran - taille_serpent)
            nourriturex = round(nourriturex / taille_serpent) * taille_serpent
            nourriturey = round(nourriturey / taille_serpent) * taille_serpent
            longueur_serpent += 1

        horloge.tick(vitesse_serpent)

    pygame.quit()
    quit()

jeu()
