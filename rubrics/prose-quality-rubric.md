# Prose Quality Rubric (Cleanup Mode)

A lightweight 50-point score for **prose quality**, used in Prose Cleanup Mode. It rates how clear, specific, and natural writing is — it does **not** estimate whether AI was involved.

> A low score does not mean text is AI-written. A high score does not mean it is human-written. This rubric measures writing quality only, and is not proof of AI authorship.

This is not proof of AI authorship.

## How to score

Rate each dimension 1–10 (10 = excellent). Sum for a total out of 50.

| Dimension | Ask | 1–3 (weak) | 8–10 (strong) |
|-----------|-----|------------|---------------|
| **Directness** | Does it state the point, or announce that a point is coming? | Throat-clearing, meta-commentary, hedged setups | Leads with the actual claim |
| **Specificity & grounding** | Are claims concrete and supported? | Vague declaratives, generic hype, unnamed sources | Named facts, figures, and sources |
| **Rhythm & variation** | Do sentence lengths and shapes vary? | Metronomic, formulaic, every paragraph ends on a punchline | Natural variation that serves meaning |
| **Reader trust** | Does it respect the reader, or over-explain? | Over-softening, repeated reassurance, condescending prompts | States facts and lets the reader judge |
| **Density** | Is anything cuttable without loss? | Filler, redundant qualifiers, empty intensifiers | Every sentence earns its place |

## Interpreting the total

- **40–50** — Publish-ready prose. Light touch-ups at most.
- **35–39** — Solid; tighten the weakest one or two dimensions.
- **Below 35** — Revise before publishing. Start with the lowest-scoring dimension.

## Guardrails (these override any cleanup urge)

- **Preserve meaning and facts.** Tightening prose must not drop or distort what the author actually said.
- **Do not fabricate.** Never invent sources, quotes, anecdotes, numbers, or specifics to raise the "specificity" score. If a claim lacks support, flag it; do not manufacture support.
- **Treat the rules as defaults, not laws.** Em dashes, adverbs, rule-of-three, and passive voice are *patterns to watch for overuse*, not banned constructions. Many strong human writers use all of them well. Cut them only when they genuinely weaken a specific sentence.
- **Match the venue.** Academic, legal, and technical writing have their own norms; do not flatten them into a single "punchy" voice.
- **Quality, not evasion.** The goal is clearer, more accountable writing — never a lower AI-detector score. Do not frame edits as ways to defeat detection.

## Relationship to Safe Review Mode

This rubric is for *improving* prose you are allowed to edit. To *assess* someone else's text for signals that warrant human review (without rewriting it), use `prompts/ai-writing-review.md` and `rubrics/signal-taxonomy.json` instead. Either way: this is not proof of AI authorship.

## Attribution

The five-dimension scoring shape is adapted, with safer framing, from the "Stop Slop" skill by Hardik Pandya (MIT License, https://github.com/hardikpandya/stop-slop). Reworded and extended; absolutist rules were converted into overuse-watch guidance with false-positive caveats.
