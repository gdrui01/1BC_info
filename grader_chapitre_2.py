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


def grade_t2(mod: types.ModuleType) -> bool:
    """
    Vérifie l'exercice T2 :
    - distance_manhattan(p1, p2)
    - swap_tuple(t)
    """
    # distance_manhattan
    if not hasattr(mod, "distance_manhattan"):
        return False
    f_dist = mod.distance_manhattan

    dist_tests = [
        (((0, 0), (0, 0)), 0),
        (((0, 0), (1, 1)), 2),
        (((3, 5), (1, 2)), 5),
        (((-1, -2), (2, 2)), 7),
    ]

    try:
        for (p1, p2), expected in dist_tests:
            if f_dist(p1, p2) != expected:
                return False
    except Exception:
        return False

    # swap_tuple
    if not hasattr(mod, "swap_tuple"):
        return False
    f_swap = mod.swap_tuple

    swap_tests = [
        ((1, 2), (2, 1)),
        (("a", "b"), ("b", "a")),
        ((0, 0), (0, 0)),
    ]

    try:
        for t, expected in swap_tests:
            if f_swap(t) != expected:
                return False
    except Exception:
        return False

    return True


# --- nouveaux graders pour T1, D1, D2 ---


def grade_t1(mod: types.ModuleType) -> bool:
    """
    Vérifie l'exercice T1 de façon minimale :
    - existence d'un tuple 'point'
    - existence d'un tuple 'date'
    - décomposition point -> (x, y) cohérente
    """
    if not hasattr(mod, "point"):
        return False
    if not hasattr(mod, "date"):
        return False

    point = getattr(mod, "point")
    date = getattr(mod, "date")

    if not (isinstance(point, tuple) and len(point) == 2):
        return False
    if not (isinstance(date, tuple) and len(date) == 3):
        return False

    # On tolère n'importe quelles valeurs tant que les longueurs sont correctes
    return True


def grade_d1(mod: types.ModuleType) -> bool:
    """
    Vérifie l'exercice D1 :
    - dictionnaire 'capitales' existant
    - au moins 3 entrées string -> string
    """
    if not hasattr(mod, "capitales"):
        return False
    capitales = getattr(mod, "capitales")

    if not isinstance(capitales, dict):
        return False
    if len(capitales) < 3:
        return False

    # toutes les clés/valeurs doivent être des strings
    for k, v in capitales.items():
        if not isinstance(k, str) or not isinstance(v, str):
            return False

    return True


def grade_d2(mod: types.ModuleType) -> bool:
    """
    Vérifie l'exercice D2 :
    - notes_par_eleve construit correctement à partir de 'notes'
    """
    if not hasattr(mod, "notes_par_eleve"):
        return False
    if not hasattr(mod, "notes"):
        return False

    notes_par_eleve = getattr(mod, "notes_par_eleve")
    notes = getattr(mod, "notes")

    if not isinstance(notes_par_eleve, dict):
        return False

    # on reconstruit l'attendu
    expected: dict[str, list[int]] = {}
    for nom, note in notes:
        expected.setdefault(nom, []).append(note)

    # comparer les ensembles de clés
    if set(notes_par_eleve.keys()) != set(expected.keys()):
        return False

    # comparer les listes de notes (ordre identique si l'étudiant suit l'énoncé)
    for nom, lst in expected.items():
        val = notes_par_eleve.get(nom)
        if not isinstance(val, list):
            return False
        if val != lst:
            return False

    return True


# --- fonctions de vérification "haut niveau" par exercice ---


def verify_exS1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie S1 (extremes_tuple).
    Si mod est None, charge le notebook chapitre_2_interactif.
    """
    print("=== Vérification Chapitre 2 - Exercice S1 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_s1(mod)
    print("Résultat S1 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exS2(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie S2 (inverser_dict).
    """
    print("=== Vérification Chapitre 2 - Exercice S2 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_s2(mod)
    print("Résultat S2 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exS3(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie S3 (frequences_mots).
    """
    print("=== Vérification Chapitre 2 - Exercice S3 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_s3(mod)
    print("Résultat S3 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exT2(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie T2 (distance_manhattan et swap_tuple).
    """
    print("=== Vérification Chapitre 2 - Exercice T2 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_t2(mod)
    print("Résultat T2 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exT1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie T1 (décomposition de tuples).
    """
    print("=== Vérification Chapitre 2 - Exercice T1 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_t1(mod)
    print("Résultat T1 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exD1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie D1 (dictionnaire de capitales).
    """
    print("=== Vérification Chapitre 2 - Exercice D1 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_d1(mod)
    print("Résultat D1 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exD2(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie D2 (notes_par_eleve).
    """
    print("=== Vérification Chapitre 2 - Exercice D2 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_d2(mod)
    print("Résultat D2 :", "Réussi" if ok else "Échoué")
    return ok


def run_grader_for_specific_exercise(exercise_code: str, mod: types.ModuleType | None = None) -> bool:
    """
    Dispatcher simple :
    - 'T1' -> verify_exT1
    - 'T2' -> verify_exT2
    - 'D1' -> verify_exD1
    - 'D2' -> verify_exD2
    - 'S1' -> verify_exS1
    - 'S2' -> verify_exS2
    - 'S3' -> verify_exS3

    (On garde un paramètre string plutôt qu'un entier pour rester
    cohérent avec S1/S2/S3.)
    """
    if exercise_code == "T1":
        return verify_exT1(mod)
    elif exercise_code == "T2":
        return verify_exT2(mod)
    elif exercise_code == "D1":
        return verify_exD1(mod)
    elif exercise_code == "D2":
        return verify_exD2(mod)
    elif exercise_code == "S1":
        return verify_exS1(mod)
    elif exercise_code == "S2":
        return verify_exS2(mod)
    elif exercise_code == "S3":
        return verify_exS3(mod)
    else:
        print(f"Exercice {exercise_code!r} non connu dans le grader du chapitre 2.")
        return False


def main() -> None:
    try:
        mod = _load_notebook_as_module(NOTEBOOK_PATH)
    except Exception as e:
        print("Erreur lors du chargement du notebook :", e)
        sys.exit(1)

    results = {
        "T1": grade_t1(mod),
        "T2": grade_t2(mod),
        "D1": grade_d1(mod),
        "D2": grade_d2(mod),
        "S1": grade_s1(mod),
        "S2": grade_s2(mod),
        "S3": grade_s3(mod),
    }

    print("Résultats du grader pour les exercices (Chapitre 2) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
