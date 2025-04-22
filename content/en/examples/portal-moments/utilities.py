
import numpy as np

class MatrixAnalysis:
    def __init__(self, model):
        self._model = model

    def Q_vector(self):
        model = self._model
        Q = np.array([
            model.eleResponse(element, "basicForces") for element in model.getEleTags()
        ]).flatten()

        return np.round(Q, 4)


def create_field(model,  artist):
    ndm = artist.model.ndm
    ndf = 3 if ndm == 2 else 6

    def field(tag, x):
        wy  = -10 if tag == 2 else (-5 if tag == 1 else 0)
        wz  =  -1 if tag == 1 else 0

        X = artist.model.cell_position(tag)
        L = np.linalg.norm(X[-1] - X[0])

        if not artist.model.cell_matches(tag, "prism"):
            M = model.eleResponse(tag, "section", x+1, "forces")[3:6]
            return M

        else:
            q = model.eleResponse(tag, "basicForces")


            if ndm == 3:
                w  = np.array([   0 ,  wz ,  wy ])
                qi = np.array([-q[3], q[4], q[1]])
                qj = np.array([ q[3], q[5], q[2]])
            else:
                w  = np.array([0, 0,  wy ])
                qi = np.array([0, 0, q[1]])
                qj = np.array([0, 0, q[2]])

            return (qi*(x-1) + qj*x + (1-x)*x * w * L*L/2)

    return field
