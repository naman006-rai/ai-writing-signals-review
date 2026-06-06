import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def read_prompt(name):
    # Normalize hyphens to spaces so "false-positive" matches "false positive".
    return read_text(Path("prompts") / name).lower().replace("-", " ")


def test_review_prompt_contract():
    prompt = read_prompt("ai-writing-review.md")
    required = [
        "not proof of ai authorship",
        "false positive",
        "quality review",
        "do not accuse",
    ]
    for phrase in required:
        assert phrase in prompt, f"review prompt missing: {phrase!r}"


def test_review_prompt_prohibits_certainty():
    prompt = read_prompt("ai-writing-review.md")
    assert "certainty" in prompt
    assert "not an ai detector" in prompt


def test_review_prompt_separates_buckets():
    prompt = read_prompt("ai-writing-review.md")
    # quality, AI-like signals, and source grounding must be distinct buckets.
    assert "quality problems" in prompt
    assert "grounding" in prompt
    assert "signs of human writing" in prompt


def test_rewrite_prompt_contract():
    prompt = read_prompt("ai-writing-rewrite.md")
    required = [
        "do not invent",
        "preserve facts",
        "do not evade detection",
    ]
    for phrase in required:
        assert phrase in prompt, f"rewrite prompt missing: {phrase!r}"


def test_rewrite_prompt_refuses_evasion_and_fabrication():
    prompt = read_prompt("ai-writing-rewrite.md")
    assert "evade ai detection" in prompt
    assert "fabricat" in prompt  # prohibits fabricating sources
    # must forbid making text "sound human" with deliberate errors
    assert "adding errors" in prompt or "add errors" in prompt or "typos" in prompt


def test_self_check_prompt_contract():
    prompt = read_prompt("ai-writing-self-check.md")
    assert "not proof of ai authorship" in prompt
    for concept in [
        "hype",
        "vague sourcing",
        "over formatting",
        "fake citation",
        "canned conclusions",
        "chatbot",
        "placeholder",
        "unsupported claim",
        "context mismatch",
    ]:
        assert concept in prompt, f"self-check prompt missing: {concept!r}"


def test_skill_json_has_source_and_license():
    skill = json.loads(read_text("skill.json"))
    source = skill.get("source", {})
    assert "Signs of AI writing" in source.get("title", "")
    assert "en.wikipedia.org" in source.get("url", "")
    assert source.get("license", "").upper().replace(" ", "") == "CCBY-SA4.0".replace(" ", "")


def test_safe_review_mode_is_default_and_cleanup_is_secondary():
    skill = json.loads(read_text("skill.json"))
    assert skill.get("default_mode") == "safe_review"
    assert skill.get("mode_order") == ["safe_review", "prose_cleanup"]
    assert "Safe Review Mode (default)" in read_text("README.md")
    assert "Safe Review Mode (default)" in read_text("SKILL.md")


def test_skill_md_includes_ethical_limitations():
    text = read_text("SKILL.md").lower()
    assert "ethical limitation" in text
    assert "ai detector" in text
    assert "evade ai detection" in text


def test_required_safety_phrase_appears_in_key_files():
    key_files = [
        "README.md",
        "SKILL.md",
        "prompts/ai-writing-review.md",
        "prompts/ai-writing-self-check.md",
        "prompts/prepublish-quality-check.md",
        "rubrics/scoring-rubric.md",
        "rubrics/prose-quality-rubric.md",
        "examples/sample-report.md",
    ]
    for relative in key_files:
        assert "This is not proof of AI authorship." in read_text(relative), relative


def test_no_detector_evasion_slogans():
    unsafe_slogans = [
        "undetectable",
        "humanize to bypass",
        "bypass detector",
        "remove ai tells",
        "remove ai tell",
    ]
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json"}:
            text = path.read_text(encoding="utf-8").lower()
            for slogan in unsafe_slogans:
                assert slogan not in text, f"{path.relative_to(ROOT)} contains {slogan!r}"


def test_taxonomy_json_referenced_and_valid_license():
    taxonomy = json.loads(read_text("rubrics/signal-taxonomy.json"))
    assert taxonomy["source"]["license"].upper().startswith("CC BY-SA")
