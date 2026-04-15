import numpy as np

"""
vrne poizvedbo zapisano v vektroju frekvenc - vse besede iz zbirke imajo frekvence v poizvedbi
"""
def zgradiVektorPoizvedbe(query, slovar, utezeno, G):
    query = query.lower()
    for char in ".,!?;:":
        query = query.replace(char, "")
    query = query.split()

    q = np.zeros(len(slovar))
    
    for word in query:
        if word in slovar:
            indeks = slovar.get(word)
            q[indeks] += 1
    
    if not utezeno:
        return q

    #ce je utezeno, vrne drugacen vektor
    f_q = q
    L_q = np.log(f_q + 1.0)
    q = L_q * G

    return q


"""
vrne vektor, ki za vsako besedo, ki se pojavi v zbirki hrani frekvenco pojavitve v poizvedbi
"""
def zgradiVektorDokumentov(q, U, S):
    S1 = np.linalg.inv(S)

    q = q @ U @ S1

    return q

"""
vrne kosinus (float) med vektorjem dokumentov in enim od stolpcev transponirane matrike V
"""
def kosinus(a, b):
    skalar = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        kos = 0
    else:
        kos = skalar / (norm_a * norm_b)
    return kos

"""
vrne indekse dokumentov, katerih stolpci v transponirani matriki V so vektorju dokumentov dovolj blizu (vsaj toliko, da je kosinusa kota med njimi vecji od izbrane mejne vrednosti)
"""
def najdiDokumente(q, V, mejna_vrednost):
    n = len(V)
    kosinusi = np.zeros(n)
    for i in range(n):
        kosinusi[i] = kosinus(q, V[i])
    #print(kosinusi)

    iskani = []
    for i in range(len(kosinusi)):
        if kosinusi[i] > mejna_vrednost:
            iskani.append(i + 1)

    return iskani