import matplotlib.pyplot as plt
plt.style.use("veux-web")
import numpy as np

def main(argv):
    x = None 
    y_files = []
    argi = iter(argv)
    for arg in argi:
        if arg == "--x":
            x = next(argi)
        else:
            if x is None:
                x = arg
            else:
                y_files.append(arg)

    ys = [
        np.loadtxt(f)[:,-1]
        for f in y_files
    ]

    x_data = np.loadtxt(x)
    if len(ys) > 0:
        for y in ys:
            plt.plot(x_data, y)
    elif len(x_data.shape) == 1:
        plt.plot(x_data)
    else:
        plt.plot(*x_data.T)

    plt.show()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
