import numpy as np

# ─────────────────────────────────────────────────────────
# All 8 Transformation Matrices
# Project 01 · Phase 1 Logic · The Architect
# Divyansh Ailani · 2026
# ─────────────────────────────────────────────────────────

identity       = np.array([[1,  0], [0,  1]], dtype=float)   # Det =  1
rotation_90    = np.array([[0, -1], [1,  0]], dtype=float)   # Det =  1  (area preserved)
shear          = np.array([[1,  1], [0,  1]], dtype=float)   # Det =  1  (area preserved)
scale2x        = np.array([[2,  0], [0,  2]], dtype=float)   # Det =  4  (area x4)
reflection_x   = np.array([[1,  0], [0, -1]], dtype=float)   # Det = -1  (orientation flips)
projection_x   = np.array([[1,  0], [0,  0]], dtype=float)   # Det =  0  (collapse)
det_0_collapse = np.array([[1,  2], [0.5, 1]], dtype=float)  # Det =  0  (collapse)
det_neg_flip   = np.array([[-1, 0], [0,  1]], dtype=float)   # Det = -1  (flip)

presets = {
    "identity":       identity,
    "rotation_90":    rotation_90,
    "shear":          shear,
    "scale2x":        scale2x,
    "reflection_x":   reflection_x,
    "projection_x":   projection_x,
    "det_0_collapse": det_0_collapse,
    "det_neg_flip":   det_neg_flip,
}

def get_preset(name):
    """Returns Transformation Matrix for a given preset name."""
    if name not in presets:
        raise ValueError(f"Unknown preset '{name}'. Available: {list(presets.keys())}")
    return presets[name]
