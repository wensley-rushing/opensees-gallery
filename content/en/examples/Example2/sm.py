# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
# 
# ===----------------------------------------------------------------------===//
#
import numpy as np

import xara
import xara.units.fks as units
from xara.units.fks import kip, ksi

from xsection.library import from_aisc
from xsection.analysis import SectionInteraction

import matplotlib.pyplot as plt



if __name__ == "__main__":
    shape = from_aisc("W14x426", units=units)

    mat = {
            "type": "J2",
            "nu": 0.3,
            "E":  29000*ksi,
            "Fy":    50*ksi,
            "Hiso": 0.003*29e3*ksi,
            "Fs": 0, "Fo": 0, "Hsat": 0
    }

    axial = np.linspace(-5e3*kip, 5e3*kip, 10)

    si = SectionInteraction(("ShearFiber", shape, mat), axial=axial)
    # si.surface2(nstep=200, incr=1e-4)

    fig, ax = plt.subplots(figsize=(12, 6))
    for N, M, k in si.surface():
        ax.plot(k, M, '.', label=f"{N/kip:.0f} kip")
    
    ax.axvline(0, color="k", lw=1)
    ax.axhline(0, color="k", lw=1)
    ax.set_ylabel("Moment (kip-in)")
    fig.legend()
    plt.show()
