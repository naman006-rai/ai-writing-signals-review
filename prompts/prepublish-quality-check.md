# Pre-Publish Quality Check Prompt (Prose Cleanup Mode)

A fast, portable checklist for tightening prose you are allowed to edit, just before publishing. Use it on your **own** draft or text you have permission to revise. It improves clarity, specificity, and rhythm — it is **not** an AI detector and says nothing about authorship.

## Inputs

```yaml
draft_text: |
  [paste the draft you want to tighten]
context: [optional: venue, audience, locale, style guide]
target_style: [optional: voice or tone to preserve]
output_format: markdown | json   # default: markdown
```

## Prompt

Tighten `draft_text` for a final pass before publishing. This is quality-focused editing of text the user is entitled to edit. Keep the author's meaning and facts intact.

Hard guardrails (these override every cleanup instinct):

- **Preserve meaning and facts.** Do not drop, distort, or reverse what the author said.
- **Do not fabricate.** Never invent sources, quotes, anecdotes, numbers, dates, or specifics to make the prose look more concrete. If a claim lacks support, flag it instead of inventing support.
- **Not for evasion.** The goal is clearer, more accountable writing, never a lower AI-detector score. If asked to defeat or bypass an AI detector, refuse that framing: "I can't help evade AI detection, but I can help make this clearer, better sourced, and more specific."
- **Patterns are defaults, not laws.** Em dashes, adverbs, rule-of-three, passive voice, and questions are constructions to check for *overuse*, not things to ban. Strong human writers use all of them. Change one only when it weakens a specific sentence, and respect the venue's norms.
- This is not proof of AI authorship.

Run the checklist. For each hit, prefer the smallest edit that fixes it. Consult `rubrics/style-pattern-watchlist.json` for patterns and safer alternatives.

Checklist:

- **Lead with the point.** Cut throat-clearing openers and meta-commentary ("here's the thing", "in this section we'll").
- **Name the specific thing.** Replace vague declaratives ("the implications are significant") with the concrete implication — sourced if it is a factual claim.
- **Find the actor.** Replace actor-hiding passive voice and false agency ("mistakes were made", "the decision emerges") with the person or group who acted.
- **Trim filler.** Reduce empty intensifiers and redundant qualifiers; keep words that change meaning.
- **Vary rhythm.** Break up runs of same-length sentences and check whether every paragraph ends on a punchline.
- **Drop manufactured drama.** Reduce formulaic binary contrasts, negative listing, and dramatic fragmentation where they add no information.
- **Check grounding.** Mark any claim that needs a source rather than asserting it.
- **Fit the venue.** Confirm tone, scope, and formatting suit the stated `context` and `target_style`.

Then score the result with `rubrics/prose-quality-rubric.md` (Directness, Specificity & grounding, Rhythm & variation, Reader trust, Density), 1–10 each. Remember: the score measures prose quality, not AI likelihood.

Return:

```yaml
prose_quality_score:
  directness: 1-10
  specificity_grounding: 1-10
  rhythm_variation: 1-10
  reader_trust: 1-10
  density: 1-10
  total: 0-50
  verdict: publish-ready | tighten | revise   # >=40 / 35-39 / <35
top_fixes:
  - the highest-impact edit to make
claims_needing_sources:
  - a claim to verify or cite rather than fabricate
revised_text: |
  the tightened version (only if the user asked for a rewrite; otherwise omit)
caveat: "This is a prose-quality check, not proof of AI authorship, and not a way to evade detection."
```

If `output_format` is `json`, return valid JSON only, using the same field names.
