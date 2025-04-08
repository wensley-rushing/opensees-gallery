
import xara
from xara.helpers import find_node, find_nodes
from veux.stress import node_average

def create_ledge(mesh,
                thickness=1,
                element: str = "LagrangeQuad"):

    nx, ny = mesh

    # create model in two dimensions with 2 DOFs per node
    model = ops.Model(ndm=2, ndf=2)

    # Define the material
    # -------------------
    #                                 tag  E      nu   rho
    model.material("ElasticIsotropic", 1, 1000.0, 0.25, 0, "-plane-strain")

    # Define geometry
    # ---------------

    load = 1000.0
    angle = 0
    b = 30
    L = 100.0
    r = 15/L

    # Create the nodes and elements using the surface command
    # {"quad", "enhancedQuad", "tri31", "LagrangeQuad"}:
    args = (thickness, "PlaneStrain", 1)

    surface = model.surface((nx, ny),
                  element=element, args=args,
                  points={
                    1: [  0.0,   0.0],
                    5: [  L/2,   10.],
                    2: [   L,    L*r],
                    3: [   L,     b ],
                    4: [  0.0,    b ]
                  })

    # Single-point constraints
    #            x   (u1 u2)
    for node in find_nodes(model, x=0.0):
        print("Fixing node ", node)
        model.fix(node, (1, 1))

    # Define gravity loads
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")

#   # Find the node at the tip center
#   place = find_node(model, x=L, y=15.0)
#   print(f"Placing load at node {place}")
#   force = (1.0, 0.0)
#   model.load(place, force, pattern=1)

    tip = list(find_nodes(model, x=L))
    for node in tip:
        model.load(node, (load/len(tip), 0.0), pattern=1)

    return model


