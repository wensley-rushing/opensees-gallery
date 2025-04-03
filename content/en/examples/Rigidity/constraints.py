import sympy as sp
import numpy as np
import pandas as pd

def add_constraints(A, ic, iu=None):
    ir = np.arange(len(A))
    ir = np.delete(ir, ic)

    ii = np.arange(len(A[0]))
    if iu is not None:
        ii = [*map(int,np.setdiff1d(ii, iu)), *iu]
    print(ii)

    A = sp.Matrix(A)

    Ao = sp.Matrix( A[ic, :])

    n,m = Ao.shape
    no = m - Ao.rank()
    M = sp.Matrix(sp.BlockMatrix([Ao.T, sp.eye(m)]))

    Rref, idx = M.rref()
    print(f"{idx = }")
    R = np.array(Rref)
   #  R[:,ii] = Rref[:,-m:]
    print(pd.DataFrame(np.array(R)))

    print(f"{no = }, {m = }")
    Uo = R[-no:,-m:].T
    print("Uo = ")
    print(pd.DataFrame(np.array(Uo)))

    Atilde = (A * Uo)
    print(pd.DataFrame(np.array(Atilde)))


if __name__ == "__main__":
# A =[[-1 / 4 , 0 , 0 , 0 , 0 , 0 , 0 ],
#     [-1 / 4 , 1 , 0 , 0 , 0 , 0 , 0 ],
#     [  -0.6 , 0 , 0.8 , 0.6 , 0 , 0 , 0 ],
#     [ 0.8/5 , 1 , 0.6/5 , -0.8/5 , 0 , 0 , 0 ],
#     [ 0.8/5 , 0 , 0.6/5 , -0.8/5 , 1 , 0 , 0 ],
#     [ 0 , 0 , -0.6 , 0.8 , 0 , 0.6 , 0 ],
#     [ 0 , 0 , 0.8 / 5 , 0.6 / 5 , 1 , -0.8 / 5 , 0 ],
#     [ 0 , 0 , 0.8 / 5 , 0.6 / 5 , 0 , -0.8 / 5 , 1 ],
#     [ 0 , 0 , 0 , 0 , 0 , 1 / 4 , 1 ],
#     [ 0 , 0 , 0 , 0 , 0 , 1 / 4 , 0]]
# 
# ic = slice(2, -2)


    A = [
        [ -1/8 , 1 ,    0 , 0 , 0 ],
        [    0 , 1 ,  1/6 , 0 , 0 ],
        [    0 , 0 ,  1/6 , 1 , 0 ],
        [  0.6 , 0 , -0.8 , 0 , 0.8 ],
        [0.8/5 , 0 , 0.6/5, 1 , -0.6 / 5 ],
        [  0.6 , 0 ,  0.8 , 0 , 0 ],
        [ -0.6 , 0 ,    0 , 0 , 0.8]]

    add_constraints(A, [0, 3, 4], [0, 4])

   #  print(A@np.array([1, 1/8, 3/4, -1/4, 0]))


