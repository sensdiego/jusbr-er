#!/usr/bin/env python3
"""JusBR-ER Baseline Evaluation — Standalone (no external dependencies).

Evaluates a Jaro-Winkler baseline on the JusBR-ER benchmark.
No external packages required beyond Python 3.8+ stdlib.

Usage:
    python eval_baseline.py --dataset jusbr_er_v1.json

Released under CC BY-NC-SA 4.0.
Citation: Sens, D. (2026). JusBR-ER: A Benchmark for Entity Resolution
of Legal Concepts in Brazilian Portuguese. NLLP Workshop at EMNLP 2026.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

# ── Normalization ────────────────────────────────────────────────────────────

_LEGAL_EXPANSIONS = [
    (re.compile(r"\bart\.?\s*"), "artigo "),
    (re.compile(r"\barts\.?\s*"), "artigos "),
    (re.compile(r"\b§\s*"), "paragrafo "),
    (re.compile(r"\b§§\s*"), "paragrafos "),
    (re.compile(r"\binc\.?\s*"), "inciso "),
    (re.compile(r"\bcf\b"), "constituicao federal"),
    (re.compile(r"\bcdc\b"), "codigo de defesa do consumidor"),
    (re.compile(r"\bcc\b"), "codigo civil"),
    (re.compile(r"\bcpc\b"), "codigo de processo civil"),
    (re.compile(r"\bcp\b"), "codigo penal"),
    (re.compile(r"\bcpp\b"), "codigo de processo penal"),
    (re.compile(r"\bclt\b"), "consolidacao das leis do trabalho"),
    (re.compile(r"\bctn\b"), "codigo tributario nacional"),
    (re.compile(r"\bect\b"), "estatuto da crianca e do adolescente"),
    (re.compile(r"\blef\b"), "lei de execucao fiscal"),
    (re.compile(r"\bn[°º]\.?\s*"), "numero "),
]

_ROMAN_MAP = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5",
    "vi": "6", "vii": "7", "viii": "8", "ix": "9", "x": "10",
    "xi": "11", "xii": "12", "xiii": "13", "xiv": "14", "xv": "15",
    "xvi": "16", "xvii": "17", "xviii": "18", "xix": "19", "xx": "20",
}


def _remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize(name: str) -> str:
    """Normalize a legal concept name for comparison."""
    text = name.lower().strip()
    text = _remove_accents(text)
    for pattern, replacement in _LEGAL_EXPANSIONS:
        text = pattern.sub(replacement, text)
    tokens = text.split()
    tokens = [_ROMAN_MAP.get(t, t) for t in tokens]
    text = " ".join(tokens)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[,;.\-\u2013\u2014]+|[,;.\-\u2013\u2014]+$", "", text).strip()
    return text


# ── Jaro-Winkler ────────────────────────────────────────────────────────────

def jaro_winkler(s1: str, s2: str, p: float = 0.1) -> float:
    """Compute Jaro-Winkler similarity between two strings."""
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len_s1, len_s2 = len(s1), len(s2)
    max_dist = max(len_s1, len_s2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len_s1
    s2_matches = [False] * len_s2
    matches = 0
    transpositions = 0

    for i in range(len_s1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len_s2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len_s1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro = (matches / len_s1 + matches / len_s2 + (matches - transpositions / 2) / matches) / 3
    prefix_len = 0
    for i in range(min(4, len_s1, len_s2)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    return jaro + prefix_len * p * (1 - jaro)


# ── Qualifier Guard ──────────────────────────────────────────────────────────

_OPPOSITE_QUALIFIERS = [
    {"objetivo", "subjetivo"}, {"objetiva", "subjetiva"},
    {"moral", "material"},
    {"urgencia", "evidencia"},
    {"sucumbenciais", "contratuais"},
    {"absoluta", "relativa"}, {"absoluto", "relativo"},
    {"positiva", "negativa"}, {"positivo", "negativo"},
    {"direta", "indireta"}, {"direto", "indireto"},
    {"simples", "qualificada"}, {"simples", "qualificado"},
    {"ativa", "passiva"}, {"ativo", "passivo"},
    {"parcial", "total"},
    {"originaria", "derivada"}, {"originario", "derivado"},
]

_NUMBERS_RE = re.compile(r"\d+")


def qualifiers_differ(a: str, b: str) -> bool:
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    diff = words_a.symmetric_difference(words_b)
    if not diff:
        return False
    return any(diff == pair or diff.issubset(pair) for pair in _OPPOSITE_QUALIFIERS)


def numbers_differ(a: str, b: str) -> bool:
    nums_a = set(_NUMBERS_RE.findall(a))
    nums_b = set(_NUMBERS_RE.findall(b))
    return bool(nums_a and nums_b and nums_a != nums_b)


# ── Evaluation ───────────────────────────────────────────────────────────────

def evaluate(pairs: list[dict], jw_threshold: float = 0.88, use_guard: bool = True) -> dict:
    """Evaluate JW baseline with optional qualifier guard."""
    tp = fp = fn = tn = 0

    for p in pairs:
        norm_a = normalize(p["entity_a"])
        norm_b = normalize(p["entity_b"])
        jw = jaro_winkler(norm_a, norm_b)

        blocked = False
        if use_guard:
            blocked = qualifiers_differ(norm_a, norm_b) or numbers_differ(norm_a, norm_b)

        predicted = "merge" if jw >= jw_threshold and not blocked else "no_merge"
        actual = p["decision"]

        if actual == "merge" and predicted == "merge":
            tp += 1
        elif actual == "no_merge" and predicted == "merge":
            fp += 1
        elif actual == "merge" and predicted == "no_merge":
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "threshold": jw_threshold,
        "qualifier_guard": use_guard,
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round((tp + tn) / (tp + fp + fn + tn), 4),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="JusBR-ER Baseline Evaluation")
    parser.add_argument("--dataset", default="jusbr_er_v1.json")
    parser.add_argument("--threshold", type=float, default=0.88)
    parser.add_argument("--no-guard", action="store_true")
    parser.add_argument("--sweep", action="store_true", help="Run threshold sweep 0.70-0.95")
    args = parser.parse_args()

    with open(args.dataset) as f:
        data = json.load(f)
    pairs = data["pairs"]
    print(f"JusBR-ER: {len(pairs)} pairs ({sum(1 for p in pairs if p['decision']=='merge')}m / {sum(1 for p in pairs if p['decision']=='no_merge')}n)")

    if args.sweep:
        print(f"\n{'Threshold':>9s} {'P':>7s} {'R':>7s} {'F1':>7s}")
        print("-" * 35)
        for t in [0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.95]:
            m = evaluate(pairs, t, not args.no_guard)
            print(f"{t:>9.2f} {m['precision']:>7.1%} {m['recall']:>7.1%} {m['f1']:>7.1%}")
    else:
        m = evaluate(pairs, args.threshold, not args.no_guard)
        print(f"\nResults (JW >= {args.threshold}, guard={'off' if args.no_guard else 'on'}):")
        print(f"  Precision: {m['precision']:.1%}")
        print(f"  Recall:    {m['recall']:.1%}")
        print(f"  F1:        {m['f1']:.1%}")
        print(f"  Accuracy:  {m['accuracy']:.1%}")
        print(f"  Confusion: TP={m['tp']} FP={m['fp']} FN={m['fn']} TN={m['tn']}")


if __name__ == "__main__":
    main()
