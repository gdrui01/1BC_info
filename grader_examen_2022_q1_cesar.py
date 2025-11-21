import os
import sys
import types
import importlib.util
import tempfile
from string import ascii_uppercase

EXAM_PATH = os.path.join(
    os.path.dirname(__file__),
    "examen_2022_q1_cesar.py",
)


def _load_module(path: str) -> types.ModuleType:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier d'examen introuvable: {path}")
    spec = importlib.util.spec_from_file_location("examen_2022_q1_cesar", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def grade_encryption_dict(mod: types.ModuleType) -> bool:
    if not hasattr(mod, "encryption_dict"):
        return False
    f = mod.encryption_dict

    try:
        # shift = 3
        d3 = f(3)
        if set(d3.keys()) != set(ascii_uppercase):
            return False
        if d3["A"] != "D" or d3["X"] != "A" or d3["Y"] != "B" or d3["Z"] != "C":
            return False

        # shift = 0 -> identité
        d0 = f(0)
        for c in ascii_uppercase:
            if d0[c] != c:
                return False

        # shift négatif (-1): A -> Z, B -> A
        dneg = f(-1)
        if dneg["A"] != "Z" or dneg["B"] != "A":
            return False

    except Exception:
        return False
    return True


def grade_decode_pipeline(mod: types.ModuleType) -> bool:
    # On attend que le candidat ait implémenté _build_decryption_dict et _detect_shift_and_decode
    if not hasattr(mod, "_build_decryption_dict") or not hasattr(mod, "_detect_shift_and_decode"):
        return False

    detect = mod._detect_shift_and_decode

    # On fabrique un petit cypher.txt artificiel:
    # texte clair simple: "EEEABZ"
    # shift = 3 => texte chiffré: "HHHDEF"
    plain = "EEEABZ\nAUTRE LIGNE!\n"
    shift = 3

    # utiliser encryption_dict pour coder
    enc = mod.encryption_dict(shift)
    cypher_lines = []
    for line in plain.splitlines(True):
        out = []
        for ch in line:
            if ch in ascii_uppercase:
                out.append(enc[ch])
            else:
                out.append(ch)
        cypher_lines.append("".join(out))
    cypher_text = "".join(cypher_lines)

    # crée fichiers temporaires
    cypher_fd, cypher_path = tempfile.mkstemp(text=True)
    plain_fd, plain_path = tempfile.mkstemp(text=True)
    os.close(cypher_fd)
    os.close(plain_fd)

    try:
        with open(cypher_path, "w", encoding="utf-8") as f:
            f.write(cypher_text)

        # appel de la fonction de décodage de l'étudiant
        detect(cypher_path, plain_path)

        with open(plain_path, "r", encoding="utf-8") as f:
            decoded = f.read()

        # On tolère des fins de ligne identiques, on compare la chaîne brute
        if decoded != plain:
            return False

    except Exception:
        return False
    finally:
        try:
            os.remove(cypher_path)
            os.remove(plain_path)
        except OSError:
            pass

    return True


def main() -> None:
    try:
        mod = _load_module(EXAM_PATH)
    except Exception as e:
        print("Erreur lors du chargement du fichier d'examen:", e)
        sys.exit(1)

    results = {
        "Q1_encryption_dict": grade_encryption_dict(mod),
        "Q1_decode_pipeline": grade_decode_pipeline(mod),
    }

    print("Résultats du grader — Examen 2022, Question 1 (Code de César) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
