import math
import matplotlib.pyplot as plt

# ---------- lookup tables ----------
SILICATE_CRATERS = [
    (0.8, "Earth", "Meteor Crater (Barringer)"),
    (10, "Moon", "Tycho"),
    (93, "Moon", "Copernicus"),
    (180, "Earth", "Chicxulub"),
    (2500, "Moon", "South Pole-Aitken basin"),
]

CARBONATE_CRATERS = [
    (1.2, "Earth", "Wolfe Creek"),
    (26, "Earth", "Ries"),
    (180, "Earth", "Chicxulub (carbonate target)"),
]

ICE_CRATERS = [
    (0.1, "Earth", "pitted cones on Mars"),
    (5, "Mars", "Korolev crater"),
    (20, "Mars", "north polar layered deposits"),
]

# ---------- core calculation ----------
def compute_melt_volume(D, target_type, uncertainty=False):
    """
    Returns dict with:
        'value': M in km³,
        'logM': log10(M),
        'sigma': standard deviation (log10 units),
        'bounds': {'low': low, 'high': high} if uncertainty else None,
        'warning': string or None.
    """
    # Map dropdown labels to internal keys
    type_map = {
        "Silicate (e.g. lunar highlands, martian crust)": "silicate",
        "Carbonate-rich (e.g. sedimentary basins)": "carbonate",
        "Ice/Snow (e.g. polar caps)": "ice",
    }
    key = type_map[target_type]

    # Parameters: (intercept, slope, sigma)
    params = {
        "silicate": (0.253, 2.764, 0.2),
        "carbonate": (-0.663, 3.194, 0.25),
        "ice": (-1.040, 3.500, 0.3),
    }
    intercept, slope, sigma = params[key]

    logD = math.log10(D)
    logM = intercept + slope * logD
    M = 10 ** logM

    # Sanity check: M should not exceed excavated volume ~0.3*D³
    warning = None
    if M > 0.3 * D ** 3:
        warning = (
            f"Estimated melt volume ({M:.2f} km³) exceeds the typical "
            f"excavated volume of the crater ({0.3 * D**3:.2f} km³). "
            "Result may be physically unrealistic."
        )

    result = {
        "value": M,
        "logM": logM,
        "sigma": sigma,
        "warning": warning,
        "bounds": None,
    }

    if uncertainty:
        low = 10 ** (logM - sigma)
        high = 10 ** (logM + sigma)
        result["bounds"] = {"low": low, "high": high}

    return result

# ---------- classification ----------
def classify_melt_volume(M):
    if M < 0.1:
        return "Miniscule (<0.1 km³)"
    elif M < 10:
        return "Small (0.1–10 km³)"
    elif M < 1000:
        return "Moderate (10–1000 km³)"
    elif M < 1e5:
        return "Large (1000–10⁵ km³)"
    else:
        return "Basin-scale (>10⁵ km³)"

# ---------- reference sentence ----------
def generate_reference_sentence(M, D, target_type):
    type_map = {
        "Silicate (e.g. lunar highlands, martian crust)": SILICATE_CRATERS,
        "Carbonate-rich (e.g. sedimentary basins)": CARBONATE_CRATERS,
        "Ice/Snow (e.g. polar caps)": ICE_CRATERS,
    }
    craters = type_map[target_type]

    # find closest crater diameter
    best_d, best_body, best_name = min(craters, key=lambda x: abs(x[0] - D))

    return (
        f"This melt volume is comparable to the impact that formed "
        f"{best_name} on {best_body} (diameter ~{best_d} km)."
    )

# ---------- bar chart ----------
def generate_bar_chart(M, D, target_type):
    # Compute typical melt volumes for a reference diameter on each body
    # Use same target type formula, but the bodies are usually silicate.
    # To keep consistent, we use the formula for the given target_type.
    # This gives a fair comparison of scale.
    typical_diameters = {
        "Moon": 10.0,
        "Earth": 20.0,
        "Mars": 10.0,
    }

    type_params = {
        "Silicate (e.g. lunar highlands, martian crust)": (0.253, 2.764),
        "Carbonate-rich (e.g. sedimentary basins)": (-0.663, 3.194),
        "Ice/Snow (e.g. polar caps)": (-1.040, 3.500),
    }
    intercept, slope = type_params[target_type]

    def M_typical(body_d):
        return 10 ** (intercept + slope * math.log10(body_d))

    values = [M]
    labels = ["Our Estimate"]
    for body, d in typical_diameters.items():
        values.append(M_typical(d))
        labels.append(f"{body} ({d} km)")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(labels, values, color=["#00bfff", "#ff9999", "#66b3ff", "#99ff99"])
    ax.set_xscale("log")
    ax.set_xlabel("Melt Volume (km³)")
    ax.set_title("Impact Melt Volume Comparison")
    plt.tight_layout()
    return fig
