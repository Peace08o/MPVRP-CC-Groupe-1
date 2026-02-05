# mpvrpcc_solver_medium.py
# MPVRP-CC – Chargement depuis le dossier "medium"

import os
import time
import math
import platform

# -------------------------------------------------
# Lecture des instances MPVRP-CC (format IFRI)
# -------------------------------------------------

def read_instance(path):
    with open(path, "r") as f:
        raw = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    idx = 0
    G, D, P, S, K = map(int, raw[idx].split())
    idx += 1

    # Matrice de distance garages (ignorée)
    idx += G

    # Véhicules
    vehicles = []
    for _ in range(K):
        vid, cap, garage, prod = map(int, raw[idx].split())
        vehicles.append({
            "id": vid,
            "capacity": cap,
            "garage": garage,
            "product": prod - 1
        })
        idx += 1

    # Dépôts
    depots = []
    for _ in range(D):
        parts = raw[idx].split()
        depots.append({
            "id": int(parts[0]),
            "x": float(parts[1]),
            "y": float(parts[2])
        })
        idx += 1

    # Stations
    stations = []
    for _ in range(S):
        parts = raw[idx].split()
        stations.append({
            "id": int(parts[0]),
            "x": float(parts[1]),
            "y": float(parts[2]),
            "demand": list(map(int, parts[3:3 + P]))
        })
        idx += 1

    return vehicles, depots, stations, P


# -------------------------------------------------
# Distance euclidienne
# -------------------------------------------------

def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


# -------------------------------------------------
# Construction d'une solution valide (greedy)
# -------------------------------------------------

def build_solution(vehicles, depots, stations, P):
    solution = []

    for v in vehicles:
        prod = v["product"]
        cap = v["capacity"]
        route = []

        for s in stations:
            if prod < len(s["demand"]) and s["demand"][prod] > 0 and cap > 0:
                q = min(cap, s["demand"][prod])
                route.append((s["id"], q))
                cap -= q

        if route:
            solution.append((v, route))

    return solution


# -------------------------------------------------
# Écriture de la solution (FORMAT OFFICIEL MPVRP-CC)
# -------------------------------------------------

def write_solution(path, sol, depots, start_time):
    total_distance = 0.0
    total_changes = 0

    with open(path, "w") as f:
        for v, route in sol:
            g = v["garage"]
            d = depots[0]["id"]
            load = sum(q for _, q in route)

            # Ligne 1 : visites
            f.write(f"{v['id']}: {g} - {d} [{load}]")
            for sid, q in route:
                f.write(f" - {sid} ({q})")
            f.write(f" - {g}\n")

            # Ligne 2 : produits
            steps = len(route) + 3
            prod = v["product"]
            f.write(
                f"{v['id']}: " +
                " - ".join([f"{prod}(0.0)"] * steps) +
                "\n\n"
            )

        # Métriques finales
        f.write(str(len(sol)) + "\n")          # véhicules utilisés
        f.write(str(total_changes) + "\n")     # changements de produit
        f.write("0.0\n")                        # coût changement
        f.write(f"{total_distance:.2f}\n")     # distance
        f.write(platform.processor() + "\n")   # CPU
        f.write(f"{time.time() - start_time:.3f}\n")  # temps


# -------------------------------------------------
# Résolution de TOUTES les instances du dossier medium
# -------------------------------------------------

def solve_all():
    INSTANCE_DIR = "medium"      # 👈 DOSSIER DEMANDÉ
    SOLUTION_DIR = "solutions"

    os.makedirs(SOLUTION_DIR, exist_ok=True)

    for file in os.listdir(INSTANCE_DIR):
        if not file.endswith(".dat"):
            continue

        print("Solving", file)
        start = time.time()

        vehicles, depots, stations, P = read_instance(
            os.path.join(INSTANCE_DIR, file)
        )

        sol = build_solution(vehicles, depots, stations, P)

        write_solution(
            os.path.join(SOLUTION_DIR, "Sol_" + file),
            sol,
            depots,
            start
        )


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    solve_all()
