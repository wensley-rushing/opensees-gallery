import numpy as np

import xara
import xara.units.fks as units
from xara.units.fks import kip, ksi

from xsection.library import from_aisc
from xsection.analysis import SectionInteraction

import matplotlib.pyplot as plt



def section_interaction(shape, mat, axial):
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    # test = lambda m: m.eleResponse(1, "section", "fiber", (0.0, 0.0), "stress")[0] < 0.9*50*ksi
    for N in axial:
        M, k = zip(*moment_curvature(shape, mat, N, 0.01, 100))
        ax.plot(k, M, label=f"{N/kip:.0f} kip")
    plt.show()


def moment_curvature(shape, mat, axialLoad, maxK, numIncr):
    """
    A procedure for performing section analysis

    Arguments
       secTag -- tag identifying section to be analyzed
       axialLoad -- axial load applied to section (negative is compression)
       maxK -- maximum curvature reached during analysis
       numIncr -- number of increments used to reach maxK (default 100)
    """

    model = xara.Model(ndm=3, ndf=6)
    m = mat
    model.nDMaterial(m["type"], 1, **{k: v for k, v in m.items() if k != "type"})

    model.section("ShearFiber", 1)
    
    for fiber in shape.create_fibers():
        model.fiber(**fiber, material=1, section=1)


    # Define two nodes at (0,0)
    model.node(1, (0, 0, 0))
    model.node(2, (0, 0, 0))

    # Fix all degrees of freedom except axial and bending
    model.fix(1, (1, 1, 1,  1, 1, 1))
    model.fix(2, (0, 1, 1,  1, 1, 0))

    # Create element
    model.element("zeroLengthSection", 1, (1, 2), 1)

    # Define constant axial load
    model.pattern("Plain", 1, "Constant", loads={2: [axialLoad, 0, 0,   0,0,0]})

    # Define analysis
    model.system("BandGeneral")
    model.numberer("Plain")
    model.constraints("Plain")
    model.test("NormUnbalance", 1.0e-8, 20)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.0)
    model.analysis("Static")

    # Do one analysis for constant axial load
    model.analyze(1)

    # Define reference moment
    model.pattern("Plain", 2, "Linear")
    model.load(2, (0, 0, 0,  0,0,1), pattern=2)

    # Compute curvature increment
    dK = maxK/numIncr

    # Use displacement control at node 2 for section analysis
    model.integrator("DisplacementControl", 2, 6, dK, 1, dK, dK)

    MK = []
    for i in range(numIncr):
        # Evaluate step
        if model.analyze(1) != 0:
            break

        # Get moment and curvature
        M = model.eleResponse(1, "force")[5]
        k = model.nodeDisp(2, 6)

        MK.append([-M, k])
    return MK


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

    axial = np.linspace(5e3*kip, -5e3*kip, 10)
    SectionInteraction((shape, mat), axial=axial).analyze(nstep=200, incr=1e-4)

    section_interaction(shape, mat, axial)
