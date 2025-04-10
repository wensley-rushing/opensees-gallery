import xara
import veux
import numpy as np
from shps.frame.extrude import ExtrudeTetrahedron
from shps import plane
from shps.shapes import Channel


if __name__ == "__main__":

    mesh = Channel(d=16, b=8, tf=1.0, tw=1.0).create_shape(mesh_scale=0.75).mesh


    e = ExtrudeTetrahedron(mesh.nodes, mesh.cells())


    model = xara.Model(ndm=3, ndf=3)
    model.material("ElasticIsotropic", 1, 29e3, 0.23)
    model.pattern("Plain", 1, "Linear")

    n = 100
    for i in range(n):

        for tag, coords in e.nodes():
            model.node(tag, tuple(coords))
            if i==0 and coords[-1] == 0:
                model.fix(tag, (1, 1, 1))
            elif i == n-1:
                model.load(tag, (0, -1, 0), pattern=1)

        for tag, cell in e.cells():
            model.element("FourNodeTetrahedron", tag, tuple(cell), 1)

        e.advance()

    model.integrator("LoadControl", 2)
    model.system("Umfpack")
    model.analysis("Static")
    model.analyze(1)
    print("Analysis complete")
    artist = veux.create_artist(model, ndf=3)
    artist.draw_outlines(state=model.nodeDisp)
    artist.draw_surfaces(state=model.nodeDisp)
    veux.serve(artist)

