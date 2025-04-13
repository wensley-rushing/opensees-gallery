---
title: Columns with Nonlinear Geometry and Shear
description: This example investigates P-Delta effects in columns with and without shear.
tags: ["Frame", "Steel"]
thumbnail: img/aisc-column.png
downloads:
  Python: ["aisc.py"]
---

![A column with a distributed load.](img/ai.png)

This example implements the analysis presented in the AISC steel manual.

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


{{< fold aisc.py "source code" >}}

The source code for this example is adapted from https://github.com/denavit/OpenSees-Examples

