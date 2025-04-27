---
title: Fire
draft: true
---

# FEM-fire

Investigation of thermal effects of fire on structural materials in finite element analysis.

In a coupled thermo-mechanical analysis, one solves a BVP for two functions, $u(x)$ represents the displacement and $\vartheta(x)$ represents the temperature. For example, given a distributed axial load $f$ and thermal flux $q(x)$:

$$
\begin{aligned}
N' + f = 0 \\
Q' + q = 0
\end{aligned}
$$

which is supported by constitutive relations:
$$
N = EA(u' - \alpha \vartheta) 
\qquad\text{ and }\qquad
Q = \kappa \vartheta'
$$

## Implementation

```python

```
