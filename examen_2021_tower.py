"""
EXAMEN DE FIN D’ÉTUDES SECONDAIRES CLASSIQUES 2021 — Informatique B
Jeu de style « Tower defense »

Ajoute ton code d’examen ici comme commentaire, par ex.:
# LXY_CB1_01
"""

# --- 1. IMPORTATIONS ET CONSTANTES -------------------------------------------
# Seules importations permises dans la version complète :
#   import pygame
#   from pygame.locals import *
#   import sys
#   from math import sqrt
#   from random import randint

# Ici, on ne force pas pygame pour permettre de tester la logique sans affichage.
from math import sqrt

# Constantes demandées
SIZE = 500
CENTER = SIZE // 2

LEFT = (-1, 0)
UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)

FPS = 30  # utilisé dans le programme principal complet (non fourni ici)


# --- 2.a Classe Bullet --------------------------------------------------------


class Bullet:
    """
    Représente un boulet de canon.

    Attributs:
    - direction: tuple[int,int]  (LEFT, UP, RIGHT ou DOWN)
    - x, y: int                  coordonnées du centre (en pixels)
    - radius: int                (5 pixels)
    - hit: bool                  True si le boulet a touché un bord ou un ennemi
    """

    def __init__(self, direction):
        """
        Constructeur.

        Aide:
        - self.direction = direction
        - self.x = CENTER
        - self.y = CENTER
        - self.radius = 5
        - self.hit = False
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Bullet.__init__")

    def draw(self, screen):
        """
        Dessine un disque noir de centre (x, y) et de rayon radius sur la surface Pygame screen.

        Aide (dans ta version complète):
        - import pygame
        - pygame.draw.circle(screen, "black", (self.x, self.y), self.radius)
        """
        # Le grader ne teste pas l'affichage.
        pass

    def move(self):
        """
        Déplace le boulet de 10 pixels dans sa direction, tant que son centre reste
        dans la surface de jeu [0, SIZE) × [0, SIZE).

        Si le centre sort de la surface, met self.hit = True.
        """
        # Aide:
        # dx, dy = self.direction
        # tentative: nx = self.x + 10*dx, ny = self.y + 10*dy
        # si 0 <= nx < SIZE et 0 <= ny < SIZE: mettre à jour self.x, self.y
        # sinon: self.hit = True
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Bullet.move")


# --- 2.b Classe Tower ---------------------------------------------------------


class Tower:
    """
    Représente la tour et son canon.

    Attributs:
    - x, y: int            centre de la tour (pixels, au centre de la fenêtre)
    - dimension: int       taille de la base carrée (40)
    - damage: int          dégâts subis (0 au début)
    - hits: int            nombre d'ennemis détruits
    - shots: int           nombre total de boulets tirés
    - color: str/Color     couleur actuelle de la tour (ex. "darkgrey" ou "red")
    - bullets: list[Bullet]
    - direction: tuple[int,int] (LEFT / UP / RIGHT / DOWN)
    """

    def __init__(self):
        """
        Constructeur.

        Aide:
        - x, y = CENTER, CENTER
        - dimension = 40
        - damage = hits = shots = 0
        - color = "darkgrey"
        - bullets = []
        - direction = LEFT
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tower.__init__")

    def draw(self, screen):
        """
        Dessine la tour (base + canon + haut) sur la surface Pygame screen.

        Aide (dans la version complète):
        - base: carré de côté dimension, centré en (x, y), couleur self.color, bordure noire 2 px
        - canon: segment noir d'origine (x, y), longueur 30 px, épaisseur 11 px
                 direction donnée par self.direction
        - haut: carré de côté dimension//2, centré en (x, y), couleur self.color, bordure noire 2 px
        """
        # Non testé par le grader.
        pass

    def increase_damage(self):
        """
        Augmente le damage de 15 et met la couleur sur rouge.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tower.increase_damage")

    def repair(self):
        """
        Répare la tour: décrémente damage de 1 si > 0.
        Quand damage retombe à 0, remet la couleur sur gris foncé.
        """
        # Aide:
        # if self.damage > 0: self.damage -= 1
        # if self.damage == 0: self.color = "darkgrey"
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tower.repair")

    def shoot(self):
        """
        Crée un Bullet dans la direction actuelle, l'ajoute à self.bullets, incrémente shots.
        """
        # Aide:
        # b = Bullet(self.direction)
        # self.bullets.append(b)
        # self.shots += 1
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tower.shoot")


# --- 2.c Classe Enemy ---------------------------------------------------------


class Enemy:
    """
    Représente un ennemi (disque jaune) qui se dirige vers la tour.

    Attributs:
    - x, y: float          centre (pixels)
    - direction: tuple[int,int] (LEFT/UP/RIGHT/DOWN)
    - radius: int          (10 pixels)
    - hit: bool            ennemi détruit ou ayant touché la tour
    """

    def __init__(self, x, y, direction):
        """
        Constructeur.

        Aide:
        - self.x, self.y = x, y
        - self.direction = direction
        - self.radius = 10
        - self.hit = False
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Enemy.__init__")

    def draw(self, screen):
        """
        Dessine l’ennemi sous forme de disque jaune sur screen.

        Aide (dans la version complète):
        - pygame.draw.circle(screen, "yellow", (int(self.x), int(self.y)), self.radius)
        """
        # Non testé par le grader.
        pass

    def distance_to(self, other) -> float:
        """
        Retourne la distance euclidienne entre l'ennemi courant et un autre objet ayant
        des attributs x et y (centre).

        Aide:
        - dx = self.x - other.x
        - dy = self.y - other.y
        - return sqrt(dx*dx + dy*dy)
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Enemy.distance_to")

    def check_hit(self, tower: Tower):
        """
        Vérifie les collisions entre l'ennemi, la tour et les boulets de la tour.

        Effets attendus:
        - collision avec la tour:
            * si distance <= seuil (par ex. self.radius + tower.dimension/2),
              alors self.hit = True et tower.increase_damage()
        - collision avec un boulet:
            * si distance <= self.radius + bullet.radius,
              alors self.hit = True, bullet.hit = True, tower.hits += 1

        Aide:
        - utiliser distance_to(tower) pour la tour
        - parcourir tower.bullets, utiliser distance_to(bullet)
        - choisir des seuils raisonnables basés sur les rayons/dimensions
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Enemy.check_hit")

    def move(self, tower: Tower):
        """
        Déplace l’ennemi vers la tour avec une vitesse dépendant des hits de la tour,
        puis vérifie les collisions.

        speed = 1 + tower.hits / 15

        Aide:
        - si self.hit est déjà True, tu peux éventuellement ne plus le déplacer
        - dx, dy = self.direction
        - self.x += dx * speed
        - self.y += dy * speed
        - ensuite appeler self.check_hit(tower)
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Enemy.move")
