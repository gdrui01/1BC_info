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


# --- nouveaux graders pour R1, Ex 3.1, Ex 3.2 ---


def grade_r1(mod: types.ModuleType) -> bool:
    """
    Exercice R1 : pgcd_iter_safe et pgcd_rec_safe
    - lève ValueError si a==0 ou b==0
    - fonctionne quel que soit l'ordre de a, b
    """
    for name in ("pgcd_iter_safe", "pgcd_rec_safe"):
        if not hasattr(mod, name):
            return False

    f_iter = getattr(mod, "pgcd_iter_safe")
    f_rec = getattr(mod, "pgcd_rec_safe")

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
            if f_iter(a, b) != expected:
                return False
            if f_rec(a, b) != expected:
                return False

        # cas d'erreur : a==0 ou b==0
        error_cases = [(0, 5), (5, 0), (0, 0)]
        for a, b in error_cases:
            for f, nm in ((f_iter, "pgcd_iter_safe"), (f_rec, "pgcd_rec_safe")):
                try:
                    f(a, b)
                    return False  # devrait lever
                except ValueError:
                    continue
                except Exception:
                    return False
    except Exception:
        return False

    return True


def grade_ex31(mod: types.ModuleType) -> bool:
    """
    Exercice 3.1 : fib_iter et fib_rec (version de base).
    On teste seulement fib_iter et fib_rec.
    """
    if not hasattr(mod, "fib_iter") or not hasattr(mod, "fib_rec"):
        return False

    f_iter = getattr(mod, "fib_iter")
    f_rec = getattr(mod, "fib_rec")

    tests = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (5, 5),
        (7, 13),
        (10, 55),
    ]

    try:
        for n, expected in tests:
            if f_iter(n) != expected:
                return False
            if f_rec(n) != expected:
                return False
    except Exception:
        return False

    return True


def grade_ex32(mod: types.ModuleType) -> bool:
    """
    Exercice 3.2 : Collatz
    - collatz_un(u0, n)
    - collatz_un_iter(u0, n)
    - collatz_temps_vol(u0)
    """
    for name in ("collatz_un", "collatz_un_iter", "collatz_temps_vol"):
        if not hasattr(mod, name):
            return False

    f_rec = getattr(mod, "collatz_un")
    f_it = getattr(mod, "collatz_un_iter")
    f_tv = getattr(mod, "collatz_temps_vol")

    # quelques tests de valeurs
    tests_un = [
        (1, 0, 1),
        (1, 1, 4),
        (2, 1, 1),   # 2 -> 1
        (3, 1, 10),  # suite classique
        (6, 2, 3),
    ]

    try:
        for u0, n, expected in tests_un:
            if f_rec(u0, n) != expected:
                return False
            if f_it(u0, n) != expected:
                return False

        # tests temps de vol connus
        # (ces valeurs sont standard pour Collatz)
        tv_tests = [
            (1, 0),
            (2, 1),
            (3, 7),
            (6, 8),
        ]
        for u0, expected_n in tv_tests:
            if f_tv(u0) != expected_n:
                return False
    except Exception:
        return False

    return True


def grade_ex33(mod: types.ModuleType) -> bool:
    """
    Exercice 3.3 — Recherche séquentielle et dichotomique.
    On teste :
      - recherche_seq_iter(L, c)
      - recherche_seq_rec(L, c, i)
      - recherche_seq_iter_toutes(L, c)
      - recherche_seq_rec_toutes(L, c, i)
      - recherche_dicho_iter(L, c)
      - recherche_dicho_rec(L, c, g, d)
    sur une petite liste.
    """
    required = [
        "recherche_seq_iter",
        "recherche_seq_rec",
        "recherche_seq_iter_toutes",
        "recherche_seq_rec_toutes",
        "recherche_dicho_iter",
        "recherche_dicho_rec",
    ]
    for name in required:
        if not hasattr(mod, name):
            return False

    seq_iter = getattr(mod, "recherche_seq_iter")
    seq_rec = getattr(mod, "recherche_seq_rec")
    seq_iter_all = getattr(mod, "recherche_seq_iter_toutes")
    seq_rec_all = getattr(mod, "recherche_seq_rec_toutes")
    dicho_iter = getattr(mod, "recherche_dicho_iter")
    dicho_rec = getattr(mod, "recherche_dicho_rec")

    # liste de test (non triée pour la séquentielle)
    L = ["a", "b", "c", "b", "d"]
    # pour la dichotomie : liste triée
    L_sorted = sorted(L)

    try:
        # séquentielle: première occurrence
        if seq_iter(L, "b") != 1:
            return False
        if seq_iter(L, "x") != -1:
            return False
        if seq_rec(L, "b", 0) != 1:
            return False
        if seq_rec(L, "x", 0) != -1:
            return False

        # séquentielle: toutes les occurrences
        if seq_iter_all(L, "b") != [1, 3]:
            return False
        if seq_iter_all(L, "x") != []:
            return False
        if seq_rec_all(L, "b", 0) != [1, 3]:
            return False
        if seq_rec_all(L, "x", 0) != []:
            return False

        # dichotomie: liste triée
        # L_sorted = ['a', 'b', 'b', 'c', 'd']
        idx_it = dicho_iter(L_sorted, "b")
        if idx_it not in (1, 2):
            return False
        idx_it_not = dicho_iter(L_sorted, "x")
        if idx_it_not != -1:
            return False

        idx_rec = dicho_rec(L_sorted, "b", 0, len(L_sorted) - 1)
        if idx_rec not in (1, 2):
            return False
        idx_rec_not = dicho_rec(L_sorted, "x", 0, len(L_sorted) - 1)
        if idx_rec_not != -1:
            return False
    except Exception:
        return False

    return True


def grade_ex34(mod: types.ModuleType) -> bool:
    """
    Exercice 3.4 — Triangle de Pascal.
    On teste uniquement pascal_r(n, k) sur quelques valeurs.
    """
    if not hasattr(mod, "pascal_r"):
        return False
    f = getattr(mod, "pascal_r")

    tests = [
        (0, 0, 1),
        (1, 0, 1),
        (1, 1, 1),
        (2, 1, 2),
        (3, 1, 3),
        (3, 2, 3),
        (4, 2, 6),
        (5, 2, 10),
    ]

    try:
        for n, k, expected in tests:
            if f(n, k) != expected:
                return False
    except Exception:
        return False

    return True


# --- wrappers de vérification pour utilisation directe ---


def verify_exS1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie S1 (somme_liste_rec).
    Si mod est None, charge le notebook chapitre_3_interactif.
    """
    print("=== Vérification Chapitre 3 - Exercice S1 ===")
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
    Vérifie S2 (inverse_chaine_rec).
    """
    print("=== Vérification Chapitre 3 - Exercice S2 ===")
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
    Vérifie S3 (pgcd_rec_ex).
    """
    print("=== Vérification Chapitre 3 - Exercice S3 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_s3(mod)
    print("Résultat S3 :", "Réussi" if ok else "Échoué")
    return ok


def verify_exR1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie R1 (pgcd_iter_safe, pgcd_rec_safe).
    """
    print("=== Vérification Chapitre 3 - Exercice R1 ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_r1(mod)
    print("Résultat R1 :", "Réussi" if ok else "Échoué")
    return ok


def verify_ex31(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie l'exercice 3.1 (Fibonacci).
    """
    print("=== Vérification Chapitre 3 - Exercice 3.1 (Fibonacci) ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_ex31(mod)
    print("Résultat 3.1 :", "Réussi" if ok else "Échoué")
    return ok


def verify_ex32(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie l'exercice 3.2 (Collatz).
    """
    print("=== Vérification Chapitre 3 - Exercice 3.2 (Collatz) ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_ex32(mod)
    print("Résultat 3.2 :", "Réussi" if ok else "Échoué")
    return ok


def verify_ex33(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie l'exercice 3.3 (recherches séquentielle et dichotomique).
    """
    print("=== Vérification Chapitre 3 - Exercice 3.3 (Recherches) ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_ex33(mod)
    print("Résultat 3.3 :", "Réussi" if ok else "Échoué")
    return ok


def verify_ex34(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie l'exercice 3.4 (Triangle de Pascal) via pascal_r.
    """
    print("=== Vérification Chapitre 3 - Exercice 3.4 (Pascal) ===")
    if mod is None:
        try:
            mod = _load_notebook_as_module(NOTEBOOK_PATH)
        except Exception as e:  # noqa: BLE001
            print("Erreur lors du chargement du notebook :", e)
            return False

    ok = grade_ex34(mod)
    print("Résultat 3.4 :", "Réussi" if ok else "Échoué")
    return ok


def run_grader_for_specific_exercise(exercise_code: str, mod: types.ModuleType | None = None) -> bool:
    """
    Dispatcher simple :
    - 'R1'  -> verify_exR1
    - '3.1' -> verify_ex31
    - '3.2' -> verify_ex32
    - '3.3' -> verify_ex33
    - '3.4' -> verify_ex34
    - 'S1'  -> verify_exS1
    - 'S2'  -> verify_exS2
    - 'S3'  -> verify_exS3
    """
    if exercise_code == "R1":
        return verify_exR1(mod)
    elif exercise_code == "3.1":
        return verify_ex31(mod)
    elif exercise_code == "3.2":
        return verify_ex32(mod)
    elif exercise_code == "3.3":
        return verify_ex33(mod)
    elif exercise_code == "3.4":
        return verify_ex34(mod)
    elif exercise_code == "S1":
        return verify_exS1(mod)
    elif exercise_code == "S2":
        return verify_exS2(mod)
    elif exercise_code == "S3":
        return verify_exS3(mod)
    else:
        print(f"Exercice {exercise_code!r} non connu dans le grader du chapitre 3.")
        return False


def main() -> None:
    try:
        mod = _load_notebook_as_module(NOTEBOOK_PATH)
    except Exception as e:
        print("Erreur lors du chargement du notebook :", e)
        sys.exit(1)

    results = {
        "R1": grade_r1(mod),
        "3.1": grade_ex31(mod),
        "3.2": grade_ex32(mod),
        "3.3": grade_ex33(mod),
        "3.4": grade_ex34(mod),
        "S1": grade_s1(mod),
        "S2": grade_s2(mod),
        "S3": grade_s3(mod),
    }

    print("Résultats du grader pour les exercices (Chapitre 3) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
