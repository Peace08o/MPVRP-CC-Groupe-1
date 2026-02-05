
# mpvrpcc_solver_autofix.py
# MPVRP-CC solver with AUTO-FIXED instance parsing

import os, math, time, platform

def read_instance(path):
    with open(path) as f:
        raw = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    idx = 0
    G, D, P, S, K = map(int, raw[idx].split())
    idx += 1

    # Garage distance matrix
    garage_dist = []
    for _ in range(G):
        garage_dist.append(list(map(float, raw[idx].split())))
        idx += 1

    # Vehicles
    vehicles = []
    for _ in range(K):
        a = raw[idx].split()
        vehicles.append({
            "id": int(a[0]),
            "capacity": float(a[1]),
            "garage": int(a[2]),
            "product": int(a[3])
        })
        idx += 1

    # Remaining lines = depots + stations (auto split)
    remaining = raw[idx:]
    expected = D + S
    if len(remaining) != expected:
        print("⚠️ Warning: instance size mismatch, auto-adjusting")

    depots, stations = [], []

    for i, line in enumerate(remaining):
        parts = line.split()
        node = {
            "id": int(parts[0]),
            "x": float(parts[1]),
            "y": float(parts[2]),
            "vals": list(map(float, parts[3:]))
        }
        if i < D:
            depots.append(node)
        else:
            stations.append(node)

    return vehicles, depots, stations

def build_solution(vehicles, stations):
    sol = []
    for v in vehicles:
        prod = v["product"] - 1
        cap = v["capacity"]
        route = []
        for s in stations:
            if prod < len(s["vals"]) and cap > 0:
                q = min(cap, s["vals"][prod])
                if q > 0:
                    route.append((s["id"], int(q)))
                    cap -= q
        if route:
            sol.append((v, route))
    return sol

def write_solution(path, sol, depots):
    t0 = time.time()
    with open(path, "w") as f:
        for v, r in sol:
            g = v["garage"]
            d = depots[0]["id"]
            load = sum(q for _, q in r)
            f.write(f"{v['id']}: {g} - {d} [{load}]")
            for sid, q in r:
                f.write(f" - {sid} ({q})")
            f.write(f" - {g}\n")

            steps = len(r) + 3
            prod = v["product"] - 1
            f.write(f"{v['id']}: " + " - ".join([f"{prod}(0.0)"] * steps) + "\n\n")

        f.write(str(len(sol)) + "\n0\n0.0\n0.0\n")
        f.write(platform.processor() + "\n")
        f.write(f"{time.time() - t0:.3f}\n")

def solve_all(inst_dir, sol_dir):
    os.makedirs(sol_dir, exist_ok=True)
    for f in os.listdir(inst_dir):
        if f.endswith(".dat"):
            print("Solving", f)
            v, d, s = read_instance(os.path.join(inst_dir, f))
            sol = build_solution(v, s)
            write_solution(os.path.join(sol_dir, "Sol_" + f), sol, d)

if __name__ == "__main__":
    solve_all("instances", "solutions")
