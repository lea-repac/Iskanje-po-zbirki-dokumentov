import numpy as np


def preberi_dokumente(stevilo_dokumentov):
    dokumenti = []
    
    for i in range(1, stevilo_dokumentov + 1):
        ime_datoteke = f"dokument{i:02d}.txt" #i:02d - i število indeksa, 0 - vodilne ničle, 2 - koliko mest more številka zapolnit
        
        with open(ime_datoteke, "r", encoding="utf-8") as f:
            dokumenti.append(f.read())
    
    return dokumenti


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
dokumenti = preberi_dokumente(10)
#važno samo da dobimo A, ampak za testiranje sem dala še besede in indeks besede
A, besede, indeks_besed = zgradi_matriko(dokumenti)

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