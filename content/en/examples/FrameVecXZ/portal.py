#
# Linear portal frame with steel AISC sections
#
import opensees.openseespy as xara
from opensees.units.fps import foot, inch, kip, ksi
import veux

def portal_solution(EI1, EI2, EIg, H, L):
    import numpy as np
    K = np.array([
              [ 12/H**3 * (EI1 + EI2),
                 6/H**2 *  EI1,
                 6/H**2 *  EI2],
              [  6/H**2 *  EI1,
                 4/L    * EIg + 4/H * EI1,
                 2/L    * EIg ],
              [  6/H**2 * EI2,
                 2/L    * EIg,
                 4/L    * EIg + 4/H * EI2]])

    kuw = K[1:,0]
#   print(1e3*kip*np.linalg.solve(K, [1,0,0])[0])
    return K[0][0] - kuw.dot(np.linalg.solve(K[1:,1:], kuw))

def create_portal(vertical = 2):

    height = 6*foot
    width =  8*foot
    E  = 29e3*ksi
    G  = 11.2e3*ksi
    Iy = 0.005104*(foot**4)
    Iz = 0.001107*(foot**4)
    A  = 0.06944*(foot**2)*1000
    J  = 4.3e-5*(foot**4)

    print(kip/portal_solution(E*Iy, E*Iz, E*Iy, height, width))

    model = xara.Model(ndm=3, ndf=6)

    model.section("ElasticFrame", 1,
                  E=29e3*ksi,
                  G=11.2e3*ksi,
                  A=A,
                  Iy=Iy,
                  Iz=Iz,
                  J=J
    )

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

    model.element("PrismFrame", 1, (2,3), section=1, transform=1, shear=0) # column
    model.element("PrismFrame", 2, (3,4), section=1, transform=2, shear=0) # girder
    model.element("PrismFrame", 3, (4,1), section=1, transform=3, shear=0) # column


    model.fix(1, (1,1,1,  1,1,1))
    model.fix(2, (1,1,1,  1,1,1))

    model.pattern("Plain", 1, "Linear", loads={3: (kip, 0, 0,  0, 0, 0),
                                               4: (  0, 0, 0,  0, 0, 0)}
    )

    model.integrator("LoadControl", 1)
    model.analysis("Static")
    model.test("NormDispIncr", inch/1000, 2)
    model.analyze(1)


    return model

if __name__ == "__main__":
    vertical = 2
    model = create_portal(vertical=vertical)
    print(model.nodeDisp(3, 1))

    artist = veux.create_artist(model, vertical=vertical)
    artist.draw_sections()
    artist.draw_outlines(state=model.nodeDisp, scale=1000)
    artist.draw_origin()
    artist.draw_axes(extrude=True)

#   artist.save("orient.glb")
    veux.serve(artist)

