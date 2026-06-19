#!/usr/bin/env python3

import argparse
import time
from models.environment import Environment
from utils.config_loader import load_terrain_csv, load_params_csv
from utils.visuals import visualize_environment_animated

def interactive_setup():
    print("Interactive Mode: Enter simulation settings.")
    area_size = int(input("Property size (e.g., 20 for 20x20): "))
    bee_count = int(input("Number of bees: "))
    flower_count = int(input("Number of flowers: "))
    obstacle_count = int(input("Number of obstacles: "))
    steps = int(input("Number of simulation steps: "))
    comm_type = input("Bee communication strategy (random/directed): ").strip().lower()
    return {
        "area_size": area_size,
        "bee_count": bee_count,
        "flower_count": flower_count,
        "obstacle_count": obstacle_count,
        "steps": steps,
        "communication": comm_type
    }

def batch_setup(terrain_file, params_file):
    terrain = load_terrain_csv(terrain_file)
    params = load_params_csv(params_file)
    config = {
        "area_size": terrain.shape[0],
        "bee_count": params.get("bee_count", 10),
        "flower_count": params.get("flower_count", 10),
        "obstacle_count": params.get("obstacle_count", 3),
        "steps": params.get("steps", 20),
        "communication": params.get("communication", "random"),
        "terrain": terrain
    }
    return config

def print_bee_status_summary(env):
    bees = env.bees
    hive = env.hive
    mission_counts = {"searching": 0, "gathering": 0, "returning": 0, "resting": 0, "holding": 0, "in_hive": 0}
    in_hive = 0
    for bee in bees:
        if bee.in_hive:
            in_hive += 1
        if bee.state in mission_counts:
            mission_counts[bee.state] += 1
        else:
            mission_counts[bee.state] = 1  # Safety

    print(f"Hive nectar levels: {hive.honey_level} of {hive.max_capacity}")
    print(f"Bees in hive: {in_hive}")
    print("Bee missions: Searching={}, Collecting={}, Returning={}, Resting={}, Holding={}, In_Hive={}".format(
        mission_counts["searching"], mission_counts["gathering"], mission_counts["returning"],
        mission_counts["resting"], mission_counts["holding"], mission_counts["in_hive"]
    ))

    # Flower nectar levels
    nectar_levels = [0, 0, 0, 0]  # Empty, Level 1, Level 2, Level 3
    for flower in env.flowers:
        if flower.nectar == 0:
            nectar_levels[0] += 1
        elif flower.nectar == 1:
            nectar_levels[1] += 1
        elif flower.nectar == 2:
            nectar_levels[2] += 1
        elif flower.nectar == 3:
            nectar_levels[3] += 1
    print(f"Flowers nectar levels: Empty={nectar_levels[0]}, Level1={nectar_levels[1]}, Level2={nectar_levels[2]}, Level3={nectar_levels[3]}")

    print(f"Hive knows: {len(hive.get_flower_locations())} flower locations")
    print(f"Active signals: {len(hive.signals)}")

def main():
    print("Bee World simulation started.")
    parser = argparse.ArgumentParser(description="BeeWorld Simulation (Postgraduate)")
    parser.add_argument('-i', action='store_true', help='Interactive mode')
    parser.add_argument('-f', type=str, help='map1 csv file')
    parser.add_argument('-p', type=str, help='params1 csv file')
    args = parser.parse_args()

    if args.i:
        config = interactive_setup()
    elif args.f and args.p:
        config = batch_setup(args.f, args.p)
    else:
        print("Usage: python3 beeworld.py -i")
        print("   or: python3 beeworld.py -f map1.csv -p params1.csv")
        return

    env = Environment(**config)
    env.initialize()
    print(f"World size: {env.size}x{env.size}\n- Bees: {env.bee_count}\n- Flowers: {env.flower_count}\n- Obstacles: {env.obstacle_count}\n- Hive size: {env.hive.max_capacity}x{env.hive.max_capacity}\n")
    print(f"Steps: {env.steps}\n")

    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    plt.ion()
    for t in range(env.steps):
        print(f"Step {t+1} of {env.steps}")
        print_bee_status_summary(env)
        visualize_environment_animated(env, ax1, ax2)
        fig.canvas.draw()
        plt.pause(1)
        env.update()
        print()  # Blank line for readability

    plt.ioff()
    plt.show()
    print("Simulation Done!")
    print(f"Final hive nectar: {env.hive.honey_level}")
    print_bee_status_summary(env)

if __name__ == "__main__":
    main()

