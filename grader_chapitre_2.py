import os
import sys
import tempfile
import types
import nbformat


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_2_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    séquentiellement toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_2_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs de cellules interactives
            # (par ex. avec input()) qui ne sont pas nécessaires
            # pour les exercices S1-S3.
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction extremes_tuple.
    """
    if not hasattr(mod, "extremes_tuple"):
        return False
    f = mod.extremes_tuple

    tests = [
        ((1, 2, 3), (1, 3)),
        ((5, 5, 5), (5, 5)),
        ((-1, 10, 3), (-1, 10)),
        ((0,), (0, 0)),
        ((7, -2, 7, 4), (-2, 7)),
    ]

    try:
        for t, expected in tests:
            if f(t) != expected:
                return False
    except Exception:
        return False
    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction inverser_dict.
    """
    if not hasattr(mod, "inverser_dict"):
        return False
    f = mod.inverser_dict

    tests = [
        ({"a": 1, "b": 2}, {1: "a", 2: "b"}),
        ({"x": 10, "y": 20, "z": 30}, {10: "x", 20: "y", 30: "z"}),
        ({}, {}),  # cas limite : dictionnaire vide
    ]

    try:
        for d_in, d_expected in tests:
            result = f(d_in)
            if result != d_expected:
                return False
    except Exception:
        return False
    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction frequences_mots.
    """
    if not hasattr(mod, "frequences_mots"):
        return False
    f = mod.frequences_mots

    tests = [
        ("", {}),
        ("bonjour", {"bonjour": 1}),
        ("bonjour bonjour", {"bonjour": 2}),
        ("bonjour le monde", {"bonjour": 1, "le": 1, "monde": 1}),
        ("  bonjour   le   monde  ", {"bonjour": 1, "le": 1, "monde": 1}),
        ("a b a b a", {"a": 3, "b": 2}),
    ]

    try:
        for texte, expected in tests:
            result = f(texte)
            if result != expected:
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 2) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
