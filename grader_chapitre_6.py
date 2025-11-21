import os
import sys
import types
import nbformat


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_6_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    séquentiellement toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_6_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs des cellules non pertinentes (exemples interactifs, input, etc.).
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction count_comparisons_selection.
    """
    if not hasattr(mod, "count_comparisons_selection"):
        return False
    f = mod.count_comparisons_selection

    try:
        for n in [1, 2, 3, 5, 10]:
            # liste quelconque, peu importe le contenu
            a = list(range(n))
            expected = n * (n - 1) // 2
            if f(a) != expected:
                return False
    except Exception:
        return False

    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction count_comparisons_insertion.
    """
    if not hasattr(mod, "count_comparisons_insertion"):
        return False
    f = mod.count_comparisons_insertion

    try:
        # Liste déjà triée (best case)
        a_sorted = [1, 2, 3, 4, 5]
        c_best = f(a_sorted)
        # Liste triée à l'envers (worst case)
        a_rev = [5, 4, 3, 2, 1]
        c_worst = f(a_rev)
        # On s'attend à ce que le worst case nécessite plus de comparaisons que le best case
        if not (c_best <= c_worst):
            return False

        # Test sur une liste avec éléments répétés
        a_rep = [2, 2, 2, 2]
        c_rep = f(a_rep)
        # Nombre de comparaisons doit être raisonnable (>= 0) ; on vérifie juste que la fonction s'exécute
        if c_rep < 0:
            return False

    except Exception:
        return False

    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction is_sorted.
    """
    if not hasattr(mod, "is_sorted"):
        return False
    f = mod.is_sorted

    tests_true = [
        [],
        [1],
        [1, 2, 3],
        [1, 1, 2, 2, 3],
        [-5, -3, -3, 0, 10],
    ]
    tests_false = [
        [2, 1],
        [1, 3, 2],
        [0, 0, -1],
        [5, 4, 5],
    ]

    try:
        for a in tests_true:
            if not f(list(a)):
                return False
        for a in tests_false:
            if f(list(a)):
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 6) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
