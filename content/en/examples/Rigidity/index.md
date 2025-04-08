---
title: Rigidity
draft: true
---

$$
\bm{v} = \bm{A}\bm{u}
\qquad\text{and}\qquad
\bm{v}_o = \bm{A}_o \bm{u}
$$
$$
\begin{bmatrix}
\bm{A}_{f1} \\ 
\bm{A}_o \\ 
\bm{A}_{f2}
\end{bmatrix}
=\left[\begin{array}{ccccccc}
-1 / 4 & 0 & 0 & 0 & 0 & 0 & 0 \\
-1 / 4 & 1 & 0 & 0 & 0 & 0 & 0 \\ \hline
-0.6 & 0 & 0.8 & 0.6 & 0 & 0 & 0 \\
\frac{0.8}{-5} & 1 & \frac{0.6}{5} & -\frac{0.8}{5} & 0 & 0 & 0 \\
\frac{0.8}{5} & 0 & \frac{0.6}{5} & -\frac{0.8}{5} & 1 & 0 & 0 \\
0 & 0 & -0.6 & 0.8 & 0 & 0.6 & 0 \\
0 & 0 & 0.8 / 5 & 0.6 / 5 & 1 & -0.8 / 5 & 0 \\
0 & 0 & 0.8 / 5 & 0.6 / 5 & 0 & -0.8 / 5 & 1 \\ \hline
0 & 0 & 0 & 0 & 0 & 1 / 4 & 1 \\
0 & 0 & 0 & 0 & 0 & 1 / 4 & 0
\end{array} \right]
$$

$$
\bm{0}  = \bm{A}_o \bm{U}_o
$$
$$
\begin{bmatrix}
\tilde{\bm{A}}_{f1} \\ \bm{0} \\ \tilde{\bm{A}}_{f2}
\end{bmatrix}= \bm{A}\bm{U}_o
$$
Define $\bm{R}$:
$$
\bm{R} \triangleq \operatorname{rref}~[\bm{A_o} ~~~~ \bm{1}] = \begin{bmatrix}
\bm{B} &|& \bm{W} \\ 
&|& \bm{U}_o^{T}
\end{bmatrix}
$$
$$
\tilde{n}_f = \operatorname{dim} \operatorname{null} \bm{A}_o
$$
