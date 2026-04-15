import numpy as np
import pickle
from pathlib import Path

from . import izgradnjaMatrike as im
from . import svd
from . import Q


# mapa app/
APP_MAPA = Path(__file__).resolve().parent.parent

# mapa app/shranjeno/
SHRANJENA_MAPA = APP_MAPA / "shranjeno"


def shrani_podatke(pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez):
    dokumenti = im.preberi_dokumente(Path(mapa))

    # gradnja matrik
    if utez:
        A, besede, slovar, G = im.zgradi_matriko_utezeno(dokumenti)
    else:
        A, besede, slovar = im.zgradi_matriko(dokumenti)
        G = None

    # shranjevanje matrik
    np.save(pot_A, A)

    if G is not None:
        np.save(pot_G, G)
    else:
        if pot_G.exists():
            pot_G.unlink()

    data = {
        "utezenost": utez,
        "slovar": slovar
    }

    with open(pot_podatki, "wb") as f:
        pickle.dump(data, f)

    # izračunamo SVD
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


def poisci_dokumente(
    mapa,
    utez,
    k,
    mejna_vrednost,
    poizvedba,
    prisili_ponovni_izracun=False
):
    """
    Funkcija za GUI aplikacijo.
    Vse pomožne matrike in ostali_podatki shrani v mapo app/shranjeno
    """

    mapa = Path(mapa)

    if not mapa.exists():
        raise FileNotFoundError(f"Mapa ne obstaja: {mapa}")

    if not mapa.is_dir():
        raise NotADirectoryError(f"Podana pot ni mapa: {mapa}")

    # ustvarimo mapo za shranjevanje, če še ne obstaja
    SHRANJENA_MAPA.mkdir(parents=True, exist_ok=True)

    pot_A = SHRANJENA_MAPA / "A.npy"
    pot_G = SHRANJENA_MAPA / "G.npy"
    pot_U = SHRANJENA_MAPA / "U.npy"
    pot_S = SHRANJENA_MAPA / "S.npy"
    pot_Vt = SHRANJENA_MAPA / "Vt.npy"
    pot_podatki = SHRANJENA_MAPA / "ostali_podatki.pkl"

    # če še ni podatkov ali želimo prisilno ponovno računanje
    if prisili_ponovni_izracun or not pot_podatki.exists():
        shrani_podatke(
            pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez
        )

    with open(pot_podatki, "rb") as f:
        data = pickle.load(f)

    utezenost = data["utezenost"]
    slovar = data["slovar"]

    # če uporabnik zamenja uteženost, ponovno zgradimo vse
    if utezenost != utez:
        shrani_podatke(
            pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez
        )

        with open(pot_podatki, "rb") as f:
            data = pickle.load(f)

        utezenost = data["utezenost"]
        slovar = data["slovar"]

    G, A, u, s, vt = beri_matrike(pot_A, pot_G, pot_U, pot_S, pot_Vt)

    if k <= 0:
        raise ValueError("Vrednost k mora biti večja od 0.")

    max_k = min(len(s), u.shape[1], vt.shape[0])
    if k > max_k:
        raise ValueError(f"Vrednost k je prevelika. Največja dovoljena vrednost je {max_k}.")

    if not (0 <= mejna_vrednost <= 1):
        raise ValueError("Mejna vrednost kosinusa mora biti med 0 in 1.")

    # odrezani SVD
    U = u[:, :k]
    Vt = vt[:k, :]
    S = np.diag(s[:k])

    q = Q.zgradiVektorPoizvedbe(poizvedba, slovar, utezenost, G)
    q = Q.zgradiVektorDokumentov(q, U, S)

    V = np.transpose(Vt)

    iskani = Q.najdiDokumente(q, V, mejna_vrednost)

    datoteke = sorted([p.name for p in mapa.glob("*.txt")])

    rezultati = []
    for idx in iskani:
        zapis = {
            "indeks": int(idx)
        }

        if 0 <= int(idx) < len(datoteke):
            zapis["datoteka"] = datoteke[int(idx)]
        else:
            zapis["datoteka"] = None

        rezultati.append(zapis)

    return {
        "rezultati": rezultati,
        "stevilo_rezultatov": len(rezultati),
        "uporabljena_utezenost": utezenost,
        "k": k,
        "mejna_vrednost": mejna_vrednost,
        "poizvedba": poizvedba,
        "mapa_za_shranjevanje": str(SHRANJENA_MAPA)
    }