---
title: Rigid Offsets
draft: false
---

In this example we investigate the `offset` argument for frame geometric transformations.

$$
\boldsymbol{A}_v = \begin{bmatrix}
-dX/L_e   &  dY/L_e   & 0 &  dX/L_e   \\
-dY/L_e^2 & -dX/L_e^2 & 0 &  dY/L_e^2 \\
-dY/L_e^2 & -dX/L_e^2 & 1 &  dY/L_e^2 \\
\end{bmatrix}
$$

$$
\boldsymbol{A}_o = 
\begin{bmatrix}
0 & 1 &               0 \\
1 & 0 & -L_o/\sqrt{2}   \\
0 & 0 &               1 \\
0 & 0 &  L_o/\sqrt{2}   \\
\end{bmatrix}
$$

$$
\boldsymbol{K}_e = \begin{bmatrix}
EA/L_e &       0 &       0 \\
    0 & 4 EI/L_e & 2 EI/L_e \\
    0 & 2 EI/L_e & 4 EI/L_e \\
\end{bmatrix}
$$

{{< fold diamond.py >}}

