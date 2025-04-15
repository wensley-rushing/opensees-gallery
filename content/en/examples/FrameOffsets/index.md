---
title: Rigid Offsets
draft: false
description: Geometric transformations are employed to model rigid joint offsets in frames.
---

In this example we investigate the `offset` argument for frame geometric transformations. The syntax is as follows:

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
m.geomTransf("Linear", 1, (0, 0, 1),
             offset={
                1: ( off/np.sqrt(2), off/np.sqrt(2), 0),
                2: (-off/np.sqrt(2),-off/np.sqrt(2), 0),
             }
)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
geomTransf Linear 1  0 0 1  -offset {
  1  0.35355339059327373  0.35355339059327373 0
  2 -0.35355339059327373 -0.35355339059327373 0
}
```
{{% /tab %}}
{{< /tabs >}}

## Validation

Recall the stiffness $\boldsymbol{K}_e$ of a linear 2D Euler-Bernoulli beam:

$$
\boldsymbol{K}_e = \begin{bmatrix}
EA/L_e &       0 &       0 \\
    0 & 4 EI/L_e & 2 EI/L_e \\
    0 & 2 EI/L_e & 4 EI/L_e \\
\end{bmatrix}
$$

This is transformed into the angled configuration using the transformation:

$$
\boldsymbol{A}_v = \begin{bmatrix}
-dX/L_e   &  dY/L_e   & 0 &  dX/L_e   \\
-dY/L_e^2 & -dX/L_e^2 & 0 &  dY/L_e^2 \\
-dY/L_e^2 & -dX/L_e^2 & 1 &  dY/L_e^2 \\
\end{bmatrix}
$$

and joint offsets are similarly applied with:

$$
\boldsymbol{A}_o = 
\begin{bmatrix}
0 & 1 &               0 \\
1 & 0 & -L_o/\sqrt{2}   \\
0 & 0 &               1 \\
0 & 0 &  L_o/\sqrt{2}   \\
\end{bmatrix}
$$


{{< fold diamond.py >}}

