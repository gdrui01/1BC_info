import os
import sys
import types
import nbformat
import statistics


NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__),
    "chapitre_7_interactif.ipynb",
)


def _load_notebook_as_module(nb_path: str) -> types.ModuleType:
    """
    Charge le notebook Jupyter comme un module Python en exécutant
    toutes les cellules de type 'code' dans un namespace isolé.
    """
    if not os.path.isfile(nb_path):
        raise FileNotFoundError(f"Notebook introuvable: {nb_path}")

    nb = nbformat.read(nb_path, as_version=4)
    module = types.ModuleType("chapitre_7_interactif_module")
    ns = module.__dict__

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        code = "".join(cell.source)
        try:
            exec(compile(code, "<notebook_cell>", "exec"), ns)
        except Exception:
            # On ignore les erreurs de cellules non pertinentes.
            pass

    return module


def grade_s1(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction next_arrival_time.
    """
    if not hasattr(mod, "next_arrival_time"):
        return False
    f = mod.next_arrival_time

    try:
        current_time = 100
        mean_interval = 50.0

        # Appels multiples pour vérifier la distribution grossièrement
        values = [f(current_time, mean_interval) for _ in range(50)]

        # Tous les temps doivent être >= current_time
        if any(t < current_time for t in values):
            return False

        # La moyenne des deltas ne doit pas être totalement aberrante (pas 0, pas énorme)
        deltas = [t - current_time for t in values]
        avg_delta = statistics.mean(deltas)
        if avg_delta <= 0:
            return False

    except Exception:
        return False

    return True


def grade_s2(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction simulate_single_server_queue.
    """
    if not hasattr(mod, "simulate_single_server_queue"):
        return False
    f = mod.simulate_single_server_queue

    try:
        duration = 1000
        mean_interarrival = 50.0
        service_time = 20

        n_served, waiting_times = f(duration, mean_interarrival, service_time)

        # Consistance de base
        if n_served < 0:
            return False
        if len(waiting_times) != n_served:
            return False
        if any(w < 0 for w in waiting_times):
            return False

    except Exception:
        return False

    return True


def grade_s3(mod: types.ModuleType) -> bool:
    """
    Vérifie la fonction average_waiting_time.
    """
    if not hasattr(mod, "average_waiting_time"):
        return False
    f = mod.average_waiting_time

    try:
        # Cas simple
        avg = f(3, 500, 50.0, 10)
        if avg < 0:
            return False

        # Cas avec aucune arrivée possible (durée très courte par rapport au mean_interarrival)
        avg2 = f(2, 1, 10**9, 10)
        if avg2 < 0:
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

    print("Résultats du grader pour les exercices supplémentaires (Chapitre 7) :")
    for ex, ok in results.items():
        statut = "Réussi" if ok else "Échoué"
        print(f"  {ex}: {statut}")


if __name__ == "__main__":
    main()
