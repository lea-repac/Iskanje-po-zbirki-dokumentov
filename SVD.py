import numpy as np
import izgradnjaMatrike as im

"""
vrne razcep matrike A na U, S in V
    U - besede v prostoru konceptov
    S - pomembnost konceptov
    V(transponirano) - dokumenti v prostoru konceptov (vrstice so teme, stolpci pa dokumenti)
"""
def SVD(k, A):
    #dobimo osnoven svd - 
    u, s, v = np.linalg.svd(A)

    #odrezemo na k
    U = u[:, :k]
    Vt = v[:k, :]

    #s je treba malo drugače, ker svd vraca samo vektor s singularnimi vrednostmi
    S = np.diag(s[:k])
   
    """
    print("U: ")
    print(U)

    print("S: ")
    print(S)

    print("V: ")
    print(V)
    """

    return U, S, Vt