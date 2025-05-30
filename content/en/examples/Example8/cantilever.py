import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(3, 1, figsize=(6, 8), sharex=True)
fig.subplots_adjust(hspace=0.3)

#
# Beam with arrow
#

L  = 10
ax = axes[0]
ax.axis("off")

#
# 1) Draw beam
#
v1, v2 = 0, 0.3
h = v2 - v1
ax.fill_between([0, L], v1, v2, color="gray")

# Draw fixed end
ax.plot([0, 0], [v1, v2], color='black', linewidth=3)
for y in np.linspace(v1, v2, 8):
    ax.plot([-0.3, 0], [y, y], color='black', linewidth=0.5)


# Red load arrow at free end
ax.arrow(L, v1, 0, -0.5, head_width=0.2, head_length=0.25, fc='red', ec='red')
# ax.annotate("", xytext=(L, 0), xy=(L, 0.6),
#             arrowprops=dict(arrowstyle="->"))
ax.annotate("", xytext=(L, v1+h/2), xy=(L*1.1, v1+h/2), arrowprops=dict(arrowstyle="->", color='black'))
ax.annotate("$x$",  xy=(L, v1 + h/2), xytext=(L*1.11, v1 + h/2))
ax.annotate("$P$",  xy=(L, v1), xytext=(L+0.3, 0))

#
# 2) Bending moment diagram
#
Mr = 4
My = 3
M = lambda x: Mr * (1 - x / L)  # Linear moment distribution
ax = axes[1]
ax.set_xlim(0, L*1.1)
ax.set_ylim(0, Mr)
ax.set_ylabel("Bending moment, $M(x)$")
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
for spine in ax.spines.values():
    spine.set_visible(False)

x = np.array([0, 2, L])
y = list(map(M, x))
ax.fill_between(x, 0, y, color="lightgray", edgecolor="black")

#
# 3) Curvature diagram
#
ax = axes[2]
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
for spine in ax.spines.values():
    spine.set_visible(False)

x_curve = np.linspace(0, L, 80)
EI = 0.1
ky = My/EI
y_curve = [-ky*np.sqrt(Mr/(Mr - M(x)))/np.sqrt(3) if M(x) >= My else -(ky*M(x)/Mr*3/2) for x in x_curve]
ax.fill_between(x_curve, 0, y_curve, color="lightgray", alpha=1, edgecolor="black")
ax.set_ylabel("Curvature, $\\kappa(x)$")

plt.show()
