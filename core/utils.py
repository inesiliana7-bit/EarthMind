# ==========================================================
# EarthMind
# Utilities
# ==========================================================

from core.encoders import *

# ==========================================================
# Generic Encoder
# ==========================================================

def encode(value, mapping):
    """
    Convert a categorical value into its numerical score.
    """

    return mapping.get(value, 50)


# ==========================================================
# Clamp Value
# ==========================================================

def clamp(value, minimum=0, maximum=100):
    """
    Keep any value inside the range [minimum, maximum].
    """

    return max(minimum, min(maximum, value))


# ==========================================================
# Normalize Value
# ==========================================================

def normalize(value, old_min, old_max, new_min=0, new_max=100):
    """
    Convert a value from one range to another.
    """

    if old_max == old_min:
        return new_min

    return (
        (value - old_min)
        /
        (old_max - old_min)
    ) * (new_max - new_min) + new_min