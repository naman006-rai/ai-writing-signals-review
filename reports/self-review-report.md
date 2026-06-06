# Self-Review Report

Date: 2026-06-06
Method: The skill reviewed its own human-facing content using its Safe Review Mode
(`prompts/ai-writing-review.md`, `rubrics/signal-taxonomy.json`,
`rubrics/scoring-rubric.md`) and Prose Cleanup Mode
(`prompts/prepublish-quality-check.md`, `rubrics/style-pattern-watchlist.json`,
`rubrics/prose-quality-rubric.md`).

This is an editorial quality audit, not a claim about who or what wrote the repo.
This is not proof of AI authorship. Every finding below carries a false-positive
note, because the skill's own rules require one.

## Overall Verdict

**Needs minor revision — shippable after a short, well-scoped set of fixes.**

The repository is in good shape on the dimension that matters most for this skill:
safety framing. The "not an AI detector" and "not proof of AI authorship" guarantees
are present and consistent, detector-evasion requests are refused in every prompt,
and the repo's own prose largely avoids the stock vocabulary its taxonomy flags
(`robust`, `seamless`, `delve`, `tapestry`, etc. appear only inside example fixtures
and as quoted "do not flag this" illustrations). That is the right result for a
dogfooding pass.

The remaining issues are editorial and licensing, not safety:

Biggest risks (in priority order):

1. **No own-license declaration despite a CC BY-SA 4.0 (ShareAlike) source.** The
   package attributes Wikipedia (CC BY-SA 4.0) and Stop Slop (MIT) but never states
   the license of the skill itself. ShareAlike normally requires the adapted text to
   stay under CC BY-SA 4.0. This is the one issue that could create a problem on
   public release. (Medium)
2. **The taxonomy's `false_positive_note` is a single boilerplate sentence repeated on
   all 35 signals — including 6 where it is semantically wrong.** For the
   `human_writing` counter-indicators and the `ineffective_indicators`, "treat it as
   one review clue" contradicts the entry's own `safer_revision_advice` ("Do not flag
   this"). A copy-pasted caveat applied without regard to fit is exactly the generic
   pattern this skill teaches reviewers to catch. (Medium)
3. **An unsourced empirical claim violates the skill's own grounding rule.** SKILL.md
   states "humans perform near chance at telling AI from human text" with no citation.
   The skill repeatedly tells writers to source or qualify claims like this. (Medium)

Highest-value fixes:

- Add a `License` section to README making the CC BY-SA 4.0 ShareAlike implication
  explicit, and add a top-level `LICENSE` file (maintainer decision — recommended, not
  auto-applied).
- Tailor the 6 mismatched `false_positive_note` entries so they fit counter-indicator
  and weak-indicator signals.
- Reframe the unsourced "near chance" claim as a normative caution that needs no
  citation.
- Sentence-case the Title-Case headings in `examples/sample-report.md` so the sample
  output models the style the skill recommends.

## File-by-file Findings

### README.md

- **risk_level:** low
- **confidence:** medium
- **detected_signals:** cross-file redundancy; minor stock phrasing; missing own-license
  section
- **evidence_quote:** "portable, model-agnostic prompt/spec"
- **why_it_matters:** "portable" / "model-agnostic" recur across README, SKILL.md, and
  skill.json. The README also re-explains the three-bucket model and safety rule already
  stated in SKILL.md. Some duplication is unavoidable for standalone files, but it is the
  repo's main prose-economy issue. The bigger gap is that the "Attribution And License"
  section describes the *sources'* licenses but never the *package's* own license.
- **recommended_fix:** Add a short `License` subsection stating the ShareAlike
  implication; otherwise leave the README's structure intact (its bullets are
  genre-appropriate for a README).
- **false_positive_note:** READMEs legitimately repeat key points for readers who never
  open SKILL.md, and feature bullets are a normal README convention, not over-formatting.

### SKILL.md

- **risk_level:** medium
- **confidence:** high
- **detected_signals:** unsupported empirical claim; inline-header bullets for the two
  modes
- **evidence_quote:** "humans perform near chance at telling AI from human text"
- **why_it_matters:** This is a specific empirical claim presented with no source, in the
  same document that tells writers to "Mark any claim that needs a source rather than
  asserting it" and to flag "non-trivial error rates"-style precision. By its own rubric,
  this sentence warrants a citation or a hedge. Separately, the two-mode list uses
  bold-label inline-header bullets (`- **Safe Review Mode (default).** ...`), a pattern
  the taxonomy lists under `style_inline_header_bullets`.
- **recommended_fix:** Reframe the claim as a normative caution ("do not treat a tool
  score or gut feeling as evidence; neither is reliable enough to support a claim about
  authorship") that asserts no statistic. Leave the two-mode bullets as-is — two items is
  not overuse.
- **false_positive_note:** The "near chance" finding is widely reported in the
  literature, so the claim is plausibly true; the issue is sourcing discipline, not
  accuracy. The mode bullets are a defensible two-item scannability choice.

### skill.json

- **risk_level:** low
- **confidence:** medium
- **detected_signals:** unverified compatibility claim
- **evidence_quote:** `"model_compatibility": ["Claude", "ChatGPT", "Gemini", "DeepSeek", "local LLMs"]`
- **why_it_matters:** Naming specific models implies tested compatibility. The artifact is
  a plain-text prompt, so the claim is reasonable, but it is asserted rather than shown.
- **recommended_fix:** Optional — note these are representative targets, not a tested
  matrix. Low priority; left unchanged this pass.
- **false_positive_note:** For a model-agnostic plain-text prompt, broad compatibility is
  a fair default expectation, not hype.

### prompts/ai-writing-review.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** none material
- **evidence_quote:** "A lone common word (one \"delve\", one em dash, one \"however\") is not a signal."
- **why_it_matters:** This is a model of the skill's own advice: it pre-empts
  single-phrase over-flagging and keeps the three buckets separate. Refusal language and
  the authorship caveat are both present.
- **recommended_fix:** None.
- **false_positive_note:** n/a — no signal raised.

### prompts/ai-writing-rewrite.md

- **risk_level:** low
- **confidence:** medium
- **detected_signals:** caveat-wording inconsistency
- **evidence_quote:** "It is not proof of authorship and is not intended to change any detector outcome."
- **why_it_matters:** This file uses a tailored caveat rather than the canonical "This is
  not proof of AI authorship." string used elsewhere. That is acceptable (the validator
  intentionally does not require the exact phrase here), but the refusal script wording
  drifts slightly across files ("I cannot help" vs "I can't help").
- **recommended_fix:** Leave the tailored caveat; optionally standardize the refusal
  sentence later. Not blocking.
- **false_positive_note:** Per-context phrasing is reasonable; rigid string-matching is a
  test concern, not a reader concern.

### prompts/ai-writing-self-check.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** inline-header bullets (10 checks)
- **evidence_quote:** "**Generic hype**: Did I overstate significance..."
- **why_it_matters:** The 10 checks use bold-label bullets — the `style_inline_header_bullets`
  pattern. In a checklist meant to be parsed by a model, bold action labels aid recall.
- **recommended_fix:** Keep. This is the textbook false positive the skill warns about
  (instructional genre). Do not flatten.
- **false_positive_note:** Checklists and prompts are a venue where labelled bullets help;
  the taxonomy explicitly rates this signal low with medium false-positive risk.

### prompts/prepublish-quality-check.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** inline-header bullets and boldface density (guardrails + checklist)
- **evidence_quote:** "**Lead with the point.** Cut throat-clearing openers..."
- **why_it_matters:** This is the flagship Cleanup-Mode prompt, and it is formatted in the
  exact bold-bullet style the Safe Review taxonomy flags. Honest dogfooding note: running
  the skill on this file would raise `style_inline_header_bullets` and
  `style_excessive_boldface`.
- **recommended_fix:** Keep the functional checklist. Note the tension in this report
  rather than degrade a usable prompt. (Per task rules: do not flatten, do not remove
  useful structure.)
- **false_positive_note:** Pre-publish checklists are a legitimate use of labelled bullets;
  the skill's own guidance says to weigh venue and not treat the pattern as a ban.

### rubrics/signal-taxonomy.json

- **risk_level:** medium
- **confidence:** high
- **detected_signals:** formulaic, copy-pasted caveat; semantic mismatch on 6 signals;
  unsourced empirical claim in one description
- **evidence_quote:** "Human writers can produce this pattern too; treat it as one review clue, not authorship evidence." (identical on all 35 signals)
- **why_it_matters:** A single sentence repeated verbatim 35 times is itself the
  "could be pasted onto almost any topic" pattern the skill flags. For the three
  `human_writing` counter-indicators and the three `ineffective_indicators`, the note is
  not just repetitive but wrong: those entries' `safer_revision_advice` says "Do not flag
  this," yet the note tells the reader to "treat it as one review clue." The
  `weak_detector_score` description also repeats the unsourced "near chance" claim.
- **recommended_fix:** Rewrite the 6 mismatched notes so they fit counter-indicators and
  weak indicators; reframe the `weak_detector_score` description to drop the unsourced
  statistic; bump the taxonomy version. Leave the 29 genuine-signal notes as an accepted
  normalized-field trade-off (per-signal nuance already lives in `review_question`,
  `false_positive_risk`, and `safer_revision_advice`).
- **false_positive_note:** A normalized JSON caveat is not prose; identical boilerplate on
  true signals is defensible. The mismatch on the 6 counter/weak signals is a genuine
  correctness bug, not a style preference.

### rubrics/scoring-rubric.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** none material
- **evidence_quote:** "Never score text as definitely AI-written, and never output a probability that AI was used."
- **why_it_matters:** Clear, conservative, and consistent with the rest of the skill. The
  authorship caveat is present.
- **recommended_fix:** None.
- **false_positive_note:** n/a.

### rubrics/prose-quality-rubric.md

- **risk_level:** low
- **confidence:** medium
- **detected_signals:** the authorship caveat appears three times in close proximity
- **evidence_quote:** "This is not proof of AI authorship." (blockquote, then a standalone line, then again in guardrails)
- **why_it_matters:** Lines 5–7 state the caveat twice within two lines (once as a
  blockquote, once as a bare sentence). Once is required; the immediate repeat is
  redundant.
- **recommended_fix:** Optional — keep the blockquote, drop the bare duplicate. Low
  priority; not changed this pass to avoid churn.
- **false_positive_note:** Redundant safety phrasing is a venial sin; over-correcting risks
  removing a required caveat, so caution is warranted.

### rubrics/style-pattern-watchlist.json

- **risk_level:** low
- **confidence:** high
- **detected_signals:** none material
- **evidence_quote:** "These are patterns to check for OVERUSE, not banned constructions."
- **why_it_matters:** Correctly reframes the Stop Slop ideas as non-absolutist, attributes
  both sources with licenses, and carries a per-pattern false-positive note.
- **recommended_fix:** None.
- **false_positive_note:** n/a.

### examples/sample-input-aiish.md and examples/sample-input-humanish.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** intentional fixtures (not the skill's own claims)
- **evidence_quote:** "As an AI language model, I do not have access to the latest council records"
- **why_it_matters:** The "AIish" sample deliberately contains a chatbot disclaimer and a
  placeholder citation as demonstration material. These must NOT be treated as the skill
  claiming anything, and the safety test must exempt them.
- **recommended_fix:** None. Leave fixtures unedited; "fixing" them would destroy their
  teaching value.
- **false_positive_note:** This is demonstration input, deliberately bad prose. Flagging it
  would be a category error.

### examples/sample-report.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** `style_title_case_overuse` in section headings
- **evidence_quote:** "### Generic Importance Or Legacy Claim"
- **why_it_matters:** The sample *output* uses Title Case headings (and even miscapitalizes
  "Or"), while the taxonomy flags title-case overuse and recommends sentence case. The
  canonical example should model the style the skill advises.
- **recommended_fix:** Sentence-case the five `###` finding headings.
- **false_positive_note:** Title case is acceptable in many venues; here it is worth fixing
  only because this file is the skill's own reference output.

### examples/before-after-revisions.md

- **risk_level:** low
- **confidence:** high
- **detected_signals:** none material
- **evidence_quote:** "Every \"after\" preserves the original meaning and invents no new facts."
- **why_it_matters:** Strong example file: it demonstrates tightening without fabrication,
  includes a deliberate "when NOT to fix" passive-voice case, and carries the
  no-fabrication caveat.
- **recommended_fix:** None.
- **false_positive_note:** n/a.

## Safety Findings

- **Detector-framing risks:** None found. Every file that mentions "detector" pairs it
  with a negation ("not an AI detector", "never be used as an AI detector"). README,
  SKILL.md, all four prompts, and both rubric prose files state the tool is not a detector.
- **Authorship-proof risks:** None found. "This is not proof of AI authorship." appears in
  all eight files the validator checks; `scoring-rubric.md` forbids outputting a probability
  of AI use; `sample-report.md` states findings "do not prove authorship." No file claims
  style proves authorship.
- **Evasion risks:** None found. Every occurrence of "evade", "evasion", or "bypass" is
  inside a refusal or negation ("Do not...", "Never...", "refuse that framing", "I can't
  help evade..."). No affirmative evasion offer exists anywhere in the repo. The validator
  already bans a list of known evasion slogans repo-wide (see `scripts/validate_skill.py`).
- **Fabrication risks:** None found. The rewrite and pre-publish prompts both forbid
  inventing sources, quotes, anecdotes, numbers, and dates, and tell the model to flag
  unsupported claims instead. The before/after examples explicitly refuse to invent
  specifics.
- **False-positive caveat gaps:** Two soft spots, both editorial rather than dangerous:
  (1) the 6 mismatched taxonomy `false_positive_note` entries described above; (2) the
  unsourced "near chance" empirical claim, which is a grounding-discipline gap, not a
  missing caveat. Both are addressed in the patch plan.

## Prose Cleanup Findings

- **Repeated phrases:** "portable" / "model-agnostic" across README, SKILL.md, skill.json;
  the three-bucket explanation restated in README, SKILL.md, the review prompt, and the
  scoring rubric; the authorship caveat stated twice within two lines in
  `prose-quality-rubric.md`; the identical 35-times `false_positive_note` in the taxonomy.
  Most cross-file repetition is justified by standalone-file portability; the in-file
  repeats (taxonomy boilerplate, double caveat) are the avoidable ones.
- **Generic claims:** "humans perform near chance..." (unsourced); skill.json
  `model_compatibility` list (asserted, not shown). Both low-to-medium severity.
- **Over-formatting:** Bold-label inline-header bullets in the two Cleanup-Mode/self-check
  prompts and the prose rubric guardrails. Defensible in instructional/checklist genre;
  noted, not "fixed", to avoid degrading usable prompts.
- **Weak examples:** `examples/sample-report.md` uses Title-Case headings — the only
  example that does not model the skill's own style advice.
- **Unclear instructions:** None material. The prompts are concrete and operational
  (explicit input/output schemas, numbered workflow, named files). If anything the skill
  errs toward repetition of its safety message, not vagueness.

## Attribution / License Findings

- **Wikipedia attribution:** Present and correct in SKILL.md, README.md, skill.json, and
  `signal-taxonomy.json` — title, URL, CC BY-SA 4.0, accessed date, and a "this is advice,
  not policy" note.
- **CC BY-SA 4.0 attribution:** Present for the source. **Gap:** the *package's own*
  license is never declared. CC BY-SA 4.0 is a ShareAlike license, so a substantive
  adaptation of its text normally must itself be offered under CC BY-SA 4.0. The repo
  should say so and ship a `LICENSE` file.
- **Stop Slop attribution:** Present in SKILL.md, README.md, skill.json
  (`additional_sources`), `style-pattern-watchlist.json`, and `prose-quality-rubric.md`,
  with author (Hardik Pandya), URL, and MIT license.
- **MIT reference:** Present wherever Stop Slop ideas are used.
- **Excessive copying:** None observed. The adaptation note ("reworded and reframed; no
  phrase lists copied verbatim") is consistent with the content; the taxonomy uses
  normalized signal objects rather than article prose.
- **Recommended action:** Add a `License` section to README clarifying (a) CC BY-SA 4.0
  for the adapted prose/rubrics under ShareAlike and (b) the relationship to the MIT-licensed
  Stop Slop ideas, and add a top-level `LICENSE` file. The license *choice* is a maintainer
  decision with legal weight, so this report recommends it and the README note states the
  implication; it does not silently impose a new license grant.

## Recommended Patch Plan

Applied in this pass (low-risk, preserves all safety framing):

1. `rubrics/signal-taxonomy.json` — rewrite the 6 mismatched `false_positive_note` entries
   (3 `human_writing`, 3 `ineffective_indicators`) to fit counter-indicators and weak
   indicators; reframe the `weak_detector_score` description to drop the unsourced
   statistic; bump version 1.1.0 → 1.1.1. (Keeps the validator/test invariants: each note
   still contains "human" and "authorship"/"proof".)
2. `SKILL.md` — reframe "humans perform near chance..." into a normative caution that
   asserts no statistic.
3. `examples/sample-report.md` — sentence-case the five finding headings; fix the
   miscapitalized "Or".
4. `README.md` — add a `License` section stating the CC BY-SA 4.0 ShareAlike implication
   and the MIT relationship; add `reports/` and the new test to the package-layout tree;
   add a one-line pointer to this dogfooding report.
5. `reports/self-review-report.md` — this report (new).
6. `tests/test_self_review_safety.py` — new dogfooding test (see task spec).
7. `scripts/validate_skill.py` — add the new test file and this report to the
   required-files contract so the dogfooding artifacts stay present.

Recommended but NOT auto-applied (maintainer decision):

- Add a top-level `LICENSE` file. Declaring a license is a legal choice; this audit
  recommends CC BY-SA 4.0 for the adapted prose to satisfy ShareAlike, but leaves the final
  grant to the maintainer.

Deliberately NOT changed (would violate the task's "do not flatten / do not remove useful
structure" rules):

- The labelled-bullet checklists in the Cleanup-Mode and self-check prompts.
- The intentional "bad prose" example fixtures.
- The 29 genuine-signal `false_positive_note` entries (acceptable normalized boilerplate).

Reminder: every finding here is an editorial indicator. None of it is proof of AI
authorship.
