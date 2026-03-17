import bpy
import sys
import importlib
import os

# ── 1. DIMENSIONAL BRIDGE ────────────────────────────────
path_phase2 = "/Users/divyanshailani/Desktop/project_1/Phase_2 Blender"
path_phase1 = "/Users/divyanshailani/Desktop/project_1/Phase_1 Logic"

if path_phase2 not in sys.path:
    sys.path.append(path_phase2)
if path_phase1 not in sys.path:
    sys.path.append(path_phase1)

# ── 2. IMPORT ENGINE ─────────────────────────────────────
from utils import materials, scene_builder, animator
import matrices

importlib.reload(materials)
importlib.reload(scene_builder)
importlib.reload(animator)
importlib.reload(matrices)

# ── 3. MISSION CONTROL ───────────────────────────────────
# Change PRESET_NAME to render any transformation:
# "identity" | "rotation_90" | "shear" | "scale2x"
# "reflection_x" | "projection_x" | "det_0_collapse" | "det_neg_flip"

PRESET_NAME = "shear"
FRAME_START = 1
FRAME_END   = 180
GRID_SIZE   = 5

print(f"\n🚀 INITIATING SIMULATION: {PRESET_NAME.upper()}")

# ── 4. EXECUTION SEQUENCE ────────────────────────────────
scene_builder.clear_scene()
scene_builder.setup_world_lighting()

target_m = matrices.presets[PRESET_NAME]

mat_i, mat_j, mat_grid = materials.setup_all_materials()

grid_obj = scene_builder.build_grid(mat_grid, size=GRID_SIZE)
i_arrow  = scene_builder.build_arrow("i_hat", mat_i, tip_coord=(1.0, 0.0, 0.0))
j_arrow  = scene_builder.build_arrow("j_hat", mat_j, tip_coord=(0.0, 1.0, 0.0))
camera   = scene_builder.setup_camera()

animator.run_director(grid_obj, target_m, FRAME_START, FRAME_END)
animator.run_director(i_arrow,  target_m, FRAME_START, FRAME_END)
animator.run_director(j_arrow,  target_m, FRAME_START, FRAME_END)

bpy.context.scene.frame_end = FRAME_END + 20

print("🌌 SYSTEM ONLINE: Simulation Constructed and Keyframed.")

# ── 5. CINEMATOGRAPHER'S EXPORT ──────────────────────────
desktop_path = os.path.join(
    os.path.expanduser("~"), "Desktop", f"Project_01_{PRESET_NAME}.mp4"
)
bpy.context.scene.render.filepath = desktop_path

# Blender 5.0 uses media_type; earlier versions use file_format + FFMPEG
if hasattr(bpy.context.scene.render.image_settings, 'media_type'):
    bpy.context.scene.render.image_settings.media_type = 'VIDEO'
else:
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec  = 'H264'

bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.fps = 60

print(f"🎥 EXPORT READY → {desktop_path}")
print("Go to: Render → Render Animation  (or Ctrl+F12)")
