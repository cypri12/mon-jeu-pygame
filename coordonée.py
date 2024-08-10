from main import *

class SaveButton(Button):
    def __init__(self):
        super().__init__(
            parent=scene,
            position=window.top_right + Vec2(-0.1, -0.1),  # Position du bouton
            scale=0.075,
            text='9',  # Numéro du bouton
            on_click=self.save_coordinates
        )
        self.coordinates = []

    def save_coordinates(self):
        self.coordinates = []
        print("Enregistrement des coordonnées de tous les blocs :")
        for entity in scene.entities:
            if isinstance(entity, Voxel) or isinstance(entity, TreeVoxel):
                self.coordinates.append(entity.position)
                print("Bloc à la position :", entity.position)
                print("Block a la position :", self.position)

    def on_save_button_click(self):
        print("Coordonnées de tous les blocs :")
        for coordinate in self.coordinates:
            print("Bloc à la position :", coordinate)