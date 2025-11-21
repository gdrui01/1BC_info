"""
EXAMEN DE FIN D’ÉTUDES SECONDAIRES CLASSIQUES 2022 — Informatique B
Question 1 : Code de César

Ajoute ici tes infos (lycée + numéro de candidat), par ex.:
# LYCEE_XYZ, candidat 123
"""

from string import ascii_uppercase  # unique importation permise


def encryption_dict(shift: int) -> dict:
    """
    Construit et renvoie le dictionnaire de chiffrement pour un décalage 'shift'.

    - Clés: lettres majuscules 'A'..'Z'
    - Valeurs: lettre majuscule codée après décalage circulaire de 'shift' positions.
    - shift peut être négatif (décalage vers la gauche).

    Exemple:
        shift = 3 -> 'A' -> 'D', 'B' -> 'E', ..., 'X' -> 'A', 'Y' -> 'B', 'Z' -> 'C'
    """
    # Aide:
    # - n = len(ascii_uppercase) (26)
    # - pour chaque indice i, lettre claire = ascii_uppercase[i]
    # - nouvelle position j = (i + shift) % n
    # - lettre codée = ascii_uppercase[j]
    # - remplir un dict et le retourner
    # ... ton code ici ...
    raise NotImplementedError("À compléter: encryption_dict")


def _build_decryption_dict(shift: int) -> dict:
    """
    Construit un dictionnaire de DÉCHIFFREMENT à partir du shift (utilise le shift opposé).

    Aide:
    - Pour décoder, on applique le shift -shift.
    - On peut donc réutiliser encryption_dict(-shift).
    """
    # ... ton code ici ...
    raise NotImplementedError("À compléter: _build_decryption_dict")


def _detect_shift_and_decode(cypher_path: str, plain_path: str) -> None:
    """
    Analyse le fichier cypher_path pour:
      - compter la fréquence de chaque lettre A..Z,
      - trouver la lettre la plus fréquente,
      - en déduire le shift (en supposant que la lettre claire la plus fréquente est 'E'),
      - décoder le texte et l'écrire dans plain_path.

    Le format (espaces, ponctuation, retours à la ligne) doit être conservé.
    Seules les lettres majuscules doivent être transformées.
    """
    # Aide (structure suggérée):
    # 1) ouvrir cypher_file en lecture, plain_file en écriture
    # 2) créer frequencies = [0]*26
    # 3) parcourir toutes les lignes pour remplir frequencies
    #    (n'incrémenter que pour les lettres majuscules)
    # 4) déterminer l'indice max_idx correspondant à la fréquence max
    #    (lettre la plus fréquente dans le texte chiffré = ascii_uppercase[max_idx])
    # 5) on suppose que cette lettre vient de 'E':
    #    shift = (max_idx - ascii_uppercase.index('E')) mod 26
    # 6) construire le dict de déchiffrement via _build_decryption_dict(shift)
    # 7) REparcourir le fichier chiffré, pour chaque caractère:
    #    - si c est dans ascii_uppercase: le remplacer via d[c]
    #    - sinon: le laisser tel quel
    #    puis écrire dans plain_file
    # ... ton code ici ...
    raise NotImplementedError("À compléter: _detect_shift_and_decode")


def main() -> None:
    """
    Programme principal pour la question 1.

    Aide:
    - adapter les chemins vers 'cypher.txt' et 'plain.txt' selon les consignes de l'examen.
    """
    cypher_path = "cypher.txt"
    plain_path = "plain.txt"
    _detect_shift_and_decode(cypher_path, plain_path)


if __name__ == "__main__":
    main()
