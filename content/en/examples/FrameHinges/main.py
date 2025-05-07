from math import sqrt
import veux
from shps.shapes import WideFlange, Rectangle
import opensees.openseespy as ops
import matplotlib.pyplot as plt
from xara.post import FrameMoments
from xara.units.fps import inch, foot, ksi, kip
# try:
#     plt.style.use("veux-web")
# except:
#     pass


def create_distributed(element, shape, fy, L, a):
    model = ops.Model(ndm=3, ndf=6)
    model.node(10, ( 0, 0, 0))
    model.node(15, (a/2, 0, 0))
    model.node(20, ( a, 0, 0))
    model.node(25, (a+(L-a)/2, 0, 0))
    model.node(30, ( L, 0, 0))

    model.fix (10, (1,1,1,  1,1,1))
    model.fix (30, (1,1,1,  1,1,1))

    E = 29e3*ksi
    nu = 0.3
    K = E/(3*(1-2*nu))
    G = 0.5*E/(1+nu)
    model.nDMaterial("J2", 1, K, G, fy, 0, 0, 0.001*E)
    # model.nDMaterial('J2BeamFiber', 1, E, nu, fy, 0.1*E, 0.0)

    model.section("ShearFiber", 1)
    for fiber in shape.create_fibers(material=1):
        model.fiber(**fiber,  section=1)

    model.geomTransf("Linear", 1, (0,0,1))
    nip = 18
    model.element(element, 1, (10,15), nip, 1, 1 ) #transform=1, sections=1)
    model.element(element, 2, (15,20), nip, 1, 1 ) #transform=1, sections=1)
    model.element(element, 3, (20,25), nip, 1, 1 ) #transform=1, sections=1)
    model.element(element, 4, (25,30), nip, 1, 1 ) #transform=1, sections=1)

    return model


def analyze(model, Pmax):

    #
    # Loading
    #
    model.pattern("Plain", 1, "Linear", loads={20: (0,0,-1,  0,0,0)})
    model.integrator("LoadControl", 1.2*Pmax/100)
    model.test("NormDispIncr", 1e-10, 20, 0) ; # OK with J2BeamFiber, bad for J2
    # model.test("NormDispIncr", 1e-8, 30, 1)
    model.analysis("Static")

    model.analyze(1)

    P = []
    u = []
    while model.getTime() < Pmax:
        if model.analyze(1) != 0:
#           raise ValueError(f"Analysis failed at time = {model.getTime()}")
            print(f"Analysis failed at time = {model.getTime()}")
            break
        P.append( model.getTime()/Pmax)
        u.append(-model.nodeDisp(20,2)/L)

    return u, P

if __name__ == "__main__":

    Fy = 50*ksi
    L  = 300*inch
    a  = 100*inch
    fig, ax = plt.subplots()

    # Rectangle

    # J    = 5.26
    # Cw   = 15000
    # Ix   = 2700
    Zx   = 254*inch**3
    # Sx   = 222
    # Iy   = 109
    # Zy   = 37.5
    # Sy   = 24.0
    wshape = WideFlange(
                tf =  0.875*inch,
                tw =  0.515*inch,
                d  = 24.3*inch,
                b  =  9.07*inch,
                mesher="gmsh"
            )

    reduce = 7/8
    Pmax = (2*Zx*Fy/(a*(L-a)))*L *reduce
    print(f"Mp = {Zx*Fy}")

    model = create_distributed("ForceFrame", wshape, Fy, L, a)
    u, P = analyze(model, Pmax)
    ax.plot(u, P)
    artist = veux.create_artist(model, vertical=3)
#   artist.draw_sections()
    artist.draw_outlines()
    artist.draw_nodes()
    scale = 1000 # 1/80
    artist.draw_diagrams(field=FrameMoments(model, artist), scale=scale, color="blue")


    rshape = Rectangle(d = wshape.d, #10/sqrt(5),
                       b = Zx/wshape.d**2*4, 
                       mesher="gmsh")
    # Zx = rshape.b*rshape.d**2/4
    model = create_distributed("ForceFrame", rshape, Fy, L, a)
    u, P = analyze(model, Pmax)
    ax.plot(u, P)
    artist.draw_diagrams(field=FrameMoments(model, artist), scale=scale, color="red")


    #
    # Finalize
    #
    ax.set_xlabel(r"Mid-span drift, $u/L$")
    ax.set_ylabel(r"Load factor, $\lambda$")

    ax.axhline(y=1, color='r', linestyle='--')
    ax.text(-1, 1, r"$\lambda_c$", color='r', va='center', ha='right', 
            bbox=dict(facecolor='white', edgecolor='none', pad=2.0))
    fig.savefig("img/e0030.png")
    # plt.show()

    veux.serve(artist)

