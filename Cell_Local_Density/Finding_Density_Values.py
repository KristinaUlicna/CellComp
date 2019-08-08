# Function to find density at birth, 1/4, half-way, 3/4 and just before mitosis:

import numpy as np

def FindDensitySpan(density_list, span="one_quarter"):
    """

    Args:
        density_list (list)     -> list of floats = density values for each frame for the entire lifetime of the cellID
        span (string)           -> "birth", "one_quarter", "half_way", "three_quarters", "mitosis"
                                        (=from where the density values should be averaged)
    """

    if span == "birth":
        density = density_list[0:5]
    elif span == "mitosis":
        density = density_list[-5:]
    else:
        quarter = int(len(density_list) / 4)
        if span == "one_quarter":
            quarter = quarter * 1
        if span == "half_way":
            quarter = quarter * 2
        if span == "three_quarters":
            quarter = quarter * 3
        density = density_list[quarter - 2], density_list[quarter - 1], density_list[quarter], \
                       density_list[quarter + 1], density_list[quarter + 2]

    density = [den for den in density if den != min(density)]
    density = [den for den in density if den != max(density)]
    density = np.mean(density)

    return density
