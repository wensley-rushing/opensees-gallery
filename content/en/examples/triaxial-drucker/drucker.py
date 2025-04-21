import matplotlib.pyplot as plt
import numpy as np
try:
    plt.style.use("veux-web")
except:
    pass

if __name__ == "__main__":
    t, *U = np.loadtxt("out/displacements1.out").T
    n = 400
    for u in U:
        plt.plot(t[:n], u[:n])
    plt.savefig("img/u.png")
