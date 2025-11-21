import os
import sys
import types
import nbformat


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_3_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    séquentiellement toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_3_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs des cellules interactives
            # (par ex. celles contenant des input()).
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction somme_liste_rec.
    """
    if not hasattr(mod, "somme_liste_rec"):
        return False
    f = mod.somme_liste_rec

    tests = [
        ([], 0),
        ([1], 1),
        ([1, 2, 3], 6),
        ([-1, 1, -2, 2], 0),
        (list(range(1, 11)), 55),
    ]

    try:
        for L, expected in tests:
            if f(L) != expected:
                return False
    except Exception:
        return False
    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction inverse_chaine_rec.
    """
    if not hasattr(mod, "inverse_chaine_rec"):
        return False
    f = mod.inverse_chaine_rec

    tests = [
        ("", ""),
        ("a", "a"),
        ("abc", "cba"),
        ("radar", "radar"),
        ("recursivite", "etivisrucer"),
        ("bonjour le monde", "ednom el ruojnob"),
    ]

    try:
        for s, expected in tests:
            if f(s) != expected:
                return False
    except Exception:
        return False
    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction pgcd_rec_ex.
    """
    if not hasattr(mod, "pgcd_rec_ex"):
        return False
    f = mod.pgcd_rec_ex

    tests = [
        (48, 18, 6),
        (18, 48, 6),
        (7, 5, 1),
        (12, 4, 4),
        (100, 10, 10),
        (17, 17, 17),
    ]

    try:
        for a, b, expected in tests:
            if f(a, b) != expected:
                return False

        # Tests d'erreur (valeurs non positives)
        error_cases = [
            (0, 5),
            (5, 0),
            (-1, 3),
            (3, -2),
        ]
        for a, b in error_cases:
            try:
                f(a, b)
                # Si aucune erreur n'est levée, c'est un échec
                return False
            except ValueError:
                # Comportement attendu
                continue
            except Exception:
                # Mauvais type d'exception
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 3) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
