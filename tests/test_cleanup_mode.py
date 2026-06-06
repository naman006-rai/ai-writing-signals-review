import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = ROOT / "rubrics" / "style-pattern-watchlist.json"

REQUIRED_PATTERN_FIELDS = {
    "id",
    "category",
    "pattern_name",
    "examples",
    "why_generic",
    "safer_alternative",
    "false_positive_note",
    "severity_default",
}

ALLOWED_LEVELS = {"low", "medium", "high"}


def read_text(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def load_watchlist():
    return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))


def test_watchlist_is_valid_json_with_patterns():
    data = load_watchlist()
    assert data["name"]
    assert isinstance(data["patterns"], list)
    assert data["patterns"]


def test_watchlist_pattern_fields():
    data = load_watchlist()
    for pattern in data["patterns"]:
        missing = REQUIRED_PATTERN_FIELDS - set(pattern)
        assert not missing, f"{pattern.get('id', '<no id>')} missing {missing}"
        assert isinstance(pattern["examples"], list) and pattern["examples"]
        assert pattern["severity_default"] in ALLOWED_LEVELS
        # safer framing: every pattern must carry a false-positive note
        assert pattern["false_positive_note"].strip()


def test_watchlist_ids_unique():
    data = load_watchlist()
    ids = [p["id"] for p in data["patterns"]]
    assert len(ids) == len(set(ids)), "duplicate watchlist ids"


def test_watchlist_has_safety_note_and_no_evasion():
    data = load_watchlist()
    blob = json.dumps(data).lower()
    assert "not proof of ai authorship" in blob
    assert "evade" in blob  # must explicitly disclaim detector evasion
    # must not frame patterns as outright bans
    assert "not banned" in blob or "not an ai detector" in blob


def test_watchlist_attributes_stop_slop_mit():
    data = load_watchlist()
    sources = data.get("sources", [])
    titles = " ".join(s.get("title", "") for s in sources)
    licenses = " ".join(s.get("license", "") for s in sources)
    assert "Stop Slop" in titles
    assert "MIT" in licenses


def test_prepublish_prompt_safety_contract():
    prompt = read_text(Path("prompts") / "prepublish-quality-check.md").lower()
    assert "not proof of ai authorship" in prompt
    assert "evade ai detection" in prompt
    assert "fabricat" in prompt          # no fabricating specifics
    assert "preserve meaning" in prompt   # keep author's meaning/facts
    assert "overuse" in prompt            # patterns are overuse-watch, not bans


def test_prose_quality_rubric_safety():
    text = read_text(Path("rubrics") / "prose-quality-rubric.md").lower()
    assert "not proof of ai authorship" in text
    assert "do not fabricate" in text
    assert "not laws" in text or "defaults, not" in text  # non-absolutist framing


def test_skill_json_attributes_stop_slop():
    skill = json.loads(read_text("skill.json"))
    extra = skill.get("additional_sources", [])
    assert any(s.get("title") == "Stop Slop" and s.get("license") == "MIT" for s in extra)
    assert "modes" in skill and "safe_review" in skill["modes"] and "prose_cleanup" in skill["modes"]


def test_before_after_examples_do_not_teach_fabrication():
    text = read_text(Path("examples") / "before-after-revisions.md").lower()
    invented_details_from_prior_draft = [
        "two weeks sooner",
        "fast release cycles",
        "three accounts",
        "support team flagged",
        "two engineers patched",
        "triage review every friday",
    ]
    for detail in invented_details_from_prior_draft:
        assert detail not in text
    assert "rather than inventing" in text
    assert "only if the writer can verify" in text
