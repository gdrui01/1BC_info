import os
import sys
import types
import nbformat
import math


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_8_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    toutes les cellules de type 'code' dans un namespace isolé.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_8_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs des cellules d'exemple/plot.
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction poly_values.
    """
    if not hasattr(mod, "poly_values"):
        return False
    f = mod.poly_values

    try:
        # P(x) = 1 + 2x + 3x^2
        coeffs = [1, 2, 3]
        xs, ys = f(coeffs, 0.0, 2.0, 3)
        # xs doit contenir 3 points: 0.0, 1.0, 2.0 (ou équivalents flottants)
        if len(xs) != 3 or len(ys) != 3:
            return False
        # Vérifier quelques valeurs exactes
        for x, y in zip(xs, ys):
            expected = 1 + 2 * x + 3 * x * x
            if abs(y - expected) > 1e-9:
                return False

    except Exception:
        return False

    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction derivative_coeffs.
    """
    if not hasattr(mod, "derivative_coeffs"):
        return False
    f = mod.derivative_coeffs

    try:
        # P(x) = 1 + 2x + 3x^2 -> P'(x) = 2 + 6x
        if f([1, 2, 3]) != [2, 6]:
            return False
        # P(x) = 5 -> 0
        if f([5]) != []:
            return False
        # P(x) = 0 -> 0
        if f([]) != []:
            return False

    except Exception:
        return False

    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction second_derivative_coeffs.
    """
    if not hasattr(mod, "second_derivative_coeffs"):
        return False
    f = mod.second_derivative_coeffs

    try:
        # P(x) = 1 + 2x + 3x^2 -> P''(x) = 6
        if f([1, 2, 3]) != [6]:
            return False
        # P(x) = 1 + 2x -> P''(x) = 0
        if f([1, 2]) != []:
            return False
        # P(x) = 5 -> 0
        if f([5]) != []:
            return False
        # P(x) = 0 -> 0
        if f([]) != []:
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 8) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
