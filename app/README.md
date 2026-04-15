# Python aplikacija za iskanje po dokumentih

Ta verzija je **lokalna Python aplikacija** brez spletnega strežnika.

## Datoteke
- `app.py` – grafični vmesnik (tkinter)
- `adapter.py` – vmesni sloj, kamor priključiš svojo obstoječo logiko iz `main.py`, `SVD.py`, `Q.py`
- `example_engine.py` – preprost delujoč primer iskanja, da aplikacija takoj deluje
- `requirements.txt` – dodatne odvisnosti (ni jih)

## Zagon
```bash
python app.py
```

## Kako priklopiš svoj projekt
V datoteki `adapter.py` imaš funkcijo:

```python
def run_search(document_paths, weighted, has_existing_matrices, matrix_paths, k, cosine_threshold, query):
```

Ta funkcija trenutno kliče `example_engine.search_documents(...)`.

Ko boš želela uporabiti svojo pravo logiko, v `adapter.py` zamenjaš ta del s klici iz svojih datotek `main.py`, `SVD.py`, `Q.py`.

## Kaj priporočam
V svojem projektu naredi eno glavno funkcijo, ki **ne uporablja** `input()` in `print()`, ampak sprejme parametre in vrne rezultate, na primer:

```python
def poisci_dokumente(document_paths, weighted, k, cosine_threshold, query, matrix_paths=None):
    ...
    return {
        "results": [...],
        "messages": [...],
    }
```

Potem bo povezava z GUI zelo enostavna.
