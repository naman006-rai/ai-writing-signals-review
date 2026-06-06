---
name: ai-writing-signals-review
description: Portable model-agnostic editorial quality review for AI-like writing signals. Use when reviewing prose for formulaic phrasing, generic hype, broken citations or markup, chatbot-like artifacts, weak sourcing, or other writing signals that may warrant human review. Do not use as an AI detector or to accuse a writer of AI use.
---

# AI Writing Signals Review

## Purpose

Review writing for editorial quality problems and possible AI-like signals without claiming authorship. Treat every signal as an indicator for human review, not proof.

This skill is based on a transformed, compact adaptation of Wikipedia's advice page "Wikipedia:Signs of AI writing." That page is descriptive guidance, not Wikipedia policy.

## Two Modes

This skill runs in either of two modes. Both share the same safety rule: nothing here is proof of AI authorship, and none of it is for evading AI detection.

- **Safe Review Mode (default).** Assess text you may not edit. Produce a structured, three-bucket report (quality / AI-like signals / source-grounding) with evidence snippets, false-positive warnings, and safer revision advice. Do not rewrite unless asked. Use `prompts/ai-writing-review.md`, `rubrics/signal-taxonomy.json`, and `rubrics/scoring-rubric.md`.
- **Prose Cleanup Mode.** Tighten your own draft (or text you are allowed to edit) before publishing: lead with the point, name specifics, find the actor, vary rhythm, cut filler. Use `prompts/prepublish-quality-check.md`, `rubrics/style-pattern-watchlist.json`, `rubrics/prose-quality-rubric.md`, and `examples/before-after-revisions.md`.

Pick Review Mode when judging someone else's text; pick Cleanup Mode when improving text you own. The cleanup watchlist treats patterns (em dashes, adverbs, passive voice, rule-of-three) as overuse signals to check, never as banned constructions — many strong human writers use them well.

## When To Use

- Reviewing article drafts, comments, reports, essays, web copy, or documentation for formulaic or AI-like writing signals.
- Separating quality problems from authorship speculation.
- Producing a structured review report with evidence snippets and safer revision advice.
- Preparing a quality-focused rewrite that preserves facts and improves specificity, sourcing, tone, and clarity.
- Self-checking an LLM draft before delivery.

## When Not To Use

- Do not use this as an AI detector.
- Do not accuse a person of using AI based on these signals.
- Do not rank writers, students, employees, or contributors by suspected AI use.
- Do not provide advice on how to evade AI detection.
- Do not remove useful structure, sources, or nuance just to make text look less AI-like.

If asked for detector evasion, respond: "I cannot help evade AI detection. I can help improve the text's quality, specificity, source grounding, factual precision, and tone."

## Input Format

```yaml
text_to_review: |
  Paste the writing to review.
context: optional publication venue, audience, source expectations, or constraints
target_style: optional style target or style guide
output_format: markdown | json
```

## Output Format

Return a structured report that keeps three buckets separate: editorial quality problems, possible AI-like signals, and factual/source-grounding problems.

```yaml
overall_assessment:
  review_focus: low | medium | high   # how much human review the text warrants
  confidence: low | medium | high      # confidence in the signals, not in authorship
  short_summary: concise editorial summary
  caveat: "This is not proof of AI authorship."
ai_like_signals:
  - category: one signal category
    signal_name: specific signal
    severity: low | medium | high
    evidence_quote: short quoted snippet only
    why_it_matters: quality or review concern
    safer_revision_advice: concrete edit advice
    false_positive_warning: why this may occur in human writing
quality_problems:
  - issue: quality issue independent of AI-likeness
    advice: concrete fix
source_grounding_problems:
  - claim: claim or reference that cannot be verified
    issue: what is missing, broken, or fabricated-looking
    advice: how to verify, source, or qualify it
signs_of_human_writing:
  - evidence_quote: short snippet
    why_it_matters: why it suggests accountable, context-specific writing
rewrite_guidance:
  - focused revision instruction (only if a rewrite is requested)
```

## Review Workflow

1. Read the whole text once for purpose, audience, and factual claims.
2. Identify editorial quality problems: vagueness, hype, weak structure, or inappropriate tone.
3. Identify factual/source-grounding problems: unsupported claims, missing or broken citations, fabricated-looking references.
4. Identify possible AI-like signals using the taxonomy below, keeping them separate from the two buckets above.
5. Quote only short evidence snippets. Do not quote long passages.
6. Set `review_focus` from the overall pattern across categories, not from one phrase.
7. Assign confidence conservatively, and only about the signals — never about authorship. Use high confidence only when multiple strong, independent, objective artifacts appear.
8. Include a false-positive warning for every detected AI-like signal.
9. Provide safer revision advice that improves writing quality, not detector evasion.
10. End with the caveat: "This is not proof of AI authorship."

## Signal Taxonomy

Use these high-level categories:

- Content-level signals: generic importance, inflated legacy claims, canned notability, superficial analysis, promotional tone, vague attribution, formulaic future-prospects conclusions.
- Language and grammar signals: dense stock vocabulary, "not only X but also Y" patterns, rule-of-three phrasing, avoidance of direct verbs, overuse of elegant variation.
- Style and formatting signals: title case overuse, excessive boldface, inline-header bullet lists, overuse of em dashes, unusual tables, inconsistent heading levels.
- User-facing or chatbot-like communication signals: "Certainly" style openings, knowledge-cutoff disclaimers, "let me know" offers, template instructions, placeholder text.
- Markup and citation artifacts: Markdown in non-Markdown contexts, broken wikitext or HTML, fake citation markers, malformed references, invented or unrelated identifiers.
- Metadata and context signals: abrupt style shifts, excessive edit-summary explanations, context-mismatched commentary, source claims that do not match the venue.
- Signs of human writing: context-specific detail, accountable sourcing, explainable editorial choices, constrained claims, natural variation that serves meaning.
- Ineffective or weak indicators: polished writing, correct grammar, use of common transitions, or a single familiar phrase without other evidence.

For normalized signal objects, use `rubrics/signal-taxonomy.json`. For scoring rules, use `rubrics/scoring-rubric.md`.

## Scoring Guidance

Review focus (how much human review the text warrants — not a probability of AI use):

- Low: no strong signals, isolated weak signals, or issues explained by genre/style.
- Medium: several signals from more than one category, with limited direct evidence.
- High: multiple strong signals, especially chatbot artifacts, broken generated markup, fake citations, or abrupt context-mismatched text.

Confidence:

- Low: short sample, genre mismatch, or mostly weak indicators.
- Medium: enough text and repeated patterns, but plausible human explanations remain.
- High: multiple independent, objective artifacts such as fake citation syntax, chatbot disclaimers, and broken markup.

Severity:

- Low: minor style issue or common phrase.
- Medium: repeated generic, formulaic, or unsupported writing pattern.
- High: objective artifact, fabricated-looking citation marker, misleading source claim, or direct chatbot residue.

## Rewrite Guidance

Do improve:

- specificity
- source grounding
- directness
- natural variation
- factual precision
- appropriate tone
- removal of generic hype
- removal of broken markdown or citation artifacts
- reduction of formulaic structure

Do not:

- add errors to sound human
- invent anecdotes, uncertainty, sources, or personal experience
- remove useful structure solely to appear less AI-like
- obscure AI-like signals while leaving unsupported claims intact
- change facts without evidence

## Caveats and Ethical Limitations

- This is an editorial quality review, not authorship proof. It must never be used as an AI detector or to accuse, rank, grade, or penalize anyone.
- Human writers can produce every weak signal in this rubric, and skilled human writing can trigger many at once.
- Do not treat an AI-detection tool's score or a gut feeling as evidence; neither is reliable enough to support a claim about authorship.
- LLM-influenced language changes over time, so these signs are unstable and will date.
- Some signs are Wikipedia-specific and may not apply to other venues.
- A text can be AI-assisted and still be accurate, useful, and ethically disclosed; a text can be fully human-written and still be formulaic, vague, or broken.
- The goal is better, more accountable writing. Do not use this rubric for detector evasion while leaving the underlying quality and sourcing problems unfixed; that defeats the purpose.
- Never help anyone evade AI detection. Offer quality-focused editing instead.

## Example Output

```json
{
  "overall_assessment": {
    "review_focus": "medium",
    "confidence": "low",
    "short_summary": "The text relies on generic significance claims and formulaic structure. These are quality concerns and possible AI-like signals, but the evidence is not conclusive.",
    "caveat": "This is not proof of AI authorship."
  },
  "ai_like_signals": [
    {
      "category": "content",
      "signal_name": "Undue emphasis on significance, legacy, or impact",
      "severity": "medium",
      "evidence_quote": "plays a vital role",
      "why_it_matters": "The claim inflates importance without a specific source or concrete fact.",
      "safer_revision_advice": "Replace it with a sourced, specific contribution or remove the sentence.",
      "false_positive_warning": "Human writers also use familiar promotional phrases."
    }
  ],
  "quality_problems": [
    {
      "issue": "Promotional tone instead of neutral description",
      "advice": "State what happened plainly; remove praise-laden adjectives."
    }
  ],
  "source_grounding_problems": [
    {
      "claim": "the subject's broad importance to the field",
      "issue": "Asserted without any citation or concrete evidence.",
      "advice": "Add a reliable source or narrow the claim to what the text can support."
    }
  ],
  "rewrite_guidance": [
    "Prefer concrete facts over broad significance language.",
    "Keep structure where useful, but remove formulaic headings."
  ]
}
```

## License Attribution

Adapted from concepts on "Wikipedia:Signs of AI writing":

- URL: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- License: Creative Commons Attribution-ShareAlike 4.0
- Accessed: 2026-06-06

The source page is an advice and field-guide page, not policy. This skill transforms its ideas into a compact rubric, checklist, workflow, and prompt set.

Prose Cleanup Mode (the watchlist, prose-quality rubric, pre-publish checklist, and before/after examples) adapts ideas from the "Stop Slop" skill:

- Author: Hardik Pandya
- URL: https://github.com/hardikpandya/stop-slop
- License: MIT

Those ideas were reworded and reframed: absolutist rules ("ban all adverbs / em dashes") became overuse-watch guidance with false-positive caveats, and detector-evasion framing was replaced with "improve clarity and accountability." No phrase lists were copied verbatim.
