import veux
import numpy as np
from opensees.units.fps import foot, inch
from shps.shapes import WideFlange
from veux.utility.alpha_shape import alpha_shape
import matplotlib.pyplot as plt

if __name__ == "__main__":
    shape = WideFlange(d=8*inch, b=6.5*inch, t=0.5*inch)
    print(shape.create_shape().summary())


    points = np.array([
        fiber.location for fiber in shape.create_fibers(origin="centroid")
    ])

    fig, ax = plt.subplots()
    ax.scatter(*zip(*points), 0.2, marker=".")
    ax.set_aspect("equal")
    alpha = alpha_shape(points, radius=0.01)
    ax.scatter(*zip(*alpha), 0.2, marker=".", color="red")
    plt.show()


    mesh = shape.create_shape().mesh
    artist = veux.create_artist((mesh.nodes, mesh.cells()), ndf=1)
    artist.draw_surfaces()
    d = 8*inch
#   R = np.eye(3)
    R = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 0, 0]])
    artist.canvas.plot_vectors([[0,0,0] for i in range(3)], d/5*R.T,
                               extrude=True)
#   artist.draw_origin(extrude=True)
    veux.serve(artist)
