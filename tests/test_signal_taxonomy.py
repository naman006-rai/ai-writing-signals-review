import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "rubrics" / "signal-taxonomy.json"

REQUIRED_FIELDS = {
    "id",
    "category",
    "name",
    "description",
    "common_patterns",
    "severity_default",
    "false_positive_risk",
    "false_positive_note",
    "review_question",
    "safer_revision_advice",
}

ALLOWED_LEVELS = {"low", "medium", "high"}

# Concepts the taxonomy must cover (matched against signal ids/names/descriptions).
REQUIRED_CONCEPTS = [
    "significance",        # generic importance / legacy
    "broader",             # broader-landscape language
    "attribution",         # vague attribution
    "superficial",         # superficial analysis
    "promotional",         # promotional / press-release
    "conclusion",          # formulaic conclusions
    "vocabulary",          # high-density AI vocabulary
    "transition",          # repetitive transitions
    "parallelism",         # not only X but also Y
    "rule-of-three",       # rule of three
    "em dash",             # em dash overuse
    "over-formatting",     # over-formatting
    "boldface",            # excessive boldface
    "markdown",            # markdown leakage
    "broken citation",     # broken citation artifacts
    "malformed",           # fake / malformed citations
    "placeholder",         # placeholder text
    "chatbot",             # chatbot disclaimers
    "knowledge-cutoff",    # knowledge cutoff language
    "style or register shift",  # abrupt style shifts
    "context mismatch",    # context mismatch
]


def load_taxonomy():
    return json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))


def test_taxonomy_json_is_valid():
    taxonomy = load_taxonomy()
    assert taxonomy["name"]
    assert isinstance(taxonomy["signals"], list)
    assert taxonomy["signals"]


def test_each_signal_has_required_fields():
    taxonomy = load_taxonomy()
    for signal in taxonomy["signals"]:
        missing = REQUIRED_FIELDS - set(signal)
        assert not missing, f"{signal.get('id', '<missing id>')} missing {missing}"
        for field in REQUIRED_FIELDS:
            assert signal[field] != "" and signal[field] is not None, (
                f"{signal['id']} has empty {field}"
            )


def test_common_patterns_is_a_list():
    taxonomy = load_taxonomy()
    for signal in taxonomy["signals"]:
        assert isinstance(signal["common_patterns"], list), (
            f"{signal['id']} common_patterns must be a list"
        )


def test_ids_are_unique():
    taxonomy = load_taxonomy()
    ids = [signal["id"] for signal in taxonomy["signals"]]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert not duplicates, f"Duplicate signal ids: {duplicates}"


def test_categories_are_from_allowed_set():
    taxonomy = load_taxonomy()
    categories = set(taxonomy["categories"])
    for signal in taxonomy["signals"]:
        assert signal["category"] in categories, (
            f"{signal['id']} has unknown category {signal['category']}"
        )


def test_severity_values_are_valid():
    taxonomy = load_taxonomy()
    for signal in taxonomy["signals"]:
        assert signal["severity_default"] in ALLOWED_LEVELS, (
            f"{signal['id']} has invalid severity_default {signal['severity_default']}"
        )


def test_false_positive_risk_values_are_valid():
    taxonomy = load_taxonomy()
    for signal in taxonomy["signals"]:
        assert signal["false_positive_risk"] in ALLOWED_LEVELS, (
            f"{signal['id']} has invalid false_positive_risk {signal['false_positive_risk']}"
        )


def test_false_positive_notes_are_present():
    taxonomy = load_taxonomy()
    for signal in taxonomy["signals"]:
        note = signal["false_positive_note"].lower()
        assert "human" in note or "false positive" in note
        assert "proof" in note or "authorship" in note


def test_no_category_is_empty():
    taxonomy = load_taxonomy()
    categories = set(taxonomy["categories"])
    counts = {category: 0 for category in categories}
    for signal in taxonomy["signals"]:
        counts[signal["category"]] += 1
    empty = [category for category, count in counts.items() if count == 0]
    assert not empty, f"Empty categories: {empty}"


def test_includes_human_writing_and_ineffective_categories():
    taxonomy = load_taxonomy()
    present = {signal["category"] for signal in taxonomy["signals"]}
    assert "human_writing" in present
    assert "ineffective_indicators" in present


def test_required_concepts_are_covered():
    taxonomy = load_taxonomy()
    blob = json.dumps(taxonomy["signals"]).lower()
    missing = [concept for concept in REQUIRED_CONCEPTS if concept.lower() not in blob]
    assert not missing, f"Taxonomy missing required concepts: {missing}"


def test_allowed_values_metadata_present():
    taxonomy = load_taxonomy()
    allowed = taxonomy.get("allowed_values", {})
    assert set(allowed.get("severity_default", [])) == ALLOWED_LEVELS
    assert set(allowed.get("false_positive_risk", [])) == ALLOWED_LEVELS
