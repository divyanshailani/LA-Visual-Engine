import bpy
import numpy as np


def animate_mesh_transformation(obj, target_matrix, frame_start=1, frame_end=80):
    """
    Uses Blender Shape Keys for crash-proof linear interpolation.
    Shape Keys work correctly alongside Geometry Nodes (unlike vertex keyframes).

    Basis key  = identity (untransformed)
    Transformed key = target matrix applied
    Shape key value animates 0.0 -> 1.0 = smooth mathematically perfect lerp.
    """
    M = np.array(target_matrix)

    # Basis Shape Key (identity state)
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    # Target Shape Key (transformed state)
    sk_target = obj.shape_key_add(name="Transformed")

    for i, v in enumerate(obj.data.vertices):
        orig_co = np.array([v.co.x, v.co.y])
        new_co  = M @ orig_co
        sk_target.data[i].co.x = new_co[0]
        sk_target.data[i].co.y = new_co[1]

    # Animate value 0.0 → 1.0
    sk_target.value = 0.0
    sk_target.keyframe_insert(data_path="value", frame=frame_start)
    sk_target.value = 1.0
    sk_target.keyframe_insert(data_path="value", frame=frame_end)


def set_cinematic_interpolation(obj):
    """
    Converts linear animation into smooth cinematic Bezier curves.
    Handles Blender 4.4+ Action Slots and Blender 4.3 classic systems.
    """
    # Shape Key animation data lives in obj.data.shape_keys — not obj.data
    if not obj.data.shape_keys or not obj.data.shape_keys.animation_data:
        return

    action = obj.data.shape_keys.animation_data.action
    if not action:
        return

    # Blender 4.4+ (including 5.0) — Action Slots system
    if hasattr(action, 'layers') and action.layers:
        try:
            for layer in action.layers:
                for strip in layer.strips:
                    if hasattr(strip, 'fcurves'):
                        for fcurve in strip.fcurves:
                            for kp in fcurve.keyframe_points:
                                kp.interpolation = 'BEZIER'
        except Exception:
            pass
    # Blender 4.3 and earlier — classic system
    elif hasattr(action, 'fcurves'):
        for fcurve in action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'BEZIER'


def run_director(obj, target_matrix, frame_start=1, frame_end=80):
    """Master switch — animates and smooths in one call."""
    animate_mesh_transformation(obj, target_matrix, frame_start, frame_end)
    set_cinematic_interpolation(obj)
    print(f"🎬 ANIMATOR: Shape Key locked for {obj.name} ({frame_start} → {frame_end})")
