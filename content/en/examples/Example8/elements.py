import veux 
import xara
import numpy as np

import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

import xara.units.fks as units
from xara.units.fks import inch, foot, kip, ksi

from xsection.library import from_aisc

from veux.config import MeshStyle, NodeStyle

from shps.frame.extrude import ExtrudeTetrahedron



def draw_fiber_beam(L, shape):

    m = xara.Model(ndm=3, ndf=6)

    m.node(1, (0, 0, 0))
    m.node(2, (L, 0, 0))

    m.nDMaterial("ElasticIsotropic", 1, 29e3*ksi, 0.3)
    m.section("ShearFiber", 1)

    for fiber in shape.create_fibers(origin="centroid", mesh_scale=1/1.5):
        m.fiber(**fiber, material=1, section=1)

    m.geomTransf("Linear", 1, (0, 0, 1))
    m.element("ForceFrame", 1, (1,2), 8, 1, 1)

    #
    # Render
    #

    a = veux.create_artist(m, model_config={"extrude_outline": shape}, vertical=3)

    # draw the outside with transparency
    a.draw_sections(mesh_style=MeshStyle(color="gray", alpha=0.4))

    # draw the sections with fibers
    Rc = a._plot_rotation
    exterior = shape.exterior()
    exterior = np.append(exterior, [exterior[0]], axis=0)
    for x in m.eleResponse(1, "integrationPoints"):
        outline = np.array([Rc@[x, *point] for point in exterior])
        a.canvas.plot_lines(outline)
        for fiber in shape.create_fibers(origin="centroid", mesh_scale=1/1.5):
            a.canvas.plot_nodes([Rc@[x, fiber["y"], fiber["z"]]],
                                style=NodeStyle(color="red", scale=0.05))
    return a 

def draw_solid_beam(L, shape):
    mesh = shape.create_shape(mesh_scale=1/1.5).mesh

    n = 30
    ex = ExtrudeTetrahedron(mesh.nodes, mesh.cells(), direction=[0, 0, L/n])

    model = xara.Model(ndm=3, ndf=3)
    model.material("ElasticIsotropic", 1, 29e3, 0.23)

    for i in range(n):

        for tag, coords in ex.nodes():
            model.node(tag, tuple(coords))
            if i==0 and coords[-1] == 0:
                model.fix(tag, (1, 1, 1))
            elif i == n-1:
                model.load(tag, (0, -1, 0), pattern=1)

        for tag, cell in ex.cells():
            model.element("FourNodeTetrahedron", tag, tuple(cell), 1)

        ex.advance()

    artist = veux.create_artist(model, ndf=3)
    artist.draw_surfaces()
    artist.draw_outlines()
    return artist


if __name__ == "__main__":
    # shape = from_aisc("W18x211", units=units)
    shape = from_aisc("W14x426", units=units)
    a = draw_fiber_beam(10*foot, shape)
    a = draw_solid_beam(10*foot, shape)
    veux.serve(a)
