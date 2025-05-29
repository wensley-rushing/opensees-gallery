from opensees import openseespy as _ops
import numpy as np
from math import pi, sin, cos
from matplotlib import pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass


def create_model(material):
    model = _ops.Model(ndm=2, ndf=2)

    model.nDMaterial(*material)

    # the plane stress
    model.section('PlaneStress', 1, 1, 1.0)

    # Create a triangle patch
    model.node(1, 0, 0)
    model.node(2, 1, 0)
    model.node(3, 0, 1)
    model.element('tri31', 1,   (1, 2, 3),   section=1)

    # Create fixities
    model.fix(1,   1, 1)
    model.fix(2,   0, 1)
    model.fix(3,   1, 0)
    return model

def analyze_dir(model, dX, dY, sig0):
    dLambda = 0.02
    dLambdaMin = 0.00005

    print("Analyze direction ({:8.3g}, {:8.3g})".format(dX, dY))

    model.reset()

    # Define a simple ramp time series
    model.timeSeries('Linear', 1, '-factor', 2.0*sig0)

    # Define load pattern for imposed stresses in the given direction
    model.pattern('Plain', 1, 1)
    model.load(2,  dX, 0.0, pattern=1)
    model.load(3, 0.0,  dY, pattern=1)

    # analyze
    model.constraints('Plain') #Transformation')
    model.numberer('Plain')
    model.system('FullGeneral')
#   ops.test('NormDispIncr', 1.0e-8, 20, 0)
    model.test('NormUnbalance', 1.0e-8, 50, 0)
    model.algorithm('Newton')

    Lambda = 0.0
    sX = 0.0
    sY = 0.0
    while True:
        model.integrator('LoadControl', dLambda)
#       ops.test('NormUnbalance', 1.0e-10, 20, 0)
        model.analysis('Static')

        if model.analyze(1) == 0:
            stress = model.eleResponse(1, 'material', 1, 'stress')
            sX = stress[0]
            sY = stress[1]
            Lambda += dLambda
            if Lambda > 1.4999 : #0.99999:
                print("Max lambda")
                break
        else:
            dLambda /= 2.0
            if dLambda < dLambdaMin:
                print("Min dLam at ", Lambda)
                break

    return sX, sY

def walk_surface(material, sig0):
    # number of subdivisions
    NDiv = 300 #80
    NP = NDiv+1
    dAngle = 2.0*pi/NDiv
    SX = np.zeros(NP)
    SY = np.zeros(NP)

    for i in range(NP):
        angle = float(i)*dAngle
        dX = cos(angle)
        dY = sin(angle)

        model = create_model(material)
        sX,sY = analyze_dir(model, dX, dY, sig0)
        # TODO: shouldnt have to scale by sqrt(3)
        SX[i] = sX/(sig0*np.sqrt(3))
        SY[i] = sY/(sig0*np.sqrt(3))
    return SX, SY

def plot_surface(material, sig0):
    #
    #
    #
    plt.ion()

    fig, ax = plt.subplots(1,1)
    ax.plot(*walk_surface(["ElasticIsotropic", *material[1:4]], sig0))
    SX, SY = walk_surface(material, sig0)

#   ax.set(xlim=[-45, 10], ylim=[-45, 10])
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)
    ax.set_xlabel(r"$\sigma_1 / F_c$")
    ax.set_ylabel(r"$\sigma_2 / F_c$")
    ax.grid(linestyle=':')
    ax.set(xlim=[min(1.1*SX), 1.2*max(SX)],
           ylim=[min(1.1*SY), 1.2*max(SY)])
    ax.set_aspect('equal')#, 'box')
    ax.axis("equal")

    the_line, = ax.plot(SX, SY, '-') #, linewidth=2.0)

    for i in range(len(SX)):
        the_line.set_xdata(SX[:i])
        the_line.set_ydata(SY[:i])
        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.ioff()


if __name__ == "__main__":
    #
    E    = 30e3
    v    =  0.2
    sig0 = 15.0
    fc = sig0
    ft = fc*0.14
    et = ft/E

    # Collect arguments for defining the material
    material = [
        'FariaPlasticDamage', 1, E, v, ft, fc,
        '-beta', 0.5, '-An', 3, '-Bn', 0.75, '-Ap', 2.5
    ]

    fig, ax = plt.subplots(1,1)
    SX, SY = walk_surface(material[:6], sig0)
    ax.plot(SX, SY)
#   ax.plot(*walk_surface(material, sig0))
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)
    ax.set_xlabel(r"$\sigma_1 / F_c$")
    ax.set_ylabel(r"$\sigma_2 / F_c$")
    ax.grid(linestyle=':')
    ax.set(xlim=[1.1*min(*SX,*SY), 1.2*max(*SX, *SY)],
           ylim=[1.1*min(*SX,*SY), 1.2*max(*SX, *SY)])
    ax.axis("square")
    plt.show()


    if False:
        material = [
            'ASDConcrete3D', 1, E, v,
            '-Ce', 0.0, fc/E, fc/E+1,
            '-Cs', 0.0, fc, fc,
            '-Cd', 0.0, 0.0, 0.0,
            '-Te', 0.0, et, et+1,
            '-Ts', 0.0, ft, ft,
            '-Td', 0.0, 0.0, 0.0
        ]

        plot_surface(material, sig0)
        plt.show()

