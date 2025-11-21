"""
EXAMEN DE FIN D’ÉTUDES SECONDAIRES CLASSIQUES 2020 — Informatique B
Sujet Snake (Element / Snake / Pygame)

Ajoute ton code d’examen ici comme commentaire, par ex.:
# LXY_CB1_07
"""

# --- Question 1 : fonctions récursive et itérative fr / fi --------------------


def fr(n: int) -> int:
    """
    Version récursive de la fonction numeric fr décrite dans l'énoncé.

    TODO: adapte le corps à partir de l'énoncé officiel.

    Aide:
    - fr doit être définie sur les entiers >= 0.
    - Identifie dans l'énoncé:
      * le ou les cas de base (par ex. n == 0, n == 1, etc.)
      * le ou les cas récursifs (appel(s) à fr avec un paramètre plus petit).
    - Exemple de structure:
      if n == 0:
          return ...
      else:
          return ... fr(n-1) ...  # ou autre combinaison
    """
    # ... ton code ici ...
    raise NotImplementedError("À compléter: fonction récursive fr")


def fi(n: int) -> int:
    """
    Version itérative de la fonction fr.

    Aide:
    - Reproduis le même calcul que fr, mais avec une boucle
      (par ex. while ou for) au lieu d'appels récursifs.
    - Utilise éventuellement une ou plusieurs variables accumulatrices
      pour simuler ce que fait la version récursive.
    """
    # ... ton code ici ...
    raise NotImplementedError("À compléter: fonction itérative fi")


# --- Question 2 : classes Element et Snake (logique sans boucle Pygame) ------

from math import sqrt
from copy import deepcopy


class Element:
    """
    Représente un élément du jeu Snake (nourriture, poison, segment de corps, tête).

    Attributs:
    - x: int        # abscisse du centre (en pixels)
    - y: int        # ordonnée du centre (en pixels)
    - border_color  # couleur de bord (objet pygame.Color ou simple string)
    - fill_color    # couleur de remplissage

    Méthodes à implémenter:
    - __init__(x, y, border_color, fill_color)
    - draw(screen): dessin du disque (rayon 7, bord 1px)
    - move(dx, dy): déplacement du centre
    - has_touched(other): distance centres < 10 pixels ?
    """

    def __init__(self, x, y, border_color, fill_color):
        # Aide:
        # - stocke simplement les paramètres dans self.x, self.y, etc.
        # - ne fais PAS d'appels Pygame ici, cela reste une classe purement logique.
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Element.__init__")

    def draw(self, screen):
        """
        Dessine l'élément sur la surface Pygame 'screen'.

        Aide:
        - Importer pygame dans le fichier si tu veux tester pour de vrai:
          import pygame
        - Utilise pygame.draw.circle(screen, fill_color, (x, y), 7, width=0)
          puis un deuxième cercle pour le bord avec width=1.
        """
        # ... ton code ici (facultatif pour le grader, qui ne testera pas l'affichage) ...
        raise NotImplementedError("À compléter: Element.draw")

    def move(self, dx: int, dy: int) -> None:
        """
        Déplace l'élément de dx pixels horizontalement et dy pixels verticalement.
        """
        # Aide:
        # - self.x += dx
        # - self.y += dy
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Element.move")

    def has_touched(self, other: "Element") -> bool:
        """
        Retourne True si la distance entre les centres de self et other
        est strictement inférieure à 10 pixels.

        Aide:
        - distance = sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        - compare distance < 10
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Element.has_touched")


class Snake:
    """
    Modélise le serpent du jeu.

    Attributs:
    - head: Element          # la tête (couleur pourpre)
    - body: list[Element]    # les segments de corps
    - energy: int            # énergie, initialement 200
    - direction: tuple[int,int]
      (dx, dy) parmi:
        gauche: (-10, 0)
        droite: (10, 0)
        haut: (0, -10)
        bas: (0, 10)
    """

    # directions utiles (tu peux les utiliser dans ton code)
    LEFT = (-10, 0)
    RIGHT = (10, 0)
    UP = (0, -10)
    DOWN = (0, 10)

    def __init__(self, x: int, y: int):
        """
        Constructeur.

        Aide:
        - crée une tête Element(x, y, "purple4", "purple1")
        - crée le corps comme une liste de 5 Elements, chacun décalé de +10 pixels en x
          (vers la droite) par rapport au précédent, avec couleurs "gold4"/"gold1"
        - energy = 200
        - direction = Snake.LEFT
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.__init__")

    def move(self) -> None:
        """
        Fait avancer le serpent de 10 pixels dans la direction actuelle.

        Aide:
        - insère en tête de self.body un nouvel Element copiant l'ancienne tête
          (par ex. deepcopy(self.head)).
        - supprime le dernier élément de self.body (self.body.pop()).
        - met à jour self.head.x, self.head.y selon self.direction (dx, dy).
        - diminue self.energy de 1.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.move")

    def draw(self, screen) -> None:
        """
        Dessine la barre d'énergie puis le corps puis la tête.

        Aide pour la barre d'énergie:
        - rectangle jaune (hauteur 5) de longueur self.energy à partir de (5, 5)
        - rectangle bleu (hauteur 5) de longueur 200 - self.energy à partir de (5+self.energy, 5)
        - ensuite dessine chaque segment du corps avec Element.draw, puis la tête.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.draw")

    def grow(self) -> None:
        """
        Augmente la taille du serpent de 8 éléments.

        Aide:
        - prends le dernier élément du corps (tail = self.body[-1])
        - ajoute 8 copies (deepcopy(tail)) à la fin de self.body.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.grow")

    def has_hit_wall(self, max_x: int, max_y: int) -> bool:
        """
        Retourne True si la tête est à moins de 7 pixels d'un bord de la fenêtre.

        Aide:
        - distance à gauche: self.head.x
        - à droite: max_x - self.head.x
        - en haut: self.head.y
        - en bas: max_y - self.head.y
        - si l'une de ces distances est < 7, retourne True.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.has_hit_wall")

    def has_touched(self, elements: list[Element]) -> bool:
        """
        Retourne True si la tête a touché au moins un Element de la liste.

        Aide:
        - utilise Element.has_touched sur chaque élément de la liste.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Snake.has_touched")
