---
title: Extrusion with bricks
Downloads:
  Python: ["hexa.py", "requirements.txt"]
  Tcl: ["hexa.tcl"]
thumbnail: img/examples/hexa-tube.png
---

In this example a plane quadrilateral mesh is extruded to create
a 3D hexahedron finite element mesh. The plane mesh is created
along the same lines as the beam with a hole from [this](../planeblock/)
example. 

Given a float array `nodes` of node coordinates and an integer array
`cells` where each row defines a quadrilateral with four indices into 
the `nodes` array, the extrusion generator is initialized:
```python
ex = ExtrudeHexahedron(nodes, cells)
```

Next the *Model* is defined:
```python
model = xara.Model(ndm=3, ndf=3)
model.material("ElasticIsotropic", 1, 29e3, 0.23)
model.pattern("Plain", 1, "Linear")
```

Finally, the extrusion is performed generating `n=100`
layers of bricks:

```python
n = 100
for i in range(n):

    for tag, coords in ex.nodes():
        model.node(tag, tuple(coords))
        if i==0 and coords[-1] == 0:
            model.fix(tag, (1, 1, 1))
        elif i == n-1:
            model.load(tag, (1, -1, 0), pattern=1)

    for tag, cell in ex.cells():
        model.element("stdBrick", tag, tuple(cell), 1)

    ex.advance([0, 0, 10])
```

{{< render hexa.glb >}}

