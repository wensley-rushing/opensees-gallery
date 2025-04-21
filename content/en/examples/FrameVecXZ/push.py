import opensees.openseespy as xara
from opensees.units.fps import foot, inch, ksi, kip
import veux
from shps.shapes import WideFlange

def create_angle(vertical = 2):

    shape = WideFlange(d=8*inch, b=6.5*inch, tw=0.5*inch, tf=0.5*inch)

    height = 6*foot
    width =  8*foot
    import sys
    model = xara.Model(ndm=3, ndf=6)

    model.material("ElasticIsotropic", 1, E=29e3*ksi, nu=0.3)

    model.section("ShearFiber", 1)
    for fiber in shape.create_fibers(origin="centroid"):
        model.fiber(**fiber, material=1, section=1)

    if vertical == 2:
        model.node(1, (    0,      0, 0))
        model.node(2, (width,      0, 0))
        model.node(3, (width, height, 0))
        model.node(4, (    0, height, 0))

        model.geomTransf("Linear", 1, (1, 0, 0))
        model.geomTransf("Linear", 2, (0, 1, 0))
        model.geomTransf("Linear", 3, (0, 0, 1))
    else:
        model.node(1, (    0, 0,      0))
        model.node(2, (width, 0,      0))
        model.node(3, (width, 0, height))
        model.node(4, (    0, 0, height))

        model.geomTransf("Linear", 1, (1, 0, 0))
        model.geomTransf("Linear", 2, (0, 0, 1))
        model.geomTransf("Linear", 3, (0,-1, 0))

    model.element("ForceFrame", 2, (2,3), section=1, transform=1, shear=0) # vertical
    model.element("ForceFrame", 3, (3,4), section=1, transform=2, shear=0) # horizontal
    model.element("ForceFrame", 4, (4,1), section=1, transform=3, shear=0) # vertical


    model.fix(1, (1,1,1,  1,1,1))
    model.fix(2, (1,1,1,  1,1,1))

    artist = veux.create_artist(model, vertical=vertical)
    artist.draw_origin()
    artist.draw_outlines()
    if vertical == 2:
        model.pattern("Plain", 1, "Linear", loads={3: (1e3*kip, 0, 100*kip,  0, 0, 0),
                                                   4: (      0, 0, 100*kip,  0, 0, 0)}
        )
    else:
        model.pattern("Plain", 1, "Linear", loads={3: (1e3*kip, -100*kip, 0,   0, 0, 0),
                                                   4: (      0, -100*kip, 0,   0, 0, 0)}
        )
    model.integrator("LoadControl", 0.01)
    model.analysis("Static")
    model.analyze(1)
    artist.draw_outlines(state=model.nodeDisp, scale=1e1)
    # artist.draw_sections()
    # artist.draw_surfaces()
    # artist.draw_axes(extrude=True)
    veux.serve(artist, viewer="mv", port=8080)

if __name__ == "__main__":
    create_angle(vertical=2)
