import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matrices import identity, presets
from math_utils import lerp_matrix, det_status

# ─────────────────────────────────────────────────────────
# CLI Interface — Choose transformation preset
# ─────────────────────────────────────────────────────────
print("🟢 System Online: Available presets")
for key in presets.keys():
    print(f" -> {key}")

choice = input("\n Enter transformation to simulate (e.g: shear, rotation_90): ")
if choice not in presets:
    print("☣️  Unknown preset! Defaulting to 'shear'")
    choice = "shear"

target_matrix = presets[choice]

# ─────────────────────────────────────────────────────────
# Matplotlib Canvas — Dark void aesthetic
# ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor('#07070e')
ax.set_facecolor('#07070e')

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.axhline(0, color='#333333', linewidth=1)
ax.axvline(0, color='#333333', linewidth=1)
ax.tick_params(colors='gray')
for spine in ax.spines.values():
    spine.set_edgecolor('#333333')

# ─────────────────────────────────────────────────────────
# Grid + Basis Vectors
# ─────────────────────────────────────────────────────────
x_vals = np.arange(-3, 4, 0.5)
y_vals = np.arange(-3, 4, 0.5)
x, y = np.meshgrid(x_vals, y_vals)
points = np.vstack([x.ravel(), y.ravel()])

grid_scatter, = ax.plot([], [], 'o', color='#00ffc8', markersize=2, alpha=0.5)
i_line, = ax.plot([], [], color='#f87171', linewidth=3, label='i-hat (1,0)')
j_line, = ax.plot([], [], color='#4ade80', linewidth=3, label='j-hat (0,1)')
plt.legend(loc='upper left', facecolor='#07070e', edgecolor='#333333', labelcolor='white')

# ─────────────────────────────────────────────────────────
# Animation — lerp from identity to target over 120 frames
# ─────────────────────────────────────────────────────────
frames = 120

def init():
    grid_scatter.set_data([], [])
    i_line.set_data([], [])
    j_line.set_data([], [])
    return grid_scatter, i_line, j_line

def update(frame):
    t = frame / (frames - 1)
    current_m = lerp_matrix(identity, target_matrix, t)

    transformed_points = current_m @ points
    grid_scatter.set_data(transformed_points[0, :], transformed_points[1, :])

    i_vec = current_m @ np.array([1, 0])
    j_vec = current_m @ np.array([0, 1])
    i_line.set_data([0, i_vec[0]], [0, i_vec[1]])
    j_line.set_data([0, j_vec[0]], [0, j_vec[1]])

    status = det_status(current_m)
    ax.set_title(f"Simulation: {choice.upper()} | t = {t:.2f}\n{status}",
                 color='white', pad=15)

    return grid_scatter, i_line, j_line

print("🚀 Booting Visualizer...")
ani = animation.FuncAnimation(fig, update, frames=frames,
                               init_func=init, blit=True, interval=16)
plt.show()
