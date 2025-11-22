import types

def _print_block(title: str, lines: list, success: bool) -> bool:
    """
    Prints the title and lines, followed by a success message.
    Returns the success status.
    """
    print(f"=== {title} ===")
    for line in lines:
        print(line)
    if success:
        print("SUCCESS")
    return success


# Verification for Exercise 1
def verify_ex1(mod: types.ModuleType | None = None) -> bool:
    """
    Vérifie simplement que la fonction carre est correcte.
    Dans le notebook, l'exercice 1 est une expérimentation non notée
    (le grader ne regarde PAS le contenu de la cellule avec 'for' et 'sum').
    """
    print("=== Vérification Exercice 1 ===")
    method_name = "carre"

    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    if hasattr(mod, method_name):
        method = getattr(mod, method_name)

        tests = [(0, 0), (1, 1), (5, 25), (-3, 9)]
        ok = True
        for x, expected in tests:
            result = method(x)
            if result != expected:
                print(f"{method_name}({x}) mauvais. Attendu {expected}, obtenu {result}")
                ok = False
        if ok:
            print(f"Method {method_name} passed!")
        return ok
    else:
        print(f"{method_name} not found in the module.")
        return False


# Verification for Exercise 2
def verify_ex2(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice 2 : plus_grand, est_pair, saluer_nom.
    """
    print("=== Vérification Exercice 2 ===")
    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    ok = True
    lines: list[str] = []

    # 1) plus_grand(a, b)
    name_pg = "plus_grand"
    if hasattr(mod, name_pg):
        f = getattr(mod, name_pg)
        tests_pg = [
            (3, 7, 7),
            (7, 3, 7),
            (-1, 0, 0),
            (5, 5, 5),
        ]
        for a, b, expected in tests_pg:
            res = f(a, b)
            if res != expected:
                ok = False
                lines.append(
                    f"{name_pg}({a}, {b}) mauvais. Attendu {expected}, obtenu {res}"
                )
        if ok:
            lines.append(f"{name_pg} OK")
    else:
        ok = False
        lines.append(f"{name_pg} not found in the module.")

    # 2) est_pair(n)
    name_ep = "est_pair"
    if hasattr(mod, name_ep):
        f = getattr(mod, name_ep)
        tests_ep = [
            (0, True),
            (1, False),
            (2, True),
            (17, False),
            (-4, True),
        ]
        for n, expected in tests_ep:
            res = f(n)
            if res is not expected:
                ok = False
                lines.append(
                    f"{name_ep}({n}) mauvais. Attendu {expected}, obtenu {res}"
                )
        if ok:
            lines.append(f"{name_ep} OK")
    else:
        ok = False
        lines.append(f"{name_ep} not found in the module.")

    # 3) saluer_nom(nom) : on vérifie juste qu'elle s'exécute sans erreur
    name_sn = "saluer_nom"
    if hasattr(mod, name_sn):
        f = getattr(mod, name_sn)
        try:
            f("Alice")
            f("Bob")
            lines.append(f"{name_sn} s'exécute sans erreur (contenu non vérifié).")
        except Exception as e:  # noqa: BLE001
            ok = False
            lines.append(f"{name_sn} lève une exception : {e!r}")
    else:
        ok = False
        lines.append(f"{name_sn} not found in the module.")

    return _print_block("Exercice 2", lines, ok)


# Verification for Exercise 3
def verify_ex3(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice 3 : fact et fact_iterative avec gestion de n négatif.
    """
    print("=== Vérification Exercice 3 ===")
    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    ok = True
    lines: list[str] = []

    name_fact = "fact"
    name_fact_it = "fact_iterative"

    if not hasattr(mod, name_fact):
        ok = False
        lines.append(f"{name_fact} not found in the module.")
    if not hasattr(mod, name_fact_it):
        ok = False
        lines.append(f"{name_fact_it} not found in the module.")

    if not ok:
        return _print_block("Exercice 3", lines, ok)

    fact = getattr(mod, name_fact)
    fact_it = getattr(mod, name_fact_it)

    # tests de valeurs normales
    tests = [(0, 1), (1, 1), (5, 120), (6, 720)]
    for n, expected in tests:
        r1 = fact(n)
        r2 = fact_it(n)
        if r1 != expected:
            ok = False
            lines.append(f"{name_fact}({n}) mauvais. Attendu {expected}, obtenu {r1}")
        if r2 != expected:
            ok = False
            lines.append(
                f"{name_fact_it}({n}) mauvais. Attendu {expected}, obtenu {r2}"
            )

    # tests négatifs : on attend ValueError
    for n in (-1, -3):
        for fct, nm in ((fact, name_fact), (fact_it, name_fact_it)):
            try:
                fct(n)
                ok = False
                lines.append(f"{nm}({n}) devrait lever ValueError, mais ne le fait pas.")
            except ValueError:
                # ok
                pass
            except Exception as e:  # noqa: BLE001
                ok = False
                lines.append(
                    f"{nm}({n}) devrait lever ValueError, mais lève {type(e).__name__}."
                )

    if ok:
        lines.append("fact et fact_iterative OK")
    return _print_block("Exercice 3", lines, ok)


# Verification for Exercise 4
def verify_ex4(mod: types.ModuleType | None = None) -> bool:
    """
    Exercices réalisés en dehors du notebook : on se contente
    d'indiquer qu'aucun test automatique n'est prévu ici.
    """
    print("=== Vérification Exercice 4 ===")
    lines = [
        "Cet exercice se fait dans des fichiers externes (packages).",
        "Aucun test automatique n'est effectué dans ce grader.",
    ]
    return _print_block("Exercice 4", lines, True)


# Verification for Exercise 5
def verify_ex5(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice 5 : fonction compter_lignes_et_mots(nom_fichier)
    qui renvoie (nb_lignes, nb_mots).
    """
    print("=== Vérification Exercice 5 ===")
    import os
    import tempfile

    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "compter_lignes_et_mots"
    if not hasattr(mod, name_fn):
        print(f"{name_fn} not found in the module.")
        return False

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []

    # on crée un fichier temporaire
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.txt")
        contenu = "Bonjour tout le monde\nUne deuxième ligne\nEt   trois   mots\n"
        with open(path, "w", encoding="utf-8") as h:
            h.write(contenu)

        expected_lines = 3
        # mots : Bonjour(1) tout(2) le(3) monde(4) -> 4
        # Une(5) deuxième(6) ligne(7) -> 3
        # Et(8) trois(9) mots(10) -> 3  => 10
        expected_words = 10

        res = f(path)
        if not isinstance(res, tuple) or len(res) != 2:
            ok = False
            lines.append(
                f"{name_fn} doit renvoyer un tuple (nb_lignes, nb_mots), obtenu {res!r}"
            )
        else:
            nl, nm = res
            if nl != expected_lines or nm != expected_words:
                ok = False
                lines.append(
                    f"{name_fn} mauvais. Attendu ({expected_lines}, {expected_words}), "
                    f"obtenu ({nl}, {nm})"
                )

    if ok:
        lines.append(f"{name_fn} OK")
    return _print_block("Exercice 5", lines, ok)


# Verification for Exercise 6
def verify_ex6(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice 6 : nombre_hausses_cours(nom_fichier)
    qui renvoie le nombre de hausses de cours.
    """
    print("=== Vérification Exercice 6 ===")
    import os
    import tempfile

    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "nombre_hausses_cours"
    if not hasattr(mod, name_fn):
        print(f"{name_fn} not found in the module.")
        return False

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "cours.txt")
        # exemple de l'énoncé : 45 47 51 38 45 / 57 57 -> 4 hausses
        contenu = "45 47 51 38 45\n57 57\n"
        with open(path, "w", encoding="utf-8") as h:
            h.write(contenu)

        expected = 4
        res = f(path)
        if res != expected:
            ok = False
            lines.append(
                f"{name_fn} mauvais sur l'exemple. Attendu {expected}, obtenu {res}"
            )

        # second test
        path2 = os.path.join(tmp, "cours2.txt")
        contenu2 = "10 9 8 7\n"  # aucune hausse
        with open(path2, "w", encoding="utf-8") as h:
            h.write(contenu2)
        expected2 = 0
        res2 = f(path2)
        if res2 != expected2:
            ok = False
            lines.append(
                f"{name_fn} mauvais sur un cas sans hausse. "
                f"Attendu {expected2}, obtenu {res2}"
            )

    if ok:
        lines.append(f"{name_fn} OK")
    return _print_block("Exercice 6", lines, ok)


# Verification for Exercise 7
def verify_ex7(mod: types.ModuleType | None = None) -> bool:
    """
    Placeholder pour un éventuel exercice 7.
    Aucun test défini pour l'instant.
    """
    print("=== Vérification Exercice 7 ===")
    lines = ["Aucun test automatique défini pour l'exercice 7 dans ce grader."]
    return _print_block("Exercice 7", lines, True)


# Exercices supplémentaires S1, S2, S3
def verify_exS1(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice S1 : somme_1_a_n(n)
    """
    print("=== Vérification Exercice S1 ===")
    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "somme_1_a_n"
    if not hasattr(mod, name_fn):
        print(f"{name_fn} not found in the module.")
        return False

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []

    tests = [
        (1, 1),
        (2, 3),
        (3, 6),
        (5, 15),
        (10, 55),
    ]

    for n, expected in tests:
        res = f(n)
        if res != expected:
            ok = False
            lines.append(
                f"{name_fn}({n}) mauvais. Attendu {expected}, obtenu {res}"
            )

    if ok:
        lines.append(f"{name_fn} OK")
    return _print_block("Exercice S1", lines, ok)


def verify_exS2(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice S2 : compter_voyelles(s)
    """
    print("=== Vérification Exercice S2 ===")
    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "compter_voyelles"
    if not hasattr(mod, name_fn):
        print(f"{name_fn} not found in the module.")
        return False

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []

    tests = [
        ("", 0),
        ("Bonjour", 3),
        ("PYTHON", 1),
        ("aeiouyAEIOUY", 12),
        ("bcdfg", 0),
    ]

    for s, expected in tests:
        res = f(s)
        if res != expected:
            ok = False
            lines.append(
                f"{name_fn}({s!r}) mauvais. Attendu {expected}, obtenu {res}"
            )

    if ok:
        lines.append(f"{name_fn} OK")
    return _print_block("Exercice S2", lines, ok)


def verify_exS3(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice S3 : moyenne_fichier_entiers(nom_fichier)
    """
    print("=== Vérification Exercice S3 ===")
    import os
    import tempfile

    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "moyenne_fichier_entiers"
    if not hasattr(mod, name_fn):
        print(f"{name_fn} not found in the module.")
        return False

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "entiers.txt")
        contenu = "2\n4\n6\n"
        with open(path, "w", encoding="utf-8") as h:
            h.write(contenu)

        expected = 4.0
        res = f(path)
        if abs(res - expected) > 1e-9:
            ok = False
            lines.append(
                f"{name_fn} mauvais. Attendu {expected}, obtenu {res}"
            )

    if ok:
        lines.append(f"{name_fn} OK")
    return _print_block("Exercice S3", lines, ok)


def verify_ex8(mod: types.ModuleType | None = None) -> bool:
    """
    Exercice 8 (notes / moyennes) : dans ce grader,
    on se contente de vérifier que le code s'exécute sans erreur
    si la fonction main_ex8(module) existe dans le module étudiant.
    """
    print("=== Vérification Exercice 8 ===")
    if mod is None:
        print("Pas de module fourni pour la vérification.")
        return False

    name_fn = "main_ex8"
    if not hasattr(mod, name_fn):
        lines = [
            "Aucune fonction main_ex8 trouvée.",
            "Cet exercice repose surtout sur l'exécution manuelle du script.",
        ]
        return _print_block("Exercice 8", lines, True)

    f = getattr(mod, name_fn)
    ok = True
    lines: list[str] = []
    try:
        f()
        lines.append("main_ex8 s'exécute sans erreur.")
    except Exception as e:  # noqa: BLE001
        ok = False
        lines.append(f"main_ex8 lève une exception : {e!r}")

    return _print_block("Exercice 8", lines, ok)


# Main function to run the grader for specific exercises
def run_grader_for_specific_exercise(exercise_number: int, mod: types.ModuleType | None = None):
    """
    Call the specific exercise verification based on the exercise number.
    """
    if exercise_number == 1:
        return verify_ex1(mod)
    elif exercise_number == 2:
        return verify_ex2(mod)
    elif exercise_number == 3:
        return verify_ex3(mod)
    elif exercise_number == 4:
        return verify_ex4(mod)
    elif exercise_number == 5:
        return verify_ex5(mod)
    elif exercise_number == 6:
        return verify_ex6(mod)
    elif exercise_number == 7:
        return verify_ex7(mod)
    elif exercise_number == 51:  # S1
        return verify_exS1(mod)
    elif exercise_number == 52:  # S2
        return verify_exS2(mod)
    elif exercise_number == 53:  # S3
        return verify_exS3(mod)
    elif exercise_number == 8:
        return verify_ex8(mod)
    else:
        print(f"Exercice {exercise_number} is not implemented in the grader.")
        return False


def main():
    """
    Petit point d'entrée pratique pour lancer quelques tests de base.
    L'utilisateur peut adapter selon ses besoins.
    """
    print("Grader chapitre 1 – exemple d'utilisation.")
    print("Ce main ne connaît pas le module d'étudiant par défaut.")
    print("Importe ce grader et appelle run_grader_for_specific_exercise(ex, ton_module).")


# Entry point for running the grader for specific exercise
if __name__ == "__main__":
    # Exemple d'utilisation : à adapter si besoin.
    # On ne force pas un import de 'your_module' ici pour éviter les erreurs.
    main()
