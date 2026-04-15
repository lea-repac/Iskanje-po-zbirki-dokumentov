from __future__ import annotations

from typing import Any, Dict, List

from pathlib import Path
from projekt.mainApp import poisci_dokumente


def run_search(folder_path, weighted, has_existing_matrices, matrix_paths, k, cosine_threshold, query):
    # A, S in G zaenkrat ignoriramo

    rezultat = poisci_dokumente(
        mapa=folder_path,
        utez=weighted,
        k=int(k),
        mejna_vrednost=float(cosine_threshold),
        poizvedba=query,
        prisili_ponovni_izracun=False
    )

    return rezultat