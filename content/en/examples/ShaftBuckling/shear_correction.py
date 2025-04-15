
import veux
from shps.shapes import WideFlange

import opensees.openseespy as ops

import numpy as np
import pandas as pd

import opensees.units.iks as units
pi   = units.pi
ft   = units.ft
ksi  = units.ksi
inch = units.inch


def isotropic_section(model, tag, material, properties, type):

    # Define material
    E = material["E"]
    nu = material["nu"]
    mat_tag = 1      # identifier that will be assigned to the new material

    model.material("ElasticIsotropic", mat_tag, E, nu, 0.0)
    G     = E / (2.0 * (1.0 + nu))          # Shear modulus
    tw    = 2.0
    width = 15.0
    depth = 24.0

    model.section(type, tag, GJ=1e6)
    print(f"{G = }")
    print(f"GAv = {G*tw*depth}")
    shape = WideFlange(t=tw, b=width, d=depth)
#   print(shape.summary())
    for fiber in shape.create_fibers():
        model.fiber(**fiber, section=tag, material=mat_tag)

    return shape.create_shape()


def test_isotropic(section):
    # Material
    material = dict(
        E    = 1, #29000*ksi,
        nu   = 0.2 #.2
    )
    model = ops.Model(ndm=3, ndf=6)

    d = 24.0
    sec = isotropic_section(model, 1, material, {}, section)


    tangent = model.invoke("section", 1, [
                           "update  0 0 0 0 0 0;",
                           "tangent"
            ])

    n = int(np.sqrt(len(tangent)))
    Ks = np.round(np.array(tangent), 4).reshape(n,n)
    print(pd.DataFrame(Ks))

    E = material['E']
    nu = material["nu"]
    G     = E / (2.0 * (1.0 + nu)) # Shear modulus
    Kv = Ks[1,1] + Ks[1,10]
    print(f" S.C.F. = {(E/G)*(Kv/Ks[0,0])}")

    # Render
    artist = veux.create_artist((sec.mesh.nodes, sec.mesh.cells()), ndf=1)

    field = sec.translate((0, d/3)).torsion.warping()
    artist.draw_outlines()
    artist.draw_surfaces(field = field, state=field, scale=1/100)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([R@[*sec.torsion.centroid(), 0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*sec.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)

    veux.serve(artist)

if __name__ == "__main__":
    test_isotropic("ShearFiber")
#   test_isotropic("AxialFiber")

