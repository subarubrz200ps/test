from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from urllib.parse import urlparse


@dataclass
class SearchItem:
    title: str
    snippet: str
    url: str


AUTHORITY_DOMAIN_SCORES = {
    "gov": 95,
    "go.jp": 95,
    "ac.jp": 90,
    "edu": 85,
    "who.int": 95,
    "nih.gov": 95,
    "ncbi.nlm.nih.gov": 95,
    "cochranelibrary.com": 92,
    "thelancet.com": 92,
    "nejm.org": 92,
    "bmj.com": 90,
}

# Evidence pyramid-inspired mapping.
# Higher score => stronger evidence type.
EVIDENCE_KEYWORDS = {
    "meta-analysis": 100,
    "systematic review": 95,
    "guideline": 90,
    "randomized controlled trial": 85,
    "rct": 85,
    "cohort": 70,
    "case-control": 65,
    "case report": 45,
    "expert opinion": 35,
}


def _domain_score(url: str) -> tuple[int, str]:
    host = urlparse(url).netloc.lower()
    for key, score in AUTHORITY_DOMAIN_SCORES.items():
        if host.endswith(key) or key in host:
            return score, f"recognized authoritative domain pattern: {key}"
    if host.endswith(".org"):
        return 68, "non-profit/org domain heuristic"
    if host.endswith(".com"):
        return 55, "commercial domain heuristic"
    return 50, "unknown domain fallback heuristic"


def _evidence_score(text: str) -> tuple[int, str]:
    lowered = text.lower()
    matched = [(kw, score) for kw, score in EVIDENCE_KEYWORDS.items() if kw in lowered]
    if not matched:
        return 40, "no explicit evidence-level keyword detected"

    keyword, score = max(matched, key=lambda x: x[1])
    return score, f"matched evidence keyword: {keyword}"


def _tokenize(text: str) -> set[str]:
    cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
    return {t for t in cleaned.split() if len(t) > 2}


def _consensus_scores(items: list[SearchItem]) -> tuple[list[int], list[str]]:
    token_sets = [_tokenize(f"{item.title} {item.snippet}") for item in items]
    scores: list[int] = []
    reasons: list[str] = []

    for i, current in enumerate(token_sets):
        if not current:
            scores.append(0)
            reasons.append("no tokens extracted for consensus comparison")
            continue

        similarities = []
        for j, other in enumerate(token_sets):
            if i == j:
                continue
            inter = len(current & other)
            union = len(current | other)
            if union == 0:
                continue
            similarities.append(inter / union)

        avg = mean(similarities) if similarities else 0
        scores.append(int(avg * 100))
        reasons.append(f"average pairwise token overlap={avg:.2f}")

    return scores, reasons


def evaluate(items: list[SearchItem]) -> dict:
    if not items:
        return {
            "overall": 0,
            "authority": 0,
            "consensus": 0,
            "evidence": 0,
            "details": [],
        }

    consensus_per_item, consensus_reasons = _consensus_scores(items)
    details = []
    authority_scores = []
    evidence_scores = []

    for item, consensus, consensus_reason in zip(items, consensus_per_item, consensus_reasons):
        authority, authority_reason = _domain_score(item.url)
        evidence, evidence_reason = _evidence_score(f"{item.title} {item.snippet}")
        total = round(0.4 * authority + 0.3 * consensus + 0.3 * evidence, 1)

        authority_scores.append(authority)
        evidence_scores.append(evidence)

        details.append(
            {
                "title": item.title,
                "url": item.url,
                "authority": authority,
                "consensus": consensus,
                "evidence": evidence,
                "total": total,
                "reasons": {
                    "authority": authority_reason,
                    "consensus": consensus_reason,
                    "evidence": evidence_reason,
                },
            }
        )

    authority_avg = round(mean(authority_scores), 1)
    consensus_avg = round(mean(consensus_per_item), 1)
    evidence_avg = round(mean(evidence_scores), 1)
    overall = round(0.4 * authority_avg + 0.3 * consensus_avg + 0.3 * evidence_avg, 1)

    return {
        "overall": overall,
        "authority": authority_avg,
        "consensus": consensus_avg,
        "evidence": evidence_avg,
        "details": sorted(details, key=lambda d: d["total"], reverse=True),
    }
