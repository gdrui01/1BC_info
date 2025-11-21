import os
import sys
import tempfile
import types
import nbformat

NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_1_interactif.ipynb",
)

EXERCICES = ["S1", "S2", "S3"]


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    séquentiellement toutes les cellules de type 'code' dans un namespace.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_1_interactif_module")

    # Namespace dans lequel les cellules seront exécutées
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs d'exécution pour ne pas bloquer le grader
            # (par ex. une cellule interactive avec input non utilisée par les exos S1-S3).
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction somme_1_a_n.
    """
    if not hasattr(mod, "somme_1_a_n"):
        return False
    f = mod.somme_1_a_n

    tests = [
        (1, 1),
        (2, 3),
        (3, 6),
        (5, 15),
        (10, 55),
    ]

    try:
        for n, expected in tests:
            if f(n) != expected:
                return False
    except Exception:
        return False
    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction compter_voyelles.
    """
    if not hasattr(mod, "compter_voyelles"):
        return False
    f = mod.compter_voyelles

    tests = [
        ("", 0),
        ("Bonjour", 3),      # o, o, u
        ("PYTHON", 1),       # O
        ("aeiouy", 6),
        ("AEIOUY", 6),
        ("BcDfG", 0),
        ("Salut les Amis", 6),
    ]

    try:
        for s, expected in tests:
            if f(s) != expected:
                return False
    except Exception:
        return False
    return True


def _create_temp_file_with_content(lines):
    """
    Crée un fichier temporaire contenant 'lines' (liste de strings sans '\n'),
    et renvoie son chemin.
    """
    fd, path = tempfile.mkstemp(text=True)
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return path


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction moyenne_fichier_entiers.
    """
    if not hasattr(mod, "moyenne_fichier_entiers"):
        return False
    f = mod.moyenne_fichier_entiers

    try:
        # Test 1
        path1 = _create_temp_file_with_content(["2", "4", "6"])
        if abs(f(path1) - 4.0) > 1e-9:
            return False

        # Test 2
        path2 = _create_temp_file_with_content(["5"])
        if abs(f(path2) - 5.0) > 1e-9:
            return False

        # Test 3
        path3 = _create_temp_file_with_content(["1", "2", "3", "4"])
        if abs(f(path3) - 2.5) > 1e-9:
            return False

    except Exception:
        return False
    finally:
        # On ne supprime pas forcément les fichiers temporaires ici pour
        # simplifier, mais on pourrait le faire si nécessaire.
        pass

    return True


def main() -> None:
    try:
        mod = _load_notebook_as_module(NOTEBOOK_PATH)
    except Exception as e:
        print("Erreur lors du chargement du notebook :", e)
        sys.exit(1)

    results = {}

    results["S1"] = grade_s1(mod)
    results["S2"] = grade_s2(mod)
    results["S3"] = grade_s3(mod)

    print("Résultats du grader pour les exercices supplémentaires:")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
