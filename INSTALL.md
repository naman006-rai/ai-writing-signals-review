# Usage and Installation

This repository is a prompt/spec skill, not a Python, npm, or browser-extension package. There is no required runtime install. Python is only needed if you want to run the validator and tests (see the end of this file).

Whichever option you choose, the safety framing is unchanged: this is an editorial quality review, not an AI detector, and nothing it produces is proof of AI authorship.

## Option 1: Use it by copy-paste

Open the prompt you need:

- `prompts/ai-writing-review.md` for Safe Review Mode
- `prompts/prepublish-quality-check.md` for Prose Cleanup Mode
- `prompts/ai-writing-self-check.md` for self-checking an LLM draft
- `prompts/ai-writing-rewrite.md` for rewriting after review

Paste the prompt into ChatGPT, Claude, Gemini, DeepSeek, or a local LLM, then provide:

```text
text_to_review:
[paste your text]

context:
[optional venue, audience, or style expectations]

target_style:
[optional style target]

output_format:
markdown
```

Set `output_format: json` instead if you want machine-readable output. Use `prompts/ai-writing-rewrite.md` only after you have review findings or a clear editing goal.

## Option 2: Clone the repository

Cloning gives you every prompt, rubric, and example locally.

```bash
git clone <repo-url> ai-writing-signals-skill
cd ai-writing-signals-skill
```

Then open whichever prompt you need and follow Option 1. To confirm the package is intact:

```bash
python scripts/validate_skill.py
```

## Option 3: Install as a Claude Code / Agent Skill

`SKILL.md` already carries the Agent Skill frontmatter (`name` and `description`), so the folder is drop-in for tools that load skills from a skills directory.

```powershell
# Windows (PowerShell)
Copy-Item -Recurse .\ai-writing-signals-skill "$env:USERPROFILE\.claude\skills\ai-writing-signals-review"
```

```bash
# macOS / Linux
cp -r ai-writing-signals-skill ~/.claude/skills/ai-writing-signals-review
```

Reload your client and invoke the skill by name (`ai-writing-signals-review`).

## Optional: run the checks

These are for contributors verifying the package, not for end users.

```bash
python scripts/validate_skill.py   # structure, JSON, safety contract, attribution, tests
python -m pytest                   # falls back to a built-in harness if pytest is absent
```

## License

The documentation, prompts, rubrics, and examples are licensed under CC BY-SA 4.0. See `LICENSE` and `LICENSE-NOTES.md`, and keep the attribution in `README.md` and `SKILL.md` when you redistribute.
