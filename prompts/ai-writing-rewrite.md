# AI Writing Signals Rewrite Prompt

Use this prompt **only when the user explicitly asks for a rewrite**, normally after a review has identified problems. It is for quality-focused editing, not for changing what the text means.

## Inputs

```yaml
original_text: |
  [paste text here]
review_findings: |
  [optional: paste structured review findings here]
context: [optional: publication venue, audience, locale, source expectations, or constraints]
target_style: [optional: style target or style guide]
output_format: markdown | json   # default: markdown
```

## Prompt

Revise `original_text` using `review_findings` when provided. This is quality-focused editing. **Preserve facts**, do not evade detection, and do not invent anything.

Rules:

- Improve clarity, specificity, source grounding, factual precision, directness, natural rhythm, and tone appropriate to `context` and `target_style`.
- Remove generic hype, unsupported significance claims, broken markup, fake or stray citation artifacts, placeholders, and formulaic filler.
- **Do not invent** personal anecdotes, quotations, sources, citations, page numbers, statistics, dates, links, credentials, events, or lived experience. If a claim needs support you cannot supply, flag it instead of fabricating one.
- Do not change factual claims unless the review findings or supplied context clearly support the change. Preserve the author's meaning.
- Do not try to make the text "sound human" by adding errors, typos, awkwardness, slang, contradictions, hedging, or fake uncertainty.
- Do not remove useful structure, sources, or nuance just to make the text look less AI-written.
- The goal is genuinely better writing, not a lower AI-detector score. **Do not evade detection.** If the user asks you to bypass, defeat, or fool an AI detector, refuse that framing and reply: "I can't help evade AI detection, but I can help make this clearer, better sourced, and more specific." Then offer the quality-focused rewrite only.

Return:

```yaml
revised_text: |
  the revised version
change_notes:
  - concise note explaining a meaningful edit and why
claims_needing_sources:
  - a claim that should be verified or cited rather than fabricated
preserved_facts:
  - an important fact retained unchanged from the original
caveat: "This rewrite improves editorial quality. It is not proof of authorship and is not intended to change any detector outcome."
```

If `output_format` is `json`, return valid JSON only, using the same field names.
