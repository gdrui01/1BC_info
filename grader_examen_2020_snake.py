import os
import sys
import types
import importlib.util

EXAM_PATH = os.path.join(
    os.path.dirname(__file__),
    "examen_2020_snake.py",
)


def _load_module(path: str) -> types.ModuleType:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier d'examen introuvable: {path}")
    spec = importlib.util.spec_from_file_location("examen_2020_snake", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def grade_fr_fi(mod: types.ModuleType) -> bool:
    """
    Vérifie que fr et fi existent et donnent les mêmes résultats
    sur quelques valeurs tests (sans vérifier la spécification exacte).
    """
    if not hasattr(mod, "fr") or not hasattr(mod, "fi"):
        return False
    fr = mod.fr
    fi = mod.fi

    try:
        tests = [0, 1, 2, 3, 5, 7, 10]
        values_r = [fr(n) for n in tests]
        values_i = [fi(n) for n in tests]
        if values_r != values_i:
            return False
    except Exception:
        return False
    return True


def grade_element(mod: types.ModuleType) -> bool:
    """
    Vérifie quelques comportements de base de la classe Element:
    - attributs x, y,
    - move,
    - has_touched.
    """
    if not hasattr(mod, "Element"):
        return False
    Element = mod.Element

    try:
        e1 = Element(10, 10, "black", "white")
        e2 = Element(17, 10, "black", "white")
        # move
        e1.move(5, -2)
        if (e1.x, e1.y) != (15, 8):
            return False
        # distance 7 -> touché
        if not e1.has_touched(e2):
            return False
        # éloigner e2
        e2.move(100, 0)
        if e1.has_touched(e2):
            return False
    except Exception:
        return False
    return True


def grade_snake_basic(mod: types.ModuleType) -> bool:
    """
    Vérifie quelques aspects de base de Snake:
    - initialisation des attributs,
    - move diminue l'énergie, déplace la tête et fait évoluer la taille du corps,
    - grow ajoute 8 éléments.
    """
    if not hasattr(mod, "Snake") or not hasattr(mod, "Element"):
        return False
    Snake = mod.Snake
    Element = mod.Element  # noqa: F841 (import logique)

    try:
        s = Snake(100, 100)
        if s.energy != 200:
            return False
        if not isinstance(s.head, Element):
            return False
        if not isinstance(s.body, list) or len(s.body) != 5:
            return False

        # stocker position initiale de la tête
        x0, y0 = s.head.x, s.head.y
        # direction doit être un tuple de deux ints
        dx, dy = s.direction
        # un move doit déplacer de (dx, dy)
        s.move()
        if (s.head.x, s.head.y) != (x0 + dx, y0 + dy):
            return False
        if s.energy != 199:
            return False

        # grow ajoute 8 éléments
        size_before = len(s.body)
        s.grow()
        if len(s.body) != size_before + 8:
            return False

        # has_hit_wall: placer la tête près d'un bord
        s.head.x, s.head.y = 3, 50
        if not s.has_hit_wall(600, 400):
            return False
        s.head.x, s.head.y = 300, 200
        if s.has_hit_wall(600, 400):
            return False

        # has_touched : tête qui touche un élément
        food = [Element(s.head.x + 5, s.head.y, "orange4", "orange1")]
        if not s.has_touched(food):
            return False
        far = [Element(s.head.x + 100, s.head.y + 100, "orange4", "orange1")]
        if s.has_touched(far):
            return False

    except Exception:
        return False
    return True


def main() -> None:
    try:
        mod = _load_module(EXAM_PATH)
    except Exception as e:
        print("Erreur lors du chargement du fichier d'examen:", e)
        sys.exit(1)

    results = {
        "Q1_fr_fi": grade_fr_fi(mod),
        "Q2_Element": grade_element(mod),
        "Q2_Snake": grade_snake_basic(mod),
    }

    print("Résultats du grader — Examen 2020 Snake :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
