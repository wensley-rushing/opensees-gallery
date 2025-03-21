---
title: Built-in mesh tools
thumbnail: img/examples/plane_block.png
tags: ["CE222"]
description: A finite element analysis is performed of a plane beam with a hole using linear Lagrange quadrilaterals.
---

![alt text](img/plane_block.png)

This introduces mesh-building tools for solid modeling. A finite element analysis is performed of a plane beam with a hole using linear Lagrange quadrilaterals. 
Visualization is performed using the [`veux`](https://pypi.org/project/veux) library.

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
model.section("PlaneStrain", 1, 1, 1)
```

{{< fold plane_block.py "analysis script" >}}

