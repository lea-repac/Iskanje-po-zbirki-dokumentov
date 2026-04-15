from __future__ import annotations

from typing import Any, Dict, List

from pathlib import Path
from projekt.mainApp import poisci_dokumente


def run_search(folder_path, save_folder, weighted, k, cosine_threshold, query):
    return poisci_dokumente(
        mapa=folder_path,
        mapa_za_shranjevanje=save_folder,
        utez=weighted,
        k=int(k),
        mejna_vrednost=float(cosine_threshold),
        poizvedba=query,
    )