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
                x = np.loadtxt(arg)
            else:
                y_files.append(arg)

    print(y_files)
    ys = [
        np.loadtxt(f)[:,-1]
        for f in y_files
    ]
    if len(ys) > 0:
        for y in ys:
            plt.plot(x, y)
    else:
        plt.plot(x)

    plt.show()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
