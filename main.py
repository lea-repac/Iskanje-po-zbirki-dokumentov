import numpy as np
import izgradnjaMatrike as im
import SVD
import Q

def main():
    stevilo_dokumentov = int(input("Vnesite stevilo dokumentov v zbirki: "))

    k = int(input("Vnesite vrednost k: "))
    mejna_vrednost = float(input("Vnesite mejno vrednost kosinusa: "))
    
    dokumenti = im.preberi_dokumente(stevilo_dokumentov)
    A, vse_besede, indeks_besed = im.zgradi_matriko_utezeno(dokumenti)

    U, S, Vt = SVD.SVD(k, A)

    poizvedba = input("Vnesite iskalni niz: ")
    
    q = Q.zgradiVektorPoizvedbe(poizvedba, vse_besede)
    q = Q.zgradiVektorDokumentov(q, U, S)

    V = np.transpose(Vt)

    iskani = Q.najdiDokumente(q, V, mejna_vrednost)
    print("Najbolj relevantni dokumenti so: ")
    for i in range(len(iskani)): 
        print(iskani[i])

if __name__ == "__main__":
    main()






