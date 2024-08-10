from PIL import Image

# Charger l'image
image = Image.open("file:///c:/Users/cypri/OneDrive/minecraft2/assets/snake-graphics.png")

# Obtenir la largeur et la hauteur de l'image largeur, hauteur = image.size

# Définir la taille des carrés
taille_cote = 50

# Parcourir l'image en créant un carré de 50x50 à chaque itération for y in range(0, hauteur, taille_cote):
for x in range(0, largeur, taille_cote):
    # Coordonnées du coin supérieur gauche du carré
    gauche = x
    haut = y
    # Coordonnées du coin inférieur droit du carré
    droite = x + taille_cote
    bas = y + taille_cote
    # Découper le carré de l'image
    carre = image.crop((gauche, haut, droite, bas))
    # Sauvegarder le carré en tant qu'image séparée
    nom_fichier = f"carre_{x}_{y}.png"  # Nom de fichier unique basé sur les coordonnées
    carre.save(nom_fichier)

