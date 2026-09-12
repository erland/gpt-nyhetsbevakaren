#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml
import jsonschema

REQUIRED_COVERAGE = {
    "profile_creation", "source_strategy", "freshness", "importance",
    "event_deduplication", "report_format", "uncertainty", "scheduling"
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    findings = []

    manifest_path = root / "evals/test-manifest.yaml"
    if not manifest_path.exists():
        findings.append("Missing evals/test-manifest.yaml")
    else:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        coverage = set(manifest.get("coverage") or [])
        missing = sorted(REQUIRED_COVERAGE - coverage)
        if missing:
            findings.append(f"Missing coverage areas: {missing}")

        e2e_schema = json.loads((root / "schemas/e2e-news-scenario.schema.json").read_text(encoding="utf-8"))
        e2e_root = root / str(manifest.get("e2e", "evals/e2e"))
        ids = set()
        for path in sorted(e2e_root.glob("*.yaml")):
            case = yaml.safe_load(path.read_text(encoding="utf-8"))
            try:
                jsonschema.validate(case, e2e_schema)
            except Exception as exc:
                findings.append(f"Invalid E2E {path.name}: {exc}")
                continue
            if case["id"] in ids:
                findings.append(f"Duplicate E2E id: {case['id']}")
            ids.add(case["id"])
        required_ids = set(manifest.get("required_e2e_ids") or [])
        missing_ids = sorted(required_ids - ids)
        if missing_ids:
            findings.append(f"Missing required E2E scenarios: {missing_ids}")

        eval_schema = json.loads((root / "schemas/eval-case.schema.json").read_text(encoding="utf-8"))
        ia_root = root / str(manifest.get("instruction_adherence", "evals/instruction-adherence"))
        ia_ids = set()
        for path in sorted(ia_root.glob("*.yaml")):
            case = yaml.safe_load(path.read_text(encoding="utf-8"))
            try:
                jsonschema.validate(case, eval_schema)
            except Exception as exc:
                findings.append(f"Invalid instruction eval {path.name}: {exc}")
                continue
            cid = case.get("id") or case.get("name")
            if cid in ia_ids:
                findings.append(f"Duplicate instruction eval id: {cid}")
            ia_ids.add(cid)

    result = "pass" if not findings else "fail"
    report = {
        "result": result,
        "instruction_adherence_cases": len(list((root/'evals/instruction-adherence').glob('*.yaml'))),
        "e2e_scenarios": len(list((root/'evals/e2e').glob('*.yaml'))),
        "findings": findings,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Eval validation: {result.upper()}")
        print(f"Instruction-adherence cases: {report['instruction_adherence_cases']}")
        print(f"E2E scenarios: {report['e2e_scenarios']}")
        for f in findings:
            print(f"- {f}")
    return 0 if result == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
