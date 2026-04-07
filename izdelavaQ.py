import numpy as np
import SVD as svd
import izgradnjaMatrike as im

def izgradiQ(q_in, k):
    U, S, V = svd.singularValueDecomposition(k)

    #inverz
    S1 = np.linalg.pinv(S)
    #mnozimo
    q = q_in @ U @ S1
    print(q)
    return q, V


#naredil gemini, treba preverit, ce je ok
def izracunaj_podobnost(q_hat, V):
    # q_hat: (1, k)
    # V: (n, k) - n dokumentov, k tem
    
    # 1. Izračunamo norme (dolžine) vektorjev
    q_norm = np.linalg.norm(q_hat)
    v_norms = np.linalg.norm(V, axis=1) # Norme za vsako vrstico posebej
    
    # 2. Skalarni produkt poizvedbe z vsemi dokumenti
    # q_hat @ V.T vrne vektor produktov (1, n)
    skalarni_produkti = dot_product = q_hat @ V.T
    
    # 3. Kosinusna podobnost: cos(phi) = (a * b) / (|a| * |b|)
    # Pazimo na deljenje z nič, če bi bil kakšen dokument prazen
    cos_phi = skalarni_produkti / (q_norm * v_norms)
    
    return cos_phi.flatten() # Vrne seznam kosinusov za vse dokumente

def main():
    #preberemo iskalni niz in vse besede v njem zapisemo v vektor (predpostavimo, da so v nizu samo besede)
    iskalni_niz = input().strip()
    niz = iskalni_niz.split()
    niz.sort()

    #pridobimo vse besede
    besede = im.vrni_besede()

    #ustavrimo vektor, ki nam pove ali je beseda na indeksu i vsebovana v nizu ali ne
    q = np.zeros(len(besede))
    for i in range(len(besede)):
        if besede[i] in niz:
            q[i] = 1
    
    print(q)

    #izgradimo q1
    q1, V = izgradiQ(q, 10)
    #izracunamo kosinuse do vseh stolpcev V
    kosinusi = izracunaj_podobnost(q1, V)
    print(kosinusi)

    #izpisemo samo tiste dokumente, ki imajo doloceno velik kosinus
    for i in range(len(kosinusi)):
        if(kosinusi[i] > 0.9):
            print(i)


if __name__ == "__main__":
    main()
