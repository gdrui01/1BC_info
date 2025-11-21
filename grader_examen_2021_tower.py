import os
import sys
import types
import importlib.util
from math import isclose

EXAM_PATH = os.path.join(
    os.path.dirname(__file__),
    "examen_2021_tower.py",
)


def _load_module(path: str) -> types.ModuleType:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier d'examen introuvable: {path}")
    spec = importlib.util.spec_from_file_location("examen_2021_tower", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def grade_bullet(mod: types.ModuleType) -> bool:
    if not hasattr(mod, "Bullet") or not hasattr(mod, "SIZE") or not hasattr(mod, "CENTER"):
        return False
    Bullet = mod.Bullet
    SIZE = mod.SIZE
    CENTER = mod.CENTER

    try:
        b = Bullet(mod.RIGHT)
        if (b.x, b.y) != (CENTER, CENTER):
            return False
        if b.radius != 5 or b.hit is not False:
            return False

        # Test déplacement à l'intérieur
        b.move()
        if (b.x, b.y) != (CENTER + 10, CENTER):
            return False
        if b.hit:
            return False

        # Test sortie de la surface
        b2 = Bullet(mod.LEFT)
        b2.x = 0  # au bord gauche
        b2.move()
        if not b2.hit:
            return False
        # ne doit pas rester strictement dans [0, SIZE) après un mouvement vers l'extérieur
        if 0 <= b2.x < SIZE and 0 <= b2.y < SIZE:
            return False
    except Exception:
        return False
    return True


def grade_tower(mod: types.ModuleType) -> bool:
    if not hasattr(mod, "Tower") or not hasattr(mod, "Bullet") or not hasattr(mod, "CENTER"):
        return False
    Tower = mod.Tower
    Bullet = mod.Bullet  # noqa: F841

    try:
        t = Tower()
        if (t.x, t.y) != (mod.CENTER, mod.CENTER):
            return False
        if t.dimension != 40:
            return False
        if t.damage != 0 or t.hits != 0 or t.shots != 0:
            return False
        if t.color not in ("darkgrey", "darkgray"):
            # On accepte l'une des orthographes
            return False
        if t.direction != mod.LEFT:
            return False
        if not isinstance(t.bullets, list) or len(t.bullets) != 0:
            return False

        # increase_damage
        t.increase_damage()
        if t.damage != 15:
            return False
        if t.color.lower() != "red":
            return False

        # repair
        for _ in range(20):
            t.repair()
        if t.damage != 0:
            return False
        if t.color not in ("darkgrey", "darkgray"):
            return False

        # shoot
        t.shoot()
        if t.shots != 1:
            return False
        if len(t.bullets) != 1:
            return False
        if not isinstance(t.bullets[0], Bullet):
            return False

    except Exception:
        return False
    return True


def grade_enemy(mod: types.ModuleType) -> bool:
    if not hasattr(mod, "Enemy") or not hasattr(mod, "Tower") or not hasattr(mod, "Bullet"):
        return False
    Enemy = mod.Enemy
    Tower = mod.Tower
    Bullet = mod.Bullet

    try:
        t = Tower()
        e = Enemy(100.0, 100.0, mod.RIGHT)
        if not isclose(e.distance_to(t), ((t.x - 100.0) ** 2 + (t.y - 100.0) ** 2) ** 0.5):
            return False

        # collision avec tour
        e2 = Enemy(float(t.x), float(t.y), mod.RIGHT)
        e2.check_hit(t)
        if not e2.hit:
            return False
        if t.damage == 0:
            return False

        # collision avec boulet
        t2 = Tower()
        t2.hits = 0
        b = Bullet(mod.RIGHT)
        # placer b très près de l'ennemi
        t2.bullets.append(b)
        e3 = Enemy(b.x + b.radius, b.y, mod.LEFT)
        e3.check_hit(t2)
        if not e3.hit:
            return False
        if not b.hit:
            return False
        if t2.hits != 1:
            return False

        # test move: vitesse 1 + hits/15
        t3 = Tower()
        t3.hits = 15  # speed = 2
        e4 = Enemy(50.0, 50.0, mod.RIGHT)
        old_x = e4.x
        e4.move(t3)
        if not isclose(e4.x, old_x + 2.0, rel_tol=1e-6):
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
        "Bullet": grade_bullet(mod),
        "Tower": grade_tower(mod),
        "Enemy": grade_enemy(mod),
    }

    print("Résultats du grader — Examen 2021 Tower defense :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
