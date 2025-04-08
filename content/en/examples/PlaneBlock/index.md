---
title: Isoparametric Elements
weight: 20
thumbnail: img/examples/plane_block.png
tags: ["CE222"]
description: A finite element analysis is performed of a plane beam with a hole using Lagrange quadrilaterals.
---

![alt text](img/plane_block.png)

This example introduces mesh-building tools for solid modeling. 
A finite element analysis is performed of a plane beam with a hole using various Lagrange quadrilaterals. 
Visualization is performed using the [`veux`](https://pypi.org/project/veux) library.

# Creating Blocks

## Preliminaries

Before generating elements, we'll first prepare our *Model* by defining an appropriate material and section. 
Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with
`ndm = 2` and `ndf = 2`.

{{< tabs tabTotal="2" >}}
{{% tab name="Python" %}}
```python
import opensees.openseespy as ops

model = ops.Model(ndm=2, ndf=2)
```
{{% /tab %}}
{{% tab name="Tcl" %}}
```tcl
model -ndm 2 -ndf 2
```
{{% /tab %}}
{{< /tabs >}}

As with the example of a [tapered beam](../planetaper/), the [ElasticIsotropic](https://xara.so/user/manual/material/ndMaterials/ElasticIsotropic.html) material model is employed.

```python
E = 4e3
nu = 0.25 # Poisson's ratio
model.material("ElasticIsotropic", 1, E, nu, 0)
model.section("PlaneStress", 1, 1, 1)
```

{{< fold plane_block.py "analysis script" >}}

### Validation

$$
\begin{gathered}
 A G k_s\left( w'(x)+\theta(x)\right) - E \theta''(x) =0 \\
-A G k_s\left(\frac{\partial^2}{\partial x^2} w(x)+\frac{\partial}{\partial x} \theta(x)\right)=\bar{q}
\end{gathered}
$$

The boundary conditions are

$$
u_y(0)=0, \quad \theta(0)=0, \quad u_y(L)=0 \quad \theta(L)=0
$$

The solution is:

$$
u_y(x)=\frac{q_0 L^4}{24 E I^{}} \frac{x^2}{L^2}\left(1-\frac{x}{L}\right)^2-\frac{1}{k_s G A}\frac{q_0 L^2}{24} \left(1-12 \frac{x}{L}+12 \frac{x^2}{L^2}\right) + \frac{1}{G A k_s L^2} \frac{q_0 L^4}{24}
$$

## Combining Blocks


{{< fold hole.py "analysis script" >}}
