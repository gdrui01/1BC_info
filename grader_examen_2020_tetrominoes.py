import os
import sys
import types
import importlib.util


EXAM_PATH = os.path.join(
    os.path.dirname(__file__),
    "examen_2020_tetrominoes.py",
)


def _load_module(path: str) -> types.ModuleType:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier d'examen introuvable: {path}")
    spec = importlib.util.spec_from_file_location("examen_2020_tetrominoes", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def grade_dicts(mod: types.ModuleType) -> bool:
    """
    Vérifie que COLORS et SHAPES contiennent au moins les 7 clés
    et que SHAPES['I'] correspond à [[1,1,1,1]], etc.
    """
    required_kinds = {"I", "O", "T", "L", "J", "S", "Z"}
    if not hasattr(mod, "COLORS") or not hasattr(mod, "SHAPES"):
        return False
    COLORS = mod.COLORS
    SHAPES = mod.SHAPES

    try:
        if set(COLORS.keys()) != required_kinds:
            return False
        if set(SHAPES.keys()) != required_kinds:
            return False

        # vérifications minimales sur la forme des matrices
        if SHAPES["I"] != [[1, 1, 1, 1]]:
            return False
        if SHAPES["O"] != [[1, 1], [1, 1]]:
            return False
    except Exception:
        return False
    return True


def grade_tetromino_basic(mod: types.ModuleType) -> bool:
    """
    Vérifie __post_init__, get_cells, move, rotate pour quelques types.
    """
    if not hasattr(mod, "Tetromino"):
        return False
    Tetromino = mod.Tetromino

    try:
        # Test I horizontal à (0,0)
        t = Tetromino("I", 0, 0)
        cells = set(t.get_cells())
        expected = {(0, 0), (1, 0), (2, 0), (3, 0)}
        if cells != expected:
            return False

        # move
        t.move(2, 1)
        cells2 = set(t.get_cells())
        expected2 = {(2, 1), (3, 1), (4, 1), (5, 1)}
        if cells2 != expected2:
            return False

        # rotate (I vertical)
        t.rotate()
        cells3 = set(t.get_cells())
        # t.shape devrait maintenant être 4x1, donc les cellules forment une colonne
        ys = {cy for (_, cy) in cells3}
        xs = {cx for (cx, _) in cells3}
        if len(xs) != 1 or len(ys) != 4:
            return False

        # Test T à une position donnée
        t2 = Tetromino("T", 2, 1)
        cells_t = set(t2.get_cells())
        # shape T: [[1,1,1],[0,1,0]]
        exp_t = {(2, 1), (3, 1), (4, 1), (3, 2)}
        if cells_t != exp_t:
            return False

    except Exception:
        return False
    return True


def grade_tetrominoes_list(mod: types.ModuleType) -> bool:
    """
    Vérifie la structure de TetrominoesList:
    - init counts,
    - add / remove,
    - get_item_containing.
    """
    if not hasattr(mod, "TetrominoesList") or not hasattr(mod, "Tetromino"):
        return False
    Tetromino = mod.Tetromino
    TetrominoesList = mod.TetrominoesList

    try:
        tl = TetrominoesList()
        if not isinstance(tl.items, list):
            return False
        if tl.selected_item is not None:
            return False
        # counts doit contenir 7 clés
        if set(tl.counts.keys()) != {"I", "O", "T", "L", "J", "S", "Z"}:
            return False
        if any(v != 0 for v in tl.counts.values()):
            return False

        # add
        t = Tetromino("O", 0, 0)
        tl.add(t)
        if tl.selected_item is not t:
            return False
        if t not in tl.items:
            return False
        if tl.counts["O"] != 1:
            return False

        # get_item_containing
        got = tl.get_item_containing(0, 0)
        if got is not t:
            return False
        if tl.selected_item is not t:
            return False

        # remove
        tl.remove(t)
        if t in tl.items:
            return False
        # selected_item doit être None après suppression
        if tl.selected_item is not None:
            return False
        if tl.counts["O"] != 0:
            return False

    except Exception:
        return False
    return True


def grade_check_puzzle(mod: types.ModuleType) -> bool:
    """
    Vérifie grossièrement check_puzzle sur un cas simplifié:
    - on construit une TetrominoesList avec 2 'I' couvrant un rectangle 4x2,
      et une implémentation de check_puzzle doit reconnaître ce cas comme "correct"
      si elle part d'un expected cohérent noirci pour ce test.
    Comme l'énoncé complet vise un rectangle 8x7, ici on teste surtout la logique:
    - counts == 2
    - ensemble des cellules égal à expected.
    """
    if not hasattr(mod, "check_puzzle") or not hasattr(mod, "TetrominoesList"):
        return False
    check_puzzle = mod.check_puzzle
    Tetromino = mod.Tetromino
    TetrominoesList = mod.TetrominoesList

    try:
        tl = TetrominoesList()
        # on suppose que l'étudiant utilisera expected basé sur 8x7,
        # le grader ne peut pas deviner la convention exacte ici.
        # On va seulement vérifier que la fonction ne plante pas et
        # retourne un booléen pour un état de tlist quelconque.
        t1 = Tetromino("I", 0, 0)
        t2 = Tetromino("I", 0, 1)
        tl.add(t1)
        tl.add(t2)

        ok = check_puzzle(tl)
        if not isinstance(ok, bool):
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
        "DICT": grade_dicts(mod),
        "Tetromino": grade_tetromino_basic(mod),
        "TetrominoesList": grade_tetrominoes_list(mod),
        "check_puzzle": grade_check_puzzle(mod),
    }

    print("Résultats du grader — Examen 2020 Tetrominoes :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
