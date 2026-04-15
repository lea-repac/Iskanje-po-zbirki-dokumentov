import numpy as np
from pathlib import Path
import os

def preberi_dokumente(pot_do_dokumentov):
    dokumenti = []
    imena = []
    
    for datoteka in sorted(pot_do_dokumentov.glob("*.txt")):
            dokumenti.append(datoteka.read_text(encoding="utf-8"))
            imena.append(datoteka.name)
    
    return dokumenti, imena


def zgradi_matriko(dokumenti):
    def razdeli_na_besede(besedilo):
        besedilo = besedilo.lower()
        besedilo = besedilo.replace(".", "")
        besedilo = besedilo.replace(",", "")
        besedilo = besedilo.replace("!", "")
        besedilo = besedilo.replace("?", "")
        
        return besedilo.split()
    #vsak dokument je seznam besed zdaj
    besede_v_seznamu = [razdeli_na_besede(dokument) for dokument in dokumenti]

    # vse unikatne besede (set da se znebimo podvojitev, dorted da )
    vse = []
    for dokument in besede_v_seznamu:
        for b in dokument:
            vse.append(b)
    vse_besede = sorted(set(vse))

    indeks_besed = {}
    for i, b in enumerate(vse_besede):
        indeks_besed[b] = i


    # matrika (besede x dokumenti)
    A = np.zeros((len(vse_besede), len(dokumenti)), dtype=int)

    for j, dokument in enumerate(besede_v_seznamu):
        for beseda in dokument:
            i = indeks_besed[beseda]
            A[i, j] += 1

    return A, vse_besede, indeks_besed


# preberi dokumente
#dokumenti = preberi_dokumente(10)
#važno samo da dobimo A, ampak za testiranje sem dala še besede in indeks besede
#A, besede, indeks_besed = zgradi_matriko(dokumenti)

"""
#ta izpis je samo za preverjanje, da je vse delovalo pravilno
print("Vse besede:")
print(besede)

print("\nIndeks besed:")
print(indeks_besed)

print("\nMatrika A:")
print(A)

print("\nFrekvence po besedah:")
for i, beseda in enumerate(besede):
    print(beseda, A[i])

"""


def zgradi_matriko_utezeno(dokumenti):
    """
    4. točka:
    a_ij = L_ij * G_i
    L_ij = log(f_ij + 1) #kako pomembna je beseda v tem dokumnetu
    G_i = 1 - sum_j(p_ij log(p_ij)) / log(n) #kako pomembna je beseda v vseh dokumentih
    p_ij = f_ij / gf_i
    """
    F, vse_besede, indeks_besed = zgradi_matriko(dokumenti)

    m, n = F.shape  # m = št. besed, n = št. dokumentov F.shape=(število_vrstic, število_stolpcev)

    L = np.log(F + 1.0)

    # globalna frekvenca posamezne besede čez vse dokumente
    gf = np.sum(F, axis=1)  # shape (m,) #za vsako besedo (vrstico) seštej vse stolpce

    G = np.zeros(m, dtype=float)

    if n == 1:
        # da se izognemo deljenju z log(1)=0
        G[:] = 1.0
    else:
        for i in range(m):
            if gf[i] == 0:
                G[i] = 0.0
                continue

            p = F[i, :] / gf[i]      # p_ij za fiksno besedo i (frekvenca besede deljeno s kolikokrat se pojavi vseh dokumentih)
            p_nonzero = p[p > 0]     # 0 * log(0) obravnavamo kot 0 ker log(0) ne obstaja

            entropija = -np.sum(p_nonzero * np.log(p_nonzero)) / np.log(n)
            G[i] = 1.0 - entropija

    # vsako vrstico L pomnožimo z ustreznim G_i
    A_utezena = L * G[:, np.newaxis]

    return A_utezena, vse_besede, indeks_besed, G


#def vrni_besede(stevilo_dokumentov=10, utezena=True):
    dokumenti = preberi_dokumente(stevilo_dokumentov)

    if utezena:
        _, besede, _ = zgradi_matriko_utezeno(dokumenti)
    else:
        _, besede, _ = zgradi_matriko(dokumenti)

    return besede
