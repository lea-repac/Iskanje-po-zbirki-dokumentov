import numpy as np
import izgradnjaMatrike as im

st_dokumentov = 10

def singularValueDecomposition(k):
    dokumenti = im.preberi_dokumente(st_dokumentov)
    A, besede, ind_besed = im.zgradi_matriko(dokumenti)
    
    #dobimo osnoven svd
    u, s, v = np.linalg.svd(A)

    #odrezemo na k
    U = u[:, :k]
    V = v[:k, :]

    #s je treba malo drugače, ker svd vraca samo vektor s singularnimi vrednostmi
    S = np.diag(s[:k])

    return U, S, V
