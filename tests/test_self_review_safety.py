"""Dogfooding safety tests.

These tests run the skill's own safety contract against the repository's own
human-facing content. They exist because the skill is published as guidance for
others: if it cannot keep its own documentation inside its own rules, it is not
ready to recommend. The checks here are deliberately about *safety framing*
(detector framing, authorship-proof claims, evasion offers, fabrication), not
prose taste.

This is not proof of AI authorship; it is a quality-and-safety guardrail.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Human-facing markdown the public will actually read.
HUMAN_FACING_MD = [
    "README.md",
    "SKILL.md",
    "prompts/ai-writing-review.md",
    "prompts/ai-writing-rewrite.md",
    "prompts/ai-writing-self-check.md",
    "prompts/prepublish-quality-check.md",
    "rubrics/scoring-rubric.md",
    "rubrics/prose-quality-rubric.md",
    "examples/sample-report.md",
    "examples/before-after-revisions.md",
    "reports/self-review-report.md",
]

EXAMPLE_FILES = [
    "examples/sample-input-aiish.md",
    "examples/sample-input-humanish.md",
    "examples/sample-report.md",
    "examples/before-after-revisions.md",
]

# Action-oriented evasion phrasing. Allowed only when the same line refuses or
# negates it (the skill must refuse evasion, not offer it).
EVASION_PHRASES = [
    "evade ai detection",
    "evade detection",
    "bypass ai detection",
    "bypass detector",
    "defeat detection",
    "defeat the detector",
    "fool the detector",
    "fool an ai detector",
    "lower the detector score",
    "lower your detector score",
    "remove ai tells",
    "make it undetectable",
]

# Tokens that mark a line as a refusal/negation/safety context.
REFUSAL_TOKENS = [
    "not ",
    "never",
    "n't",
    "cannot",
    "refuse",
    "without",
    "instead",
    "rather than",
    "do not",
    "don't",
    "no help",
]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def in_refusal_context(line):
    low = line.lower()
    return any(token in low for token in REFUSAL_TOKENS)


def test_readme_does_not_frame_tool_as_an_ai_detector():
    text = read("README.md")
    low = text.lower()
    # Must explicitly disclaim detector framing.
    assert "not an ai detector" in low, "README must state it is not an AI detector"
    # Must not affirmatively present itself as a detector.
    for bad in ["this is an ai detector", "use this as an ai detector", "it is an ai detector"]:
        assert bad not in low, f"README frames the tool as a detector: {bad!r}"


def test_skill_md_keeps_safe_review_mode_as_default():
    text = read("SKILL.md")
    assert "Safe Review Mode (default)" in text, "SKILL.md must mark Safe Review Mode as default"
    # Default must come before the cleanup mode in the document.
    assert text.index("Safe Review Mode") < text.index("Prose Cleanup Mode"), (
        "Safe Review Mode must be presented before Prose Cleanup Mode"
    )


def test_key_prompts_include_authorship_caveat():
    # The review, self-check, and pre-publish prompts must carry the exact caveat.
    for relative in [
        "prompts/ai-writing-review.md",
        "prompts/ai-writing-self-check.md",
        "prompts/prepublish-quality-check.md",
    ]:
        assert "This is not proof of AI authorship." in read(relative), (
            f"{relative} missing the authorship caveat"
        )
    # The rewrite prompt uses a tailored caveat; it must still disclaim authorship.
    rewrite = read("prompts/ai-writing-rewrite.md").lower()
    assert "not proof of authorship" in rewrite, "rewrite prompt missing an authorship caveat"


def test_prompts_refuse_detector_evasion_requests():
    # Prompts that accept an external request must refuse evasion explicitly.
    for relative in [
        "prompts/ai-writing-review.md",
        "prompts/ai-writing-rewrite.md",
        "prompts/prepublish-quality-check.md",
    ]:
        low = read(relative).lower()
        assert "evade ai detection" in low, f"{relative} should name detector evasion to refuse it"
        assert ("i can't help evade" in low) or ("i cannot help evade" in low) or ("refuse" in low), (
            f"{relative} must contain refusal language for evasion requests"
        )


def test_examples_do_not_claim_proof_of_ai_authorship():
    for relative in EXAMPLE_FILES:
        low = read(relative).lower()
        # Any mention of "proof of ai authorship" must be the negated form.
        total = low.count("proof of ai authorship")
        negated = low.count("not proof of ai authorship")
        assert total == negated, (
            f"{relative} contains a non-negated 'proof of AI authorship' claim"
        )
        # No affirmative authorship verdicts.
        for bad in ["proves ai authorship", "proves it is ai", "is definitely ai", "definitely ai-written", "confirmed ai-written"]:
            assert bad not in low, f"{relative} makes an authorship-proof claim: {bad!r}"


def test_self_review_report_exists():
    assert (ROOT / "reports" / "self-review-report.md").exists(), (
        "reports/self-review-report.md must exist (dogfooding artifact)"
    )


def test_self_review_report_includes_false_positive_notes():
    low = read("reports/self-review-report.md").lower()
    # The report must follow the skill's own rule: every finding carries a note.
    assert "false_positive_note" in low or "false-positive note" in low, (
        "report must include false-positive notes"
    )
    assert "not proof of ai authorship" in low, "report must keep the authorship caveat"
    # Should carry notes on multiple findings, not a single token.
    assert low.count("false_positive_note") + low.count("false-positive") >= 3, (
        "report should carry false-positive notes across multiple findings"
    )


def test_no_human_facing_markdown_offers_evasion_outside_refusal_context():
    offenders = []
    for relative in HUMAN_FACING_MD:
        for lineno, line in enumerate(read(relative).splitlines(), start=1):
            low = line.lower()
            for phrase in EVASION_PHRASES:
                if phrase in low and not in_refusal_context(line):
                    offenders.append(f"{relative}:{lineno}: {phrase!r} -> {line.strip()!r}")
    assert not offenders, "evasion phrasing found outside a refusal/safety context:\n" + "\n".join(offenders)


def test_hard_evasion_slogans_absent_from_human_facing_markdown():
    # Slogans that have no legitimate non-refusal use at all.
    banned = ["undetectable", "humanize to bypass", "remove ai tells", "remove ai tell"]
    offenders = []
    for relative in HUMAN_FACING_MD:
        low = read(relative).lower()
        for slogan in banned:
            if slogan in low:
                offenders.append(f"{relative}: {slogan!r}")
    assert not offenders, "banned evasion slogan present: " + ", ".join(offenders)


# Prompts that accept an external request and can produce or offer rewritten text.
# The QA pass caught two fabrication regressions in this path: a rewrite that
# swapped an unsupported "experts" for an invented "commentators", and an
# evasion-refusal whose offered alternative invented "community learning
# programs". These contract tests guard the instruction that prevents both.
# (They assert the rule exists in the prompt, not live model output — the prompt
# is the only deterministic surface; a model harness is out of scope.)
REWRITE_PROMPT = "prompts/ai-writing-rewrite.md"
REFUSAL_OFFER_PROMPTS = [
    "prompts/ai-writing-review.md",
    "prompts/ai-writing-rewrite.md",
    "prompts/prepublish-quality-check.md",
]


def test_rewrite_prompt_forbids_substituting_unsupported_attributions():
    # Regression: rewrite turned "experts" into "commentators".
    low = read(REWRITE_PROMPT).lower()
    assert "do not substitute one unsupported attribution" in low, (
        "rewrite prompt must forbid swapping one unsupported attribution for another"
    )
    assert "commentators" in low, (
        "rewrite prompt should name the 'commentators' substitution as the worked example"
    )


def test_rewrite_prompt_forbids_inventing_actors_and_specifics():
    # Regression: invented actors and concrete specifics not present in the source.
    low = read(REWRITE_PROMPT).lower()
    assert "actors" in low, "rewrite no-invent rule must cover invented actors/attributions"
    for specific in ["program names", "place names", "activities"]:
        assert specific in low, (
            f"rewrite no-invent rule must cover invented concrete specifics ({specific!r})"
        )


def test_evasion_refusal_offers_forbid_invented_specifics():
    # Regression: the alternative offered after refusing evasion invented a
    # concrete detail ("community learning programs"). Every prompt that may
    # offer an alternative must require placeholders over invented specifics.
    for relative in REFUSAL_OFFER_PROMPTS:
        low = read(relative).lower()
        assert "bracketed placeholder" in low, (
            f"{relative} must require bracketed placeholders instead of invented specifics "
            "in any offered alternative"
        )
