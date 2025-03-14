---
title: Finite deformation
draft: true
thumbnail: img/examples/FiniteTension.png
---

See [this](https://cimne.com/cvdata/cntr2/spc2466/dtos/mdia/Assigment%203-1st%20part-Perell%C3%B3%20i%20Ribas-Rafel.pdf)


In this simulation we investigate the deformation map
$$
\bm{x} = (\Lambda \mathbf{e}\otimes\mathbf{e} + \mathbf{e}_{\alpha}\otimes\mathbf{e}_{\alpha})\bm{X}
$$

The deformation gradient is, in coordinates:

$$
\boldsymbol{F}=\left[\begin{array}{lll}
\Lambda & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{array}\right]
$$

$$
\boldsymbol{C}=\boldsymbol{F}^T \boldsymbol{F}=\left[\begin{array}{ccc}
\Lambda^2 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{array}\right]
$$
furnishing the Green-Lagrange strain \(\boldsymbol{E}\)
$$
\boldsymbol{E}=\frac{1}{2}(\boldsymbol{C}-\boldsymbol{I})=\left[\begin{array}{ccc}
\frac{1}{2}\left(\Lambda^2-1\right) & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]
$$

For a SVK material the 2PK stress is
$$
\boldsymbol{S}=\lambda \operatorname{tr}(\boldsymbol{E}) \boldsymbol{I}+2 \mu \boldsymbol{E}=\left[\begin{array}{ccc}
\left(\Lambda^2-1\right)\left(\frac{\lambda}{2}+\mu\right) & 0 & 0 \\
0 & \frac{\lambda}{2}\left(\Lambda^2-1\right) & 0 \\
0 & 0 & \frac{\lambda}{2}\left(\Lambda^2-1\right)
\end{array}\right]
$$
$$
\boldsymbol{P}=\boldsymbol{F} \boldsymbol{S}=\left[\begin{array}{ccc}
\Lambda\left(\Lambda^2-1\right)\left(\frac{\lambda}{2}+\mu\right) & 0 & 0 \\
0 & \frac{\lambda}{2}\left(\Lambda^2-1\right) & 0 \\
0 & 0 & \frac{\lambda}{2}\left(\Lambda^2-1\right)
\end{array}\right]
$$

and

$$
P_{x X}=\Lambda\left(\Lambda^2-1\right)\left(\frac{\lambda}{2}+\mu\right)
$$
