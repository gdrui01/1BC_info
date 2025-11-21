import os
import sys
import types
import nbformat


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_5_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_5_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs des cellules interactives/pygame
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction within_window.
    """
    if not hasattr(mod, "within_window"):
        return False
    f = mod.within_window

    tests = [
        ((0, 0, 10, 10), True),
        ((9, 9, 10, 10), True),
        ((10, 0, 10, 10), False),
        ((0, 10, 10, 10), False),
        ((-1, 5, 10, 10), False),
        ((5, -1, 10, 10), False),
        ((5, 5, 6, 6), True),
        ((6, 6, 6, 6), False),
    ]

    try:
        for (x, y, w, h), expected in tests:
            if f(x, y, w, h) != expected:
                return False
    except Exception:
        return False

    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction random_point_in_window.
    """
    if not hasattr(mod, "random_point_in_window"):
        return False
    f = mod.random_point_in_window

    w, h = 10, 20

    try:
        for _ in range(100):
            x, y = f(w, h)
            if not (0 <= x < w and 0 <= y < h):
                return False
    except Exception:
        return False

    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la classe MovingSquare.
    """
    if not hasattr(mod, "MovingSquare"):
        return False
    MovingSquare = mod.MovingSquare

    try:
        # Test simple sans rebond
        sq = MovingSquare(10, 10, 5, 1, 2, 100, 100)
        sq.update()
        if (sq.x, sq.y) != (11, 12):
            return False

        # Test rebond à droite
        sq = MovingSquare(95, 10, 10, 5, 0, 100, 100)
        # Après update, le carré sort, il doit rebondir
        sq.update()
        if not (0 <= sq.x <= 90):
            return False
        if sq.vx >= 0:
            return False  # vx devrait avoir inversé de signe

        # Test rebond en bas
        sq = MovingSquare(10, 95, 10, 0, 5, 100, 100)
        sq.update()
        if not (0 <= sq.y <= 90):
            return False
        if sq.vy >= 0:
            return False  # vy devrait avoir inversé de signe

        # Test rebond à gauche
        sq = MovingSquare(0, 10, 10, -5, 0, 100, 100)
        sq.update()
        if sq.x < 0:
            return False
        if sq.vx <= 0:
            return False

        # Test rebond en haut
        sq = MovingSquare(10, 0, 10, 0, -5, 100, 100)
        sq.update()
        if sq.y < 0:
            return False
        if sq.vy <= 0:
            return False

    except Exception:
        return False

    return True


def main() -> None:
    try:
        mod = _load_notebook_as_module(NOTEBOOK_PATH)
    except Exception as e:
        print("Erreur lors du chargement du notebook :", e)
        sys.exit(1)

    results = {
        "S1": grade_s1(mod),
        "S2": grade_s2(mod),
        "S3": grade_s3(mod),
    }

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 5) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
