import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

def visualize_environment_animated(env, ax1, ax2):
    # --- Prepare World Grid with green background ---
    grid = np.full((env.size, env.size), 0)
    for obs in env.obstacles:
        grid[obs.pos] = 1
    for flower in env.flowers:
        grid[flower.pos] = 1 + flower.nectar  # 2,3,4,5
    grid[env.hive.position] = 6

    # Custom colormap for world with distinct colors
    cmap = mcolors.ListedColormap([
        '#90ee90',   # 0: normal (green)
        '#8B4513',   # 1: obstacle (brown)
        '#ffe066',   # 2: flower (1) - bright yellow
        '#ffb347',   # 3: flower (2) - orange
        '#cd5c5c',   # 4: flower (3) - red
        '#e0e0e0',   # 5: empty flower - pale gray
        '#8ecae6',   # 6: hive - light blue
    ])

    bee_state_color = {
        "in_hive": "#000000",      # black
        "searching": "#FFFF00",    # yellow
        "gathering": "#00FF00",    # green
        "returning": "#1E90FF",    # blue
        "resting": "#FF0000",      # red
        "holding": "#800080",      # purple
    }

    # --- Bee positions and colors for plotting ---
    bee_positions = []
    bee_colors = []
    in_hive_present = False
    for bee in env.bees:
        if bee.in_hive:
            in_hive_present = True
        else:
            bee_positions.append(bee.position)
            bee_colors.append(bee_state_color.get(bee.state, "#000000"))
    fig = plt.gcf() # Get current figure  
    fig.suptitle(f'Bee World Simulation - Time Step {env.time + 1}', fontsize=16, fontweight='bold')
    # --- World subplot ---
    ax1.clear()
    ax1.imshow(grid.T, origin="lower", cmap=cmap, vmin=0, vmax=6)
    # Plot all bees not in hive
    if bee_positions:
        xs, ys = zip(*bee_positions)
        ax1.scatter(xs, ys, c=bee_colors, s=60, edgecolors='k', zorder=3, alpha=0.85)
    # Plot a single black dot at the hive if any bee is in the hive
    hive_x, hive_y = env.hive.position
    if in_hive_present:
        ax1.scatter([hive_x], [hive_y], marker="o", c="#000000", s=60, edgecolors='k', zorder=5)
    # Hive as a filled circle, no border, no square
    ax1.scatter([hive_x], [hive_y], marker="o", c="#8ecae6", s=200, edgecolors='none', zorder=4)
    ax1.set_xlim(-0.5, env.size - 0.5)
    ax1.set_ylim(-0.5, env.size - 0.5)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("Bee World Simulation")

    ax1.set_xticks(np.arange(-0.5, env.size, 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, env.size, 1), minor=True)
    ax1.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)

    # --- Bee mission legend (circles) OUTSIDE on RIGHT, at top ---
    bee_legend_circles = [
        Line2D([0], [0], marker='o', color='w', label='In Hive', markerfacecolor=bee_state_color["in_hive"], markeredgecolor='k', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Searching', markerfacecolor=bee_state_color["searching"], markeredgecolor='k', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Collecting', markerfacecolor=bee_state_color["gathering"], markeredgecolor='k', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Returning', markerfacecolor=bee_state_color["returning"], markeredgecolor='k', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Resting', markerfacecolor=bee_state_color["resting"], markeredgecolor='k', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Holding', markerfacecolor=bee_state_color["holding"], markeredgecolor='k', markersize=10),
    ]
    circle_legend = ax1.legend(handles=bee_legend_circles, loc='upper left', bbox_to_anchor=(1.02, 1), ncol=1, frameon=False, borderaxespad=0.)
    ax1.add_artist(circle_legend)

    # --- Terrain/flower legend (patches) OUTSIDE on RIGHT, below circles ---
    terrain_legend = [
        mpatches.Patch(color='#8B4513', label="NoFly"),
        mpatches.Patch(color='#cd5c5c', label="Flower (3)"),
        mpatches.Patch(color='#ffb347', label="Flower (2)"),
        mpatches.Patch(color='#ffe066', label="Flower (1)"),
        mpatches.Patch(color='#e0e0e0', label="Empty Flower"),
        mpatches.Patch(color='#8ecae6', label="Hive"),
        mpatches.Patch(color='#90ee90', label="Normal"),
    ]
    patch_legend = ax1.legend(handles=terrain_legend, loc='upper left', bbox_to_anchor=(1.22, 0.6), ncol=1, frameon=False, borderaxespad=0.)

    # --- Hive Interior subplot ---
    n_bees_in_hive = sum(bee.in_hive for bee in env.bees)
    hive_dim = int(np.ceil(np.sqrt(env.hive.max_capacity)))
    hive_grid = np.zeros((hive_dim, hive_dim), dtype=int)
    all_cells = [(i, j) for i in range(hive_dim) for j in range(hive_dim)]
    np.random.shuffle(all_cells)
    for idx in range(n_bees_in_hive):
        i, j = all_cells[idx]
        hive_grid[i, j] = 1

    honey_color = "#FFF8DC"
    bee_color = "#FFD700"
    hive_rgb_grid = np.full((hive_dim, hive_dim, 3), mcolors.to_rgb(honey_color))
    for i in range(hive_dim):
        for j in range(hive_dim):
            if hive_grid[i, j] == 1:
                hive_rgb_grid[i, j] = mcolors.to_rgb(bee_color)

    ax2.clear()
    ax2.imshow(hive_rgb_grid, origin="lower")
    ax2.set_title(f"Hive Interior - Bees: {n_bees_in_hive}")
    ax2.set_xticks(np.arange(-0.5, hive_dim, 1), minor=True)
    ax2.set_yticks(np.arange(-0.5, hive_dim, 1), minor=True)
    ax2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
    ax2.set_xticks([])
    ax2.set_yticks([])

    bee_patch = mpatches.Patch(facecolor=bee_color, edgecolor='black', label='Bee')
    empty_patch = mpatches.Patch(facecolor=honey_color, edgecolor='black', label='Empty')
    ax2.legend(handles=[empty_patch, bee_patch], loc='upper right', bbox_to_anchor=(1, 1), frameon=False)

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)

