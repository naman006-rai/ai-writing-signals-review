# AI Writing Signals Review Skill

This package is a portable, model-agnostic prompt/spec for reviewing writing for quality issues and possible AI-like signals. It is not an AI detector and must not be used to accuse a writer of using AI.

The skill adapts the ideas from Wikipedia's advice page [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) into a compact editorial review workflow. The source page is descriptive, not policy, and its signs are potential indicators that need human review.

## Two Modes

- **Safe Review Mode (default)** — assess text you may not edit and produce a structured three-bucket report (quality / AI-like signals / source-grounding) with false-positive warnings. Files: `prompts/ai-writing-review.md`, `rubrics/signal-taxonomy.json`, `rubrics/scoring-rubric.md`.
- **Prose Cleanup Mode** — tighten your own draft before publishing (lead with the point, name specifics, find the actor, vary rhythm, cut filler). Files: `prompts/prepublish-quality-check.md`, `rubrics/style-pattern-watchlist.json`, `rubrics/prose-quality-rubric.md`, `examples/before-after-revisions.md`.

Both modes keep the same rule: nothing here is proof of AI authorship, and none of it is for evading AI detection. Cleanup Mode treats patterns (em dashes, adverbs, passive voice) as overuse signals to check, not bans.

## What It Does

- Reviews text for weak-to-strong signals associated with formulaic or AI-like writing.
- Separates findings into three buckets it never blurs: editorial quality problems, possible AI-like signals, and factual/source-grounding problems.
- Produces structured findings with evidence snippets, severity, false-positive warnings, and safer revision advice.
- Reports `review_focus` (how much human review the text warrants) instead of a probability of AI use.
- Helps revise text for specificity, source grounding, directness, factual precision, and appropriate tone.
- Refuses requests to bypass or evade AI detectors, and never claims text is definitely AI-written.

## Package Layout

```text
ai-writing-signals-skill/
  README.md
  SKILL.md
  skill.json
  prompts/
    ai-writing-review.md
    ai-writing-rewrite.md
    ai-writing-self-check.md
    prepublish-quality-check.md
  rubrics/
    signal-taxonomy.json
    scoring-rubric.md
    prose-quality-rubric.md
    style-pattern-watchlist.json
  examples/
    sample-input-humanish.md
    sample-input-aiish.md
    sample-report.md
    before-after-revisions.md
  tests/
    test_signal_taxonomy.py
    test_prompt_contract.py
    test_cleanup_mode.py
    test_self_review_safety.py
  scripts/
    validate_skill.py
  reports/
    self-review-report.md
```

## How To Use

For all installation and usage paths (copy-paste, clone, or install as an Agent Skill), see [`INSTALL.md`](INSTALL.md).

Open `prompts/ai-writing-review.md`, paste it into ChatGPT, Claude, Gemini, DeepSeek, or a local LLM, and provide:

```text
text_to_review:
[paste the text]

context:
[optional publication venue, audience, source expectations, or style guide]

target_style:
[optional style target]

output_format:
markdown
```

For JSON output, set `output_format: json`. Use `prompts/ai-writing-rewrite.md` only after you have review findings or a clear editing goal.

## Example JSON Output

```json
{
  "overall_assessment": {
    "review_focus": "medium",
    "confidence": "low",
    "short_summary": "The text has several generic claims and formulaic transitions, but the evidence is not enough to infer authorship.",
    "caveat": "This is not proof of AI authorship."
  },
  "ai_like_signals": [
    {
      "category": "content",
      "signal_name": "Undue emphasis on significance, legacy, or impact",
      "severity": "medium",
      "evidence_quote": "plays a vital role",
      "why_it_matters": "The phrase inflates importance without concrete evidence.",
      "safer_revision_advice": "Replace the claim with a specific, sourced fact or remove it.",
      "false_positive_warning": "Human writers also use stock promotional language."
    }
  ],
  "quality_problems": [
    {
      "issue": "Promotional tone instead of neutral description",
      "advice": "State what happened plainly and drop the praise language."
    }
  ],
  "source_grounding_problems": [
    {
      "claim": "the subject's broad importance",
      "issue": "No citation or concrete evidence supports it.",
      "advice": "Add a reliable source or narrow the claim."
    }
  ],
  "rewrite_guidance": [
    "Add specific evidence for broad claims.",
    "Remove generic hype unless it is sourced and necessary."
  ]
}
```

## Ethical Limits

Use this as an editorial quality review, not an accusation engine. The skill should never claim that text is definitely AI-written. It should warn about false positives, preserve facts, and improve clarity instead of teaching evasion.

If a user asks how to bypass AI detection, use the refusal language in `SKILL.md` and offer quality-focused editing instead.

## Attribution And License

This package is adapted from concepts on Wikipedia's "Signs of AI writing" page:

- Source: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- License: Creative Commons Attribution-ShareAlike 4.0
- Accessed: 2026-06-06

This package transforms the source into a compact rubric, workflow, prompts, examples, and tests. It does not copy large portions of the page verbatim.

Prose Cleanup Mode adapts ideas (with safer, non-absolutist framing) from the "Stop Slop" skill by Hardik Pandya:

- Source: https://github.com/hardikpandya/stop-slop
- License: MIT

No phrase lists were copied verbatim; absolutist rules were reframed as overuse-watch guidance with false-positive caveats.

## License

This package mixes material with two origins (see Attribution above):

- **Adapted prose and rubrics** derive from Wikipedia's CC BY-SA 4.0 page. CC BY-SA 4.0 is a ShareAlike license, so derivative text normally must stay under CC BY-SA 4.0. Treat the adapted content here as **CC BY-SA 4.0** and keep the attribution above when you redistribute it.
- **Prose Cleanup Mode ideas** were reworded from the MIT-licensed Stop Slop skill; MIT permits this reuse.

Before publishing, add a top-level `LICENSE` file that records this. The license choice carries legal weight and is the maintainer's to finalize; this note states the ShareAlike implication rather than overriding it.

## Dogfooding

This skill was run against its own content as an editorial quality audit. See [`reports/self-review-report.md`](reports/self-review-report.md). That review is not proof of AI authorship; it is a quality pass that follows the skill's own rules, including a false-positive note on every finding.
