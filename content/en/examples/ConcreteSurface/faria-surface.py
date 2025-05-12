from opensees import openseespy as ops
import numpy as np
from math import pi, sin, cos
from matplotlib import pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass


def analyze_dir(material, dX, dY, sig0):

    # info
    print("Analyze direction ({:8.3g}, {:8.3g})".format(dX, dY))

    # the 2D model
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 2)

    ops.nDMaterial(*material)

    # the plane stress
    ops.section('PlaneStress', 2, 1, 1.0)

    # Create a triangle patch
    ops.node(1, 0, 0)
    ops.node(2, 1, 0)
    ops.node(3, 0, 1)
    ops.element('tri31', 1,   (1, 2, 3),   section=1) #1.0, 'PlaneStress', 2)

    # Create fixities
    ops.fix(1,   1, 1)
    ops.fix(2,   0, 1)
    ops.fix(3,   1, 0)

    # Define a simple ramp time series
    ops.timeSeries('Linear', 1, '-factor', 2.0*sig0)

    # Define load pattern for imposed stresses in the given direction
    ops.pattern('Plain', 1, 1)
    ops.load(2,  dX, 0.0, pattern=1)
    ops.load(3, 0.0,  dY, pattern=1)

    # analyze
    ops.constraints('Transformation')
    ops.numberer('Plain')
    ops.system('FullGeneral')
    ops.test('NormDispIncr', 1.0e-6, 10, 0)
    ops.algorithm('Newton')

    dLambda = 0.1
    dLambdaMin = 0.0001
    Lambda = 0.0
    sX = 0.0
    sY = 0.0
    while True:
        ops.integrator('LoadControl', dLambda)
        ops.analysis('Static')
        ok = ops.analyze(1)
        if ok == 0:
            stress = ops.eleResponse(1, 'material', 1, 'stress')
            sX = stress[0]
            sY = stress[1]
            Lambda += dLambda
            if Lambda > 0.9999:
                break
        else:
            dLambda /= 2.0
            if dLambda < dLambdaMin:
                break

    return sX, sY

def plot_surface(material, sig0):
    # number of subdivisions
    NDiv = 80
    NP = NDiv+1
    dAngle = 2.0*pi/NDiv
    SX = np.zeros(NP)
    SY = np.zeros(NP)

    for i in range(NP):
        angle = float(i)*dAngle
        dX = cos(angle)
        dY = sin(angle)
        a,b = analyze_dir(material, dX, dY, sig0)
        SX[i] = a
        SY[i] = b

    #
    #
    #
    plt.ion()
    fig, ax = plt.subplots(1,1)
    ax.set(xlim=[-45, 10], ylim=[-45, 10])
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
    ax.grid(linestyle=':')
    ax.set_aspect('equal', 'box')
    ax.set(xlim=[min(1.1*SX), max(1.1*SX)], ylim=[min(1.1*SY), max(1.1*SY)])

    the_line, = ax.plot(SX, SY, '-k', linewidth=2.0)

    for i in range(NP):
        the_line.set_xdata(SX[:i])
        the_line.set_ydata(SY[:i])
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    # the isotropic material
    E    = 30e3
    v    =  0.2
    sig0 = 30.0
    fc = sig0
    ec = fc/E
    ft = fc/10.0
    et = ft/E

    # Collect arguments for defining the material
    material = [
        'PlasticDamageConcrete', 1, E, v, ft, fc
    ]

    plot_surface(material, sig0)

