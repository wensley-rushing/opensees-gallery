---
title: Solid extrusions
thumbnail: img/examples/tetra-channel.png
tags: ["Solid"]
description: |
  Mesh generation utilities are used to create a 3D tetrahedron model of a cantilever beam with a channel cross section.
downloads:
  Python: ["tetra.py", "requirements.txt"]
  Tcl: ["tetra.tcl"]
---

This investigation begins with a plane triangle mesh of a channel cross section. 
```python
from shps.shapes import Channel
mesh = Channel(d=16, b=8, tf=1.0, tw=1.0).create_shape(mesh_scale=0.75).mesh
```
Next we use the `ExtrudeTetrahedron` class which will generate node locations and connectivity for a tetrahedron mesh:
```python
from shps.frame.extrude import ExtrudeTetrahedron

ex = ExtrudeTetrahedron(mesh.nodes, mesh.cells())
```

Next we setup a `Model` instance for the 3D simulation:
```python
model = xara.Model(ndm=3, ndf=3)
model.material("ElasticIsotropic", 1, 29e3, 0.23)
model.pattern("Plain", 1, "Linear")
```
And finally we perform `n = 100` extrusions:
```python
n = 100
for i in range(n):

    for tag, coords in e.nodes():
        model.node(tag, tuple(coords))
        if i==0 and coords[-1] == 0:
            model.fix(tag, (1, 1, 1))
        elif i == n-1:
            model.load(tag, (0, -1, 0), pattern=1)

    for tag, cell in e.cells():
        model.element("FourNodeTetrahedron", tag, cell, 1)

    e.advance()
```
This will create the following finite element model, which is rendered with veux:

![Channel section](img/channel.png)

After performing the analysis the deformed shape is:
![Deformed cantilever](img/channel-deformed.png)