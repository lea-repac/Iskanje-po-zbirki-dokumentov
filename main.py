import numpy as np
import pickle
from pathlib import Path
import izgradnjaMatrike as im
import svd
import Q

def shrani_podatke(pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez):
    dokumenti = im.preberi_dokumente(Path(mapa))

    #gradnja matrik
    if utez:
        A, besede, slovar, G = im.zgradi_matriko_utezeno(dokumenti)
    else:
        A, besede, slovar = im.zgradi_matriko(dokumenti)
        G = None
    
    #shranjevanje matrik
    np.save(pot_A, A)
    if G is not None:
        np.save(pot_G, G)
    
    data = {
        "utezenost" : utez,
        "slovar" : slovar
    }
    with open(pot_podatki, "wb") as f:
        pickle.dump(data, f)

    #izracunamo SVD
    u, s, vt = svd.SVD(A)
    np.save(pot_U, u)
    np.save(pot_S, s)
    np.save(pot_Vt, vt)

def beri_matrike(pot_A, pot_G, pot_U, pot_S, pot_Vt):
    A = np.load(pot_A)
    G = None 
    if pot_G.exists():
        G = np.load(pot_G)
    
    U = np.load(pot_U)
    S = np.load(pot_S)
    Vt = np.load(pot_Vt)

    return G, A, U, S, Vt

def main():
    mapa = input("Kje se nahajajo dokumenti (vnesite pot)? ")
    

    #pot do datoteke, ki vsebuje matriko A
    pot_A = Path("A.npy")
    pot_G = Path("G.npy")
    pot_U = Path("U.npy")
    pot_S = Path("S.npy")
    pot_Vt = Path("Vt.npy")
    pot_podatki = Path("ostali_podatki.pkl")
    
    odgovor = input("Željena uteženost (u/n)? ")
    utez = odgovor.lower() == 'u'

    if not pot_podatki.exists():
        shrani_podatke(pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez)
    
    with open(pot_podatki, "rb") as f:
        data = pickle.load(f)
    utezenost = data["utezenost"]
    slovar = data["slovar"]

    if utezenost != utez:
        shrani_podatke(pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez)
        with open(pot_podatki, "rb") as f:
            data = pickle.load(f)
        utezenost = data["utezenost"]
        slovar = data["slovar"]
    
    G, A, u, s, v = beri_matrike(pot_A, pot_G, pot_U, pot_S, pot_Vt)

    k = int(input("Vnesite vrednost k: "))
    mejna_vrednost = float(input("Vnesite mejno vrednost kosinusa: "))
    
    #odrezemo na k
    U = u[:, :k]
    Vt = v[:k, :]
    #s je treba malo drugače, ker svd vraca samo vektor s singularnimi vrednostmi
    S = np.diag(s[:k])

    poizvedba = input("Vnesite iskalni niz: ")
    
    q = Q.zgradiVektorPoizvedbe(poizvedba, slovar, utezenost, G)
    #q = qT Uk S−1    
    q = Q.zgradiVektorDokumentov(q, U, S)

    V = np.transpose(Vt)

    iskani = Q.najdiDokumente(q, V, mejna_vrednost)
    print("Najbolj relevantni dokumenti so: ")
    for i in range(len(iskani)): 
        print(iskani[i])

if __name__ == "__main__":
    main()
