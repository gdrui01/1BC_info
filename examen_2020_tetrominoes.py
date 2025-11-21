"""
EXAMEN DE FIN D’ÉTUDES SECONDAIRES CLASSIQUES 2020 — Informatique B
Sujet Tetrominoes Puzzle (pygame)

Ajoute ton lycée et ton numéro de candidat ici comme commentaire, par ex.:
# LYCEE_XYZ, candidat 123
"""

# Seules importations permises par le sujet pour le programme complet:
# import pygame
# from pygame.locals import *
# import sys
#
# Pour les parties logiques testées par le grader, aucune dépendance
# à Pygame n'est obligatoire.

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


# --- I. Dictionnaires COLORS et SHAPES ---------------------------------------

# Aide:
# - COLORS associe chaque kind ('I', 'O', ...) à une couleur.
#   Pour ne pas dépendre de pygame.Color dans le grader, on peut
#   stocker simplement le nom de la couleur (string).
# - SHAPES associe chaque kind à sa matrice de 0/1 (liste de listes).

COLORS: Dict[str, str] = {
    # TODO: complète selon l'énoncé.
    # Exemple:
    # "I": "cyan",
    # "O": "yellow",
    # ...
    # ... ton code ici ...
}

SHAPES: Dict[str, List[List[int]]] = {
    # TODO: complète selon le tableau de l'énoncé.
    # "I": [[1, 1, 1, 1]],
    # "O": [[1, 1], [1, 1]],
    # ...
    # ... ton code ici ...
}


# --- II. Classe Tetromino ----------------------------------------------------


@dataclass
class Tetromino:
    kind: str
    x: int = 0
    y: int = 0
    shape: List[List[int]] = None
    color: str = None

    def __post_init__(self):
        """
        Initialise shape et color à partir de SHAPES et COLORS.

        Aide:
        - self.kind doit être une clé de SHAPES / COLORS.
        - self.shape = copie profonde de SHAPES[self.kind]
        - self.color = COLORS[self.kind]
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tetromino.__post_init__")

    def get_cells(self) -> List[Tuple[int, int]]:
        """
        Retourne la liste des (x, y) des cellules effectivement occupées
        par le tétromino, en coordonnées de grille.

        Aide:
        - Parcours self.shape ligne par ligne.
          Pour chaque case où shape[i][j] == 1:
            cellule_x = self.x + j
            cellule_y = self.y + i
        - Ajoute (cellule_x, cellule_y) à une liste.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tetromino.get_cells")

    def move(self, dx: int, dy: int) -> None:
        """
        Déplace le tétromino de dx colonnes et dy lignes.

        Aide:
        - self.x += dx
        - self.y += dy
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tetromino.move")

    def rotate(self) -> None:
        """
        Fait tourner la matrice shape de 90° dans le sens positif (anti-horaire).

        Aide:
        - shape est une liste de lignes.
        - nombre de lignes: n = len(shape)
        - nombre de colonnes: m = len(shape[0])
        - Nouvelle shape a m lignes et n colonnes.
        - L'algorithme décrit dans l'énoncé:
          nouvelle[0] = dernière colonne de l'ancienne
          nouvelle[1] = avant-dernière colonne de l'ancienne
          ...
        - Indice de colonne j dans l'ancienne -> ligne correspondante dans la nouvelle.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: Tetromino.rotate")

    def draw(self, screen) -> None:
        """
        Dessine le tétromino sur la surface Pygame screen.

        Aide:
        - Utilise get_cells() pour connaître les cellules occupées.
        - Chaque cellule (cx, cy) correspond à un carré de 30x30 pixels,
          avec coin supérieur gauche aux coordonnées (cx*30, cy*30).
        - Remplis le carré avec self.color et dessine un bord noir.
        - Cette méthode ne sera pas testée par le grader (Pygame), mais
          tu peux la compléter pour avoir un jeu fonctionnel.
        """
        # ... code Pygame facultatif ...
        pass


# --- III. Classe TetrominoesList --------------------------------------------


class TetrominoesList:
    """
    Gère une liste de Tetromino.

    Attributs:
    - items: list[Tetromino]
    - selected_item: Tetromino | None
    - counts: dict[str, int] # nombre de tétrominos de chaque type
    """

    def __init__(self):
        """
        Initialisation comme demandé:
        - items = []
        - selected_item = None
        - counts = dict avec clés 'I','O','T','L','J','S','Z' et valeurs 0
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: TetrominoesList.__init__")

    def add(self, t: Tetromino) -> None:
        """
        Ajoute t à items et met selected_item = t.
        Met à jour counts.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: TetrominoesList.add")

    def remove(self, t: Tetromino) -> None:
        """
        Enlève t de items s'il y est, met selected_item à None
        si on l'a effectivement enlevé, et met à jour counts.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: TetrominoesList.remove")

    def get_item_containing(self, x: int, y: int) -> Optional[Tetromino]:
        """
        Retourne le premier Tetromino de items qui occupe la cellule (x, y),
        ou None si aucun n'occupe cette cellule.

        Aide:
        - Pour chaque t dans items:
            si (x, y) est dans t.get_cells():
                selected_item = t
                retourne t
        - Sinon, retourne None sans changer selected_item.
        """
        # ... ton code ici ...
        raise NotImplementedError("À compléter: TetrominoesList.get_item_containing")

    def draw(self, screen) -> None:
        """
        Dessine tous les tétrominos.

        Aide:
        - dessine d'abord tous ceux qui ne sont pas selected_item
        - puis dessine selected_item en dernier pour qu'il passe "au-dessus".
        - Cette méthode ne sera pas testée par le grader mais elle est utile
          pour le jeu complet.
        """
        # ... code Pygame facultatif ...
        pass


# --- IV. Fonction check_puzzle ----------------------------------------------


def check_puzzle(tlist: TetrominoesList) -> bool:
    """
    Vérifie si le puzzle central est correctement rempli.

    Pour simplifier le grader, on teste ici seulement:
    1. Il y a exactement 2 tétrominos de chaque type dans tlist.counts.
    2. L'ensemble de toutes les cellules occupées par tous les tétrominos:
       - correspond exactement à l'ensemble des 56 cellules du rectangle central
         (8 colonnes x 7 lignes),
       - et ne contient aucune cellule hors de ce rectangle.

    Aide:
    - rectangle central défini dans l'énoncé: 8x7 cellules.
      Selon ton choix de repère, définis un ensemble attendu, par ex.:
        expected = {(cx, cy) for cx in range(??) for cy in range(??)}
      (le grader supposera une convention simple, voir plus bas).
    - construit un ensemble cells avec toutes les cellules occupées
      par les tétrominos: union des t.get_cells() pour t dans tlist.items.
    - vérifie d'abord counts (== 2 pour chaque type), puis cells == expected.
    """
    # ... ton code ici ...
    raise NotImplementedError("À compléter: check_puzzle")
