# Cantilever with channel section and eccentric loading
#
import veux
from veux.motion import Motion
from shps.shapes import Channel
import opensees.openseespy as ops

# External libraries
import numpy as np
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

def create_cantilever(ne, offset, element, section, nen=2, warp_base="n", center=None):
    model = ops.Model(ndm=3, ndf=6 if warp_base =="n" else 7)

    E = 2.1e4 # MPa, or 210 GPa
    v = 0.30  # 0.5*E/G - 1
    G = 0.5*E/(1+v) # 8076.92

    nmn = ne*(nen-1)+1
    L  = 900


    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    shape = Channel(d=30, b=10, tf=1.6, tw=1.0).create_shape()

    shape = shape.translate(offset)


    # _m = shape.mesh
    # veux.serve(veux.render((_m.nodes, _m.cells())))

    if "fiber" in section.lower():
        print(f"Section = Fiber; ", center)

        model.section("ShearFiber", sec, GJ=0)

        for fiber in shape.fibers(center=center):
            y, z = fiber.location
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], section=sec) #fiber.warp[1], section=sec)

    else:
        print("Section = Elastic")
        shape.torsion._solution = shape.translate(center).torsion.solution()
        cnn = shape.torsion.cnn()
        cnm = shape.torsion.cnm()
#       cnw = shape.torsion.cnw()
        cnv = shape.torsion.cnv()
        cmm = shape.torsion.cmm()
        cww = shape.torsion.cww()
        cmv = shape.torsion.cmv()
        cmw = shape.torsion.cmw()
        A = cnn[0,0]
        model.section("ElasticFrame", sec,
                        E=E,
                        G=G,
                        A=A,
                        Ay=1*A,
                        Az=1*A,
                        Qy=cnm[0,1],
                        Qz=cnm[2,0],
                        Iy=cmm[1,1],
                        Iz=cmm[2,2],
                        Iyz=cmm[1,2],
                        J =shape.torsion.torsion_constant(),
                        Cw= cww[0,0],
#                       Rw= 0, #cnw[0,0], # this is pretty much always 0.0
                        Ry= cnv[1,0],
                        Rz= cnv[2,0],
                        Sa= cmv[0,0],
                        Sy= cmw[1,0],
                        Sz= cmw[2,0]
        )


#   model.geomTransf("Corotational", 1, (0,1,0))
    model.geomTransf("Linear", 1, (0,0,1))

    for i,x in enumerate(np.linspace(0, L, nmn)):
        model.node(i, (x,0,0))

    model.fix(0,  (1,1,1,  1,1,1, int(warp_base in "pr")))
    if warp_base == "r":
        model.fix(nmn-1,  (0,0,0,  0,0,0, 1))

    for i in range(ne):
        start = i * (nen - 1)
        nodes = list(range(start, start + nen))
        model.element(element, i+1, nodes, section=sec, transform=1)


    return model, shape

def analyze(element, section, pattern="D", nen=2, warp_base="n", cpoint=None, render=False):
    ne = 20
    en = ne*(nen-1)
    if pattern in {"D", "node"}:
        # Top
        offset = ( 0,    15)
    elif pattern == "A":
        # Shear center
        offset = (-3.571, 0)
    elif pattern == "B":
        offset = (     0, 0)
    elif pattern == "C":
        # Centroid
        offset = ( 2.449, 0)

    o = np.array(offset)
    if cpoint in {"D", "node"}:
        # Top
        center = ( 0,    15) - o
    elif cpoint == "A":
        # Shear center
        center = (-3.571, 0) - o
    elif cpoint == "B":
        center = (     0, 0) - o
    elif cpoint == "C":
        # Centroid
        center = ( 2.449, 0) - o

    model,shape = create_cantilever(ne, offset,
                                    center=center,
                                    element=element,
                                    section=section,
                                    nen=nen,
                                    warp_base=warp_base)
    if render:
        artist = veux.create_artist(model, model_config=dict(extrude_outline=shape))
        artist.draw_nodes(size=10)
        # artist.draw_sections()
        # veux.serve(artist)
        motion = Motion(artist)

    #
    # Apply vertical load
    #
    speed  =  1 # animation frames
    Pmax   = 20 # kN
    model.pattern("Plain", 1, "Linear")
    if pattern in {"D", "node"}:
        print("Pattern = node")
        model.load(en, (0,0,-1,  0,0,0,0), pattern=1)
#       model.load(ne, (0,-1,0,  0,0,0), pattern=1)

    else:
        print("Pattern = Element, offset = ", offset)
        model.eleLoad("Frame", "Dirac",
                      basis = "global",
                      force = [0, 0, -1],
                      offset=[ 1.0,
                               0.0-offset[0],
                              15.0-offset[1]],
                      pattern=1,
                      elements=[ne]
        )

    model.system('BandGen')
    model.integrator("LoadControl", Pmax/100, 5, Pmax/500, Pmax/10)
    model.test("NormDispIncr", 1e-11, 50, 0)
#   model.test('NormUnbalance',1e-6,10,1)
    model.algorithm("Newton")
    model.analysis("Static")
    fg_warp, ax_warp = plt.subplots()

    u = []
    v = []
    w = []
    P = []
    i = 0
    x = [model.nodeCoord(node, 1) for node in model.getNodeTags()]
    while model.getTime() <= Pmax:
        i += 1
        if render:
            motion.advance(time=model.getTime()*speed)
            motion.draw_sections(rotation=model.nodeRotation,
                                 position=model.nodeDisp)
        u.append(-model.nodeDisp(ne, 1))
        v.append( model.nodeDisp(ne, 2))
        w.append(-model.nodeDisp(ne, 3))
        P.append( model.getTime())

        status = model.analyze(1)

        if not i%50 or status != 0 or model.getTime() >= Pmax:
            if warp_base != "n":
                ampl = [model.nodeDisp(node,7) for node in model.getNodeTags()]
            else:
                twist = [model.nodeDisp(node,4) for node in model.getNodeTags()]
                ampl = np.gradient(twist, x)

#           ampl[np.isclose(ampl, 0, atol=1e-8)] = 0.0
            ax_warp.plot(x, ampl)


        if status != 0:
            print(f"Failed at time = {model.getTime()} with v = {v[-1]}")
            break


    if True:
        fig, ax = plt.subplots()
        ax.set_xlabel(r"Displ, $v$")
        ax.set_ylabel("Load, $P$")
        ax.set_xlim([-100, 280])
        ax.set_ylim([0,   Pmax])
        ax.axvline(0, color='black', linestyle='-', linewidth=1)
        ax.axhline(0, color='black', linestyle='-', linewidth=1)
        ax.plot(u, P, label="$u$")
        ax.plot(v, P, label="$v$")
        ax.plot(w, P, label="$w$")
        ax.legend()

        name = f"{pattern}-{cpoint}-{warp_base}-{section}-{element[:5].lower()}"
        fig.savefig(f"img/{name}-displacements.png")

        ax_warp.set_xlim([0,  900])
#       ax_warp.set_ylim([-0.009,  0.009])
        ax_warp.axvline(0, color='black', linestyle='-', linewidth=1)
        ax_warp.axhline(0, color='black', linestyle='-', linewidth=1)
        fg_warp.savefig(f"img/{name}-warping.png")

        if render:
            plt.show()
            motion.add_to(artist.canvas)
            veux.serve(artist)

if __name__ == "__main__":
    import os
    analyze(pattern = os.environ.get("Pattern", "D"),
            element = os.environ.get("Element", "ExactFrame"),
            section = os.environ.get("Section", "ShearFiber"),
            nen=2,
            render=False,
            cpoint  = os.environ.get("Center", None),
            warp_base=os.environ.get("Warping", "n") # "f", "r", "n"
            )

