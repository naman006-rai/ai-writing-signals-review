# AI Writing Signals Self-Check Prompt

Use this before finalizing an LLM-generated or AI-assisted draft. It helps a model catch its own weak spots. It is a quality self-check, not an AI detector, and says nothing about authorship.

## Inputs

```yaml
draft_text: |
  [paste draft here]
context: [optional: publication venue, audience, locale, source expectations, or constraints]
target_style: [optional: style target or style guide]
output_format: markdown | json   # default: markdown
```

## Prompt

Self-check `draft_text` as an editorial quality review. Do not speculate about authorship. Identify concrete improvements before finalizing, and keep the author's meaning intact.

Run through these checks:

- **Generic hype**: Did I overstate significance, legacy, impact, or broader trends instead of giving specific evidence?
- **Vague sourcing**: Did I use unnamed groups ("experts say", "many believe") instead of named, verifiable sources?
- **Unsupported claims**: Does every factual claim have real support, or am I asserting things I cannot back up?
- **Fake citation risk**: Did I invent, guess, or malform any citation, DOI, ISBN, link, or page number? (If unsure a source is real, do not include it.)
- **Canned conclusions**: Did I end with formulaic "challenges and future prospects" filler instead of a concrete point?
- **Over-formatting**: Did I over-use title case, boldface, tables, or inline-header bullets where prose would be clearer?
- **Chatbot disclaimers**: Did I leave in assistant phrasing, knowledge-cutoff language, helpfulness offers, or self-identification?
- **Placeholder text**: Did I leave any template slots, brackets, TODOs, or lorem ipsum unfilled?
- **Markup leakage**: Did I leave stray Markdown, broken links, or citation artifacts that do not belong in the target format?
- **Context mismatch**: Does the tone, scope, locale, and time frame fit the stated `context` and `target_style`, and does it actually answer what was asked?

Return:

```yaml
ready_to_publish: yes | no | needs human review
highest_priority_fixes:
  - the most important fix
unsupported_claims:
  - a claim that lacks real support
claims_needing_sources:
  - a claim that should be cited rather than fabricated
formatting_or_artifact_fixes:
  - over-formatting, placeholder, disclaimer, or markup issue to remove
specificity_improvements:
  - a place to replace generic wording with concrete detail
final_caveat: "This is an editorial self-check. This is not proof of AI authorship."
```

If `output_format` is `json`, return valid JSON only, using the same field names.
