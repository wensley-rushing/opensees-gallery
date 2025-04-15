---
title: Columns with Nonlinear Geometry and Shear
description: This example investigates P-Delta effects in columns with and without shear.
tags: ["Frame", "Steel"]
thumbnail: img/aisc-column.png
downloads:
  Python: ["aisc.py"]
---

![A column with a distributed load.](img/ai.png)

This example implements the benchmarks presented in Chapter C2 of the AISC steel manual commentary. The benchmarks consist of two cases:
- *Case 1* involves a simply supported column with a constant uniformly distributed transverse load, and a monotonically increasing axial force. This case only involves $P-\delta$ effects.
- *Case 2* involves a cantilever column with a constant transverse load at the tip and an increasing axial force. This problem involves both $P-\Delta$ and $P-\delta$ effects.

## Section

In both cases the cross section is a *W14x48* wide flange shape. Note the approximation of the shear areas $A_y$ and $A_z$:
```python
d  = 13.75*inch
b  = 8.030*inch
tw = 0.340*inch
tf = 0.595*inch
transform = "Corotational"
section = dict(
        E  = 29000.0,
        G =  11200.0,
        A  = 14.1*inch**2,
        J  = 1.45*inch**4,
        Iy = 51.4,
        Iz = 484.0,
        Ay = d*tw,
        Az = b*tf*2,
        Cw = 2240*inch**6
)
```

## Case 1

In *Case 1*, a uniformly distributed load of $0.2$ kip/ft is first applied to the elements:
```python
model.pattern("Plain", 1, "Linear")
for i in range(ne):
    model.eleLoad("-ele", i+1, "-pattern", 1, "-type", "beamUniform",  ( 0.2*kip/ft, 0.0))
```

$$
\boldsymbol{q}_0 = \frac{wL^2}{12}\begin{pmatrix}
1 \\ -1
\end{pmatrix}
= \frac{wL^2}{12}\begin{pmatrix}
1 \\ -1
\end{pmatrix}
$$

To check Case 1 we use the `eleResponse` method:

```python
def check_case1(model, Mbench, Dbench, ndm):
    ne    = len(model.getEleTags())
    Axial = model.getTime()
    Mmid  = (-1)**ndm*model.eleResponse(int(ne//2), "forces")[5 if ndm==2 else 11]
    u     = model.nodeDisp(int(ne//2)+1, 2)

    # Axial Force  |  Moment at h/2  |  Displacement at h/2 |
    print(f"| {Axial:8.0f} |", end="")
    print(f" {Mmid:8.1f} | {Mbench:8.0f} | %8.2f %% |" % (100*(Mbench-Mmid)/Mbench), end="")
    print(f" {u:8.4f} | {Dbench:8.3f} | %8.2f %% |" % ((100*(Dbench-u)/Dbench)))
```

## Case 2

{{< fold aisc.py "source code" >}}

The source code for this example is adapted from https://github.com/denavit/OpenSees-Examples

