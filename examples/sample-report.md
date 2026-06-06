# Sample Report

This report reviews `examples/sample-input-aiish.md`.

## Overall Assessment

- review_focus: high
- confidence: medium
- short_summary: The text contains generic significance claims, formulaic phrasing, over-formatting, a direct chatbot disclaimer, and placeholder citation text. These are strong editorial review concerns, but they do not prove authorship.
- caveat: This is not proof of AI authorship.

## Possible AI-Like Signals

### Generic importance or legacy claim

- category: Content-level signals
- severity: medium
- evidence_quote: "marks a pivotal moment"
- why_it_matters: The phrase inflates importance without specific evidence from records, sources, or concrete outcomes.
- safer_revision_advice: Replace with the actual approval date, cost, vote, accessibility changes, or sourced community impact.
- false_positive_warning: Human writers also use stock civic or promotional language.

### Formulaic parallelism

- category: Language and grammar signals
- severity: low
- evidence_quote: "Not only does the project"
- why_it_matters: This construction can create a polished but generic rhythm.
- safer_revision_advice: State the concrete change directly.
- false_positive_warning: This is a common human rhetorical pattern and is weak on its own.

### Inline-header bullet formatting

- category: Style and formatting signals
- severity: low
- evidence_quote: "**Key Benefits:**"
- why_it_matters: The formatting looks template-like and may not fit the target venue.
- safer_revision_advice: Use normal prose or venue-appropriate headings.
- false_positive_warning: Human writers often use bold labels in drafts and presentations.

### Chatbot disclaimer

- category: User-facing / chatbot-like communication signals
- severity: high
- evidence_quote: "As an AI language model"
- why_it_matters: This is direct assistant-style residue and should not appear in final editorial prose.
- safer_revision_advice: Remove the sentence and verify council records directly.
- false_positive_warning: The phrase might be quoted intentionally, but no quotation context appears here.

### Placeholder citation

- category: Markup and citation artifacts
- severity: high
- evidence_quote: "[insert citation here]"
- why_it_matters: The text contains unfinished source markup.
- safer_revision_advice: Replace with a real citation or mark the claim as unsourced for human follow-up.
- false_positive_warning: Placeholder text can occur in any unfinished human draft.

## Quality Problems

- Tone is promotional rather than factual ("serves as a testament", "lasting legacy").
- Over-formatted: an inline-header bullet label ("**Key Benefits:**") replaces plain prose.
- Rule-of-three filler ("improved access, stronger engagement, and meaningful opportunities") adds cadence but no information.

## Source-Grounding Problems

- claim: the renovation's importance to "community learning and accessibility"
  - issue: Asserted with no source or concrete evidence.
  - advice: Replace with sourced specifics (cost, vote, accessibility changes) or remove.
- claim: council records referenced via "[insert citation here]"
  - issue: Placeholder where a real citation should be; the underlying claim is unverifiable as written.
  - advice: Add the actual council record and date, or flag the claim as unsourced for human follow-up.

## Signs of Human Writing

- None clearly present in this sample. The prose is generic and could be pasted onto almost any civic project, which is itself part of the concern.

## Rewrite Guidance

(Provide only if the user asks for a rewrite.)

- Lead with verifiable facts: vote date, bid details, cost, accessibility changes, and approval status.
- Remove broad significance claims unless a reliable source explicitly supports them.
- Repair or remove placeholder citation text; never replace it with a fabricated source.
