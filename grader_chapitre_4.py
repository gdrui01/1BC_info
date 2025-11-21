import os
import sys
import types
import nbformat
import math


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_4_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    séquentiellement toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_4_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs des cellules qui ne concernent pas les exos S1-S3.
            pass

    return module


# --- Tests pour SimplePoint (S1) ---


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la classe SimplePoint.
    """
    if not hasattr(mod, "SimplePoint"):
        return False
    SimplePoint = mod.SimplePoint

    try:
        # Test constructeur et attributs
        p = SimplePoint(1, 2)
        if not hasattr(p, "x") or not hasattr(p, "y"):
            return False
        if p.x != 1 or p.y != 2:
            return False

        # Test __str__
        if str(p) != "(1; 2)":
            return False

        # Test distance_to
        p0 = SimplePoint(0, 0)
        p34 = SimplePoint(3, 4)
        if abs(p0.distance_to(p34) - 5.0) > 1e-9:
            return False

        # Test move
        p_move = SimplePoint(1, 1)
        p_move.move(2, -1)
        if p_move.x != 3 or p_move.y != 0:
            return False

    except Exception:
        return False

    return True


# --- Tests pour Rectangle (S2) ---


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la classe Rectangle.
    """
    if not hasattr(mod, "Rectangle"):
        return False
    Rectangle = mod.Rectangle

    try:
        r = Rectangle(3.0, 4.0)
        if not hasattr(r, "width") or not hasattr(r, "height"):
            return False
        if r.width != 3.0 or r.height != 4.0:
            return False

        if str(r) != "Rectangle(width=3.0, height=4.0)":
            return False

        if abs(r.area() - 12.0) > 1e-9:
            return False

        if abs(r.perimeter() - 14.0) > 1e-9:
            return False

        if r.is_square():
            return False

        r2 = Rectangle(5, 5)
        if not r2.is_square():
            return False

    except Exception:
        return False

    return True


# --- Tests pour StackLite (S3) ---


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la classe StackLite.
    """
    if not hasattr(mod, "StackLite"):
        return False
    StackLite = mod.StackLite

    try:
        s = StackLite()

        # Pile vide
        if not s.is_empty():
            return False
        if s.size() != 0:
            return False
        if s.pop() is not None:
            return False
        if s.top() is not None:
            return False

        # Empilement
        s.push(1)
        s.push(2)
        s.push(3)

        if s.is_empty():
            return False
        if s.size() != 3:
            return False
        if s.top() != 3:
            return False

        # Représentation (on teste seulement un format minimal)
        rep = str(s)
        if "StackLite" not in rep:
            return False
        # On attend l'ordre top -> 3 2 1
        if "3" not in rep or "2" not in rep or "1" not in rep:
            return False

        # Dépilement
        if s.pop() != 3:
            return False
        if s.pop() != 2:
            return False
        if s.pop() != 1:
            return False
        if not s.is_empty():
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 4) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
