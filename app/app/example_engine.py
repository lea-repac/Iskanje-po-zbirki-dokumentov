from __future__ import annotations

from collections import Counter
from math import sqrt
from pathlib import Path
from typing import Any, Dict, List
import re

WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)


def tokenize(text: str) -> List[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]



def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    common = set(vec_a) & set(vec_b)
    numerator = sum(vec_a[w] * vec_b[w] for w in common)
    norm_a = sqrt(sum(v * v for v in vec_a.values()))
    norm_b = sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return numerator / (norm_a * norm_b)



def build_vector(tokens: List[str], weighted: bool) -> Dict[str, float]:
    counts = Counter(tokens)
    if weighted:
        return {word: float(count) for word, count in counts.items()}
    return {word: 1.0 for word in counts}



def search_documents(
    document_paths: List[str],
    weighted: bool,
    k: int,
    cosine_threshold: float,
    query: str,
) -> Dict[str, Any]:
    """
    Preprost delujoč primer, da aplikacija že zdaj dela.
    To NI tvoj polni SVD sistem, ampak samo demonstracija vmesnika.
    """
    query_tokens = tokenize(query)
    query_vector = build_vector(query_tokens, weighted=weighted)

    results: List[Dict[str, Any]] = []
    unreadable: List[str] = []

    for path_str in document_paths:
        path = Path(path_str)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                text = path.read_text(encoding="latin-1")
            except Exception:
                unreadable.append(path_str)
                continue
        except Exception:
            unreadable.append(path_str)
            continue

        doc_tokens = tokenize(text)
        doc_vector = build_vector(doc_tokens, weighted=weighted)
        score = cosine_similarity(query_vector, doc_vector)

        if score >= cosine_threshold:
            results.append({"path": str(path), "score": score})

    results.sort(key=lambda item: item["score"], reverse=True)

    if k > 0:
        results = results[:k]

    messages: List[str] = []
    messages.append(
        f"Način matrike: {'utežena' if weighted else 'neutežena'}"
    )
    messages.append("Ta primer trenutno uporablja osnovno kosinusno podobnost brez SVD.")

    if unreadable:
        messages.append(f"Nekaterih datotek ni bilo mogoče prebrati: {len(unreadable)}")

    return {
        "results": results,
        "messages": messages,
    }
