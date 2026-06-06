import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message):
    print(f"FAIL: {message}")
    return False


def pass_check(message):
    print(f"PASS: {message}")
    return True


def read_text(path):
    return path.read_text(encoding="utf-8")


def validate_required_files():
    required = [
        "README.md",
        "SKILL.md",
        "skill.json",
        "prompts/ai-writing-review.md",
        "prompts/ai-writing-rewrite.md",
        "prompts/ai-writing-self-check.md",
        "prompts/prepublish-quality-check.md",
        "rubrics/signal-taxonomy.json",
        "rubrics/scoring-rubric.md",
        "rubrics/prose-quality-rubric.md",
        "rubrics/style-pattern-watchlist.json",
        "examples/sample-input-humanish.md",
        "examples/sample-input-aiish.md",
        "examples/sample-report.md",
        "examples/before-after-revisions.md",
        "tests/test_signal_taxonomy.py",
        "tests/test_prompt_contract.py",
        "tests/test_cleanup_mode.py",
        "tests/test_self_review_safety.py",
        "scripts/validate_skill.py",
        "reports/self-review-report.md",
    ]
    missing = [item for item in required if not (ROOT / item).exists()]
    if missing:
        return fail(f"Missing required files: {missing}")
    return pass_check("required files exist")


def validate_json_files():
    for relative in [
        "skill.json",
        "rubrics/signal-taxonomy.json",
        "rubrics/style-pattern-watchlist.json",
    ]:
        try:
            json.loads(read_text(ROOT / relative))
        except json.JSONDecodeError as exc:
            return fail(f"{relative} is invalid JSON: {exc}")
    return pass_check("JSON files are valid")


def validate_taxonomy():
    taxonomy = json.loads(read_text(ROOT / "rubrics" / "signal-taxonomy.json"))
    required = {
        "id",
        "category",
        "name",
        "description",
        "common_patterns",
        "severity_default",
        "false_positive_risk",
        "false_positive_note",
        "review_question",
        "safer_revision_advice",
    }
    levels = {"low", "medium", "high"}
    categories = set(taxonomy.get("categories", []))
    if not categories:
        return fail("taxonomy categories are empty")
    counts = {category: 0 for category in categories}
    seen_ids = set()
    for signal in taxonomy.get("signals", []):
        missing = required - set(signal)
        if missing:
            return fail(f"signal {signal.get('id', '<missing id>')} missing {sorted(missing)}")
        for field in required:
            value = signal.get(field)
            if value is None or value == "":
                return fail(f"signal {signal.get('id')} has empty {field}")
        if not isinstance(signal["common_patterns"], list):
            return fail(f"signal {signal['id']} common_patterns must be a list")
        if signal["id"] in seen_ids:
            return fail(f"duplicate signal id: {signal['id']}")
        seen_ids.add(signal["id"])
        if signal["severity_default"] not in levels:
            return fail(f"signal {signal['id']} invalid severity_default {signal['severity_default']}")
        if signal["false_positive_risk"] not in levels:
            return fail(f"signal {signal['id']} invalid false_positive_risk {signal['false_positive_risk']}")
        note = str(signal["false_positive_note"]).lower()
        if "human" not in note and "false positive" not in note:
            return fail(f"signal {signal['id']} false_positive_note must mention human or false positive risk")
        category = signal["category"]
        if category not in categories:
            return fail(f"signal {signal['id']} has unknown category {category}")
        counts[category] += 1
    empty = [category for category, count in counts.items() if count == 0]
    if empty:
        return fail(f"taxonomy categories with no signals: {empty}")
    for needed in ("human_writing", "ineffective_indicators"):
        if counts.get(needed, 0) == 0:
            return fail(f"taxonomy missing signals in category: {needed}")
    return pass_check(f"taxonomy schema is complete ({len(seen_ids)} signals)")


def _norm(path):
    # Normalize hyphens to spaces so "false-positive" matches "false positive".
    return read_text(path).lower().replace("-", " ")


def validate_prompt_contract():
    review = _norm(ROOT / "prompts" / "ai-writing-review.md")
    rewrite = _norm(ROOT / "prompts" / "ai-writing-rewrite.md")
    self_check = _norm(ROOT / "prompts" / "ai-writing-self-check.md")
    review_required = [
        "not proof of ai authorship",
        "false positive",
        "quality review",
        "do not accuse",
        "not an ai detector",
        "certainty",
        "grounding",
    ]
    rewrite_required = [
        "do not invent",
        "preserve facts",
        "do not evade detection",
        "evade ai detection",
        "fabricat",
    ]
    self_check_required = [
        "not proof of ai authorship",
        "fake citation",
        "placeholder",
        "context mismatch",
    ]
    missing_review = [phrase for phrase in review_required if phrase not in review]
    missing_rewrite = [phrase for phrase in rewrite_required if phrase not in rewrite]
    missing_self = [phrase for phrase in self_check_required if phrase not in self_check]
    if missing_review:
        return fail(f"review prompt missing phrases: {missing_review}")
    if missing_rewrite:
        return fail(f"rewrite prompt missing phrases: {missing_rewrite}")
    if missing_self:
        return fail(f"self-check prompt missing phrases: {missing_self}")
    return pass_check("prompt contracts are present")


def validate_metadata_and_ethics():
    skill = json.loads(read_text(ROOT / "skill.json"))
    source = skill.get("source", {})
    if "Signs of AI writing" not in source.get("title", ""):
        return fail("skill.json source.title missing Wikipedia attribution")
    if "en.wikipedia.org" not in source.get("url", ""):
        return fail("skill.json source.url missing Wikipedia URL")
    if source.get("license", "").upper().replace(" ", "") != "CCBY-SA4.0":
        return fail(f"skill.json license is not CC BY-SA 4.0: {source.get('license')!r}")
    skill_md = read_text(ROOT / "SKILL.md").lower()
    for phrase in ["ethical limitation", "ai detector", "evade ai detection"]:
        if phrase not in skill_md:
            return fail(f"SKILL.md missing ethics phrase: {phrase!r}")
    if skill.get("default_mode") != "safe_review":
        return fail("skill.json default_mode must be safe_review")
    if skill.get("mode_order") != ["safe_review", "prose_cleanup"]:
        return fail("skill.json mode_order must keep Safe Review Mode first")
    return pass_check("metadata, license, and ethics statements present")


def validate_safety_language():
    required_phrase_files = [
        "README.md",
        "SKILL.md",
        "prompts/ai-writing-review.md",
        "prompts/ai-writing-self-check.md",
        "prompts/prepublish-quality-check.md",
        "rubrics/scoring-rubric.md",
        "rubrics/prose-quality-rubric.md",
        "examples/sample-report.md",
    ]
    for relative in required_phrase_files:
        if "This is not proof of AI authorship." not in read_text(ROOT / relative):
            return fail(f"{relative} missing required safety phrase")
    unsafe_slogans = [
        "undetectable",
        "humanize to bypass",
        "bypass detector",
        "remove ai tells",
        "remove ai tell",
    ]
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json"}:
            text = read_text(path).lower()
            for slogan in unsafe_slogans:
                if slogan in text:
                    return fail(f"{path.relative_to(ROOT)} contains unsafe slogan {slogan!r}")
    return pass_check("safety language scan passed")


def validate_cleanup_mode():
    watchlist = json.loads(read_text(ROOT / "rubrics" / "style-pattern-watchlist.json"))
    required = {
        "id",
        "category",
        "pattern_name",
        "examples",
        "why_generic",
        "safer_alternative",
        "false_positive_note",
        "severity_default",
    }
    levels = {"low", "medium", "high"}
    seen = set()
    patterns = watchlist.get("patterns", [])
    if not patterns:
        return fail("watchlist has no patterns")
    for pattern in patterns:
        missing = required - set(pattern)
        if missing:
            return fail(f"watchlist pattern {pattern.get('id', '<no id>')} missing {sorted(missing)}")
        if pattern["id"] in seen:
            return fail(f"duplicate watchlist id: {pattern['id']}")
        seen.add(pattern["id"])
        if not isinstance(pattern["examples"], list) or not pattern["examples"]:
            return fail(f"watchlist pattern {pattern['id']} needs a non-empty examples list")
        if pattern["severity_default"] not in levels:
            return fail(f"watchlist pattern {pattern['id']} invalid severity_default")
        if not str(pattern["false_positive_note"]).strip():
            return fail(f"watchlist pattern {pattern['id']} missing false_positive_note")
    blob = json.dumps(watchlist).lower()
    if "not proof of ai authorship" not in blob:
        return fail("watchlist missing 'not proof of ai authorship' safety note")
    if "evade" not in blob:
        return fail("watchlist missing detector-evasion disclaimer")
    source_titles = " ".join(s.get("title", "") for s in watchlist.get("sources", []))
    if "Stop Slop" not in source_titles:
        return fail("watchlist missing Stop Slop attribution")

    prepublish = _norm(ROOT / "prompts" / "prepublish-quality-check.md")
    for phrase in ["not proof of ai authorship", "evade ai detection", "fabricat", "preserve meaning", "overuse"]:
        if phrase not in prepublish:
            return fail(f"prepublish prompt missing phrase: {phrase!r}")

    rubric = read_text(ROOT / "rubrics" / "prose-quality-rubric.md").lower()
    for phrase in ["not proof of ai authorship", "do not fabricate"]:
        if phrase not in rubric:
            return fail(f"prose-quality rubric missing phrase: {phrase!r}")

    skill = json.loads(read_text(ROOT / "skill.json"))
    extra = skill.get("additional_sources", [])
    if not any(s.get("title") == "Stop Slop" and s.get("license") == "MIT" for s in extra):
        return fail("skill.json missing Stop Slop (MIT) attribution in additional_sources")
    modes = skill.get("modes", {})
    if "safe_review" not in modes or "prose_cleanup" not in modes:
        return fail("skill.json missing two-mode declaration")
    return pass_check(f"cleanup mode is complete ({len(seen)} watchlist patterns)")


def validate_line_counts():
    too_long = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json", ".py"}:
            line_count = len(read_text(path).splitlines())
            if line_count > 500:
                too_long.append(f"{path.relative_to(ROOT)} ({line_count})")
    if too_long:
        return fail(f"files exceed 500 lines: {too_long}")
    return pass_check("all package files are under 500 lines")


def run_direct_test_harness():
    sys.dont_write_bytecode = True
    failures = []
    count = 0
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in sorted(dir(module)):
            if name.startswith("test_") and callable(getattr(module, name)):
                count += 1
                try:
                    getattr(module, name)()
                except Exception as exc:
                    failures.append(f"{path.name}::{name}: {exc}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return fail("direct test harness failed")
    return pass_check(f"direct test harness passed ({count} tests)")


def run_pytest_if_available():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", str(ROOT / "tests")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        print(result.stdout.strip())
        return pass_check("pytest tests passed")
    if "No module named pytest" in result.stderr:
        print("INFO: pytest not installed; running direct test harness")
        return run_direct_test_harness()
    print(result.stdout)
    print(result.stderr)
    return fail("pytest tests failed")


def main():
    checks = [
        validate_required_files,
        validate_json_files,
        validate_taxonomy,
        validate_prompt_contract,
        validate_metadata_and_ethics,
        validate_safety_language,
        validate_cleanup_mode,
        validate_line_counts,
        run_pytest_if_available,
    ]
    results = [check() for check in checks]
    if all(results):
        print("SUMMARY: validation passed")
        return 0
    print("SUMMARY: validation failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
