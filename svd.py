import numpy as np
import izgradnjaMatrike as im

"""
vrne razcep matrike A na U, S in V
    U - besede v prostoru konceptov
    S - pomembnost konceptov
    V(transponirano) - dokumenti v prostoru konceptov (vrstice so teme, stolpci pa dokumenti)
"""
def SVD(A):
    #dobimo osnoven svd - 
    u, s, v = np.linalg.svd(A, full_matrices=False)
   
    """
    print("U: ")
    print(U)

    print("S: ")
    print(S)

    print("V: ")
    print(V)
    """

    return u, s, v