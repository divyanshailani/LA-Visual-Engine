import numpy as np

# ─────────────────────────────────────────────────────────
# Math Utilities
# Project 01 · Phase 1 Logic · The Architect
# Divyansh Ailani · 2026
# ─────────────────────────────────────────────────────────

# 1. Composition — apply m1 first, then m2
def compose(m1, m2):
    """Applies m1 first, then m2. Right-to-left rule in Linear Algebra."""
    return m2 @ m1

# 2. Lerp — Linear Interpolation for smooth animation
def lerp_matrix(I, M, t):
    """Interpolates from identity (I) to target matrix (M). t: 0.0 to 1.0."""
    return (1 - t) * I + t * M

# 3. Determinant Status — predicts space behavior
def det_status(M):
    """Checks the determinant of M to predict space behavior."""
    det = np.linalg.det(M)
    if np.isclose(det, 0):
        return "Space collapsed to a Lower Dimension!"
    elif det < 0:
        return "Space flipped (orientation reversed)!"
    else:
        return f"Area scaled by {det:.2f}"

# 4. Composition Proof — det(M2 @ M1) = det(M2) * det(M1)
def verify_composition_det(m1, m2):
    """
    Proves: det(M2 @ M1) = det(M2) * det(M1)
    One of the most important determinant properties.
    """
    composed     = compose(m1, m2)
    det_composed = np.linalg.det(composed)
    det_product  = np.linalg.det(m1) * np.linalg.det(m2)

    print(f"det(M2 @ M1)      = {det_composed:.4f}")
    print(f"det(M2) x det(M1) = {det_product:.4f}")
    print(f"Match: {np.isclose(det_composed, det_product)}")  # always True
    return det_composed, det_product
