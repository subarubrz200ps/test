from app.evaluator import SearchItem, evaluate


def test_empty_items_returns_zeroes():
    result = evaluate([])
    assert result["overall"] == 0
    assert result["details"] == []


def test_evidence_hierarchy_prefers_meta_analysis_over_rct():
    items = [
        SearchItem(
            title="Exercise therapy meta-analysis for low back pain",
            snippet="Systematic review and meta-analysis",
            url="https://www.bmj.com/example",
        ),
        SearchItem(
            title="Exercise therapy randomized controlled trial",
            snippet="single-center RCT",
            url="https://www.example.com/rct",
        ),
    ]

    result = evaluate(items)
    details = result["details"]
    assert details[0]["evidence"] >= details[1]["evidence"]


def test_authority_scoring_favors_gov_over_commercial():
    items = [
        SearchItem(
            title="Public health guideline",
            snippet="guideline",
            url="https://www.nih.gov/news-events",
        ),
        SearchItem(
            title="Blog health tips",
            snippet="expert opinion",
            url="https://example.com/health-tips",
        ),
    ]

    result = evaluate(items)
    urls_by_total = [d["url"] for d in result["details"]]
    assert urls_by_total[0] == "https://www.nih.gov/news-events"


def test_details_include_reasons_for_explainability():
    items = [
        SearchItem(
            title="Cohort study on rehabilitation",
            snippet="cohort",
            url="https://www.ncbi.nlm.nih.gov/pubmed/123",
        )
    ]

    result = evaluate(items)
    reasons = result["details"][0]["reasons"]
    assert set(reasons.keys()) == {"authority", "consensus", "evidence"}


def test_deterministic_output_for_same_input():
    items = [
        SearchItem(
            title="WHO guideline",
            snippet="guideline",
            url="https://www.who.int/path",
        ),
        SearchItem(
            title="NIH RCT summary",
            snippet="randomized controlled trial",
            url="https://www.nih.gov/path",
        ),
    ]

    first = evaluate(items)
    second = evaluate(items)
    assert first == second
