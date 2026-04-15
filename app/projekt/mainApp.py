import numpy as np
import pickle
from pathlib import Path

from . import izgradnjaMatrike as im
from . import svd
from . import Q


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

    # izračun SVD
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


def matrike_obstajajo(pot_A, pot_podatki, pot_U, pot_S, pot_Vt, utez):
    """
    Vrne True, če v mapi že obstajajo vse potrebne datoteke za izbrano uteženost.
    Za uteženo morata obstajati tudi G.npy in ustrezna uteženost v pickle datoteki.
    """
    if not (pot_A.exists() and pot_podatki.exists() and pot_U.exists() and pot_S.exists() and pot_Vt.exists()):
        return False

    try:
        with open(pot_podatki, "rb") as f:
            data = pickle.load(f)

        shranjena_utezenost = data.get("utezenost", None)

        if shranjena_utezenost != utez:
            return False

        if utez:
            pot_G = pot_A.parent / "G.npy"
            if not pot_G.exists():
                return False

    except Exception:
        return False

    return True


def poisci_dokumente(
    mapa,
    mapa_za_shranjevanje,
    utez,
    k,
    mejna_vrednost,
    poizvedba
):
    """
    Glavna funkcija za GUI.

    mapa = mapa z .txt dokumenti
    mapa_za_shranjevanje = kam shranimo / od koder beremo matrike
    """

    mapa = Path(mapa)
    shramba = Path(mapa_za_shranjevanje)

    if not mapa.exists():
        raise FileNotFoundError(f"Mapa z dokumenti ne obstaja: {mapa}")

    if not mapa.is_dir():
        raise NotADirectoryError(f"Podana pot ni mapa: {mapa}")

    # ustvarimo mapo za shranjevanje
    shramba.mkdir(parents=True, exist_ok=True)

    # poti do datotek
    pot_A = shramba / "A.npy"
    pot_G = shramba / "G.npy"
    pot_U = shramba / "U.npy"
    pot_S = shramba / "S.npy"
    pot_Vt = shramba / "Vt.npy"
    pot_podatki = shramba / "ostali_podatki.pkl"

    sporocila = []

    # Če matrike ne obstajajo, jih izračunamo.
    if not matrike_obstajajo(pot_A, pot_podatki, pot_U, pot_S, pot_Vt, utez):
        sporocila.append("Matrike niso bile najdene ali ne ustrezajo nastavitvam. Generiram nove matrike ...")
        shrani_podatke(
            pot_A, pot_G, pot_podatki, pot_U, pot_S, pot_Vt, mapa, utez
        )
    else:
        sporocila.append("Obstoječe matrike so bile najdene. Uporabljam shranjene matrike ...")

    with open(pot_podatki, "rb") as f:
        data = pickle.load(f)

    utezenost = data["utezenost"]
    slovar = data["slovar"]

    G, A, u, s, vt = beri_matrike(pot_A, pot_G, pot_U, pot_S, pot_Vt)

    # preverjanje parametrov
    if k <= 0:
        raise ValueError("Vrednost k mora biti večja od 0.")

    max_k = min(len(s), u.shape[1], vt.shape[0])
    if k > max_k:
        raise ValueError(f"k je prevelik (max = {max_k})")

    if not (0 <= mejna_vrednost <= 1):
        raise ValueError("Meja kosinusa mora biti med 0 in 1.")

    # odrezani SVD
    U = u[:, :k]
    Vt = vt[:k, :]
    S = np.diag(s[:k])

    # poizvedba
    q = Q.zgradiVektorPoizvedbe(poizvedba, slovar, utezenost, G)
    q = Q.zgradiVektorDokumentov(q, U, S)

    V = np.transpose(Vt)

    iskani = Q.najdiDokumente(q, V, mejna_vrednost)

    # imena datotek
    datoteke = sorted([p.name for p in mapa.glob("*.txt")])

    rezultati = []
    for idx in iskani:
        idx_int = int(idx)

        zapis = {
            "indeks": idx_int
        }

        # Q.najdiDokumente vrača indekse od 1 naprej
        seznam_index = idx_int - 1

        if 0 <= seznam_index < len(datoteke):
            zapis["datoteka"] = datoteke[seznam_index]
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
        "mapa_za_shranjevanje": str(shramba),
        "messages": sporocila
    }