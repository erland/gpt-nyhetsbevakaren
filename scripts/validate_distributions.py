#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except Exception as exc:
    raise SystemExit("PyYAML is required") from exc


FORBIDDEN_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "research",
    "evals",
    "tests",
}


def load_cfg(root: Path) -> dict:
    return yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))


def validate_custom(root: Path, cfg: dict) -> list[str]:
    errors = []
    build = root / "build" / "custom-gpt"
    if not build.exists():
        return ["Custom GPT build directory missing"]

    instr = build / "builder" / "instructions.md"
    if not instr.exists():
        errors.append("Missing builder/instructions.md")
    else:
        actual = len(instr.read_text(encoding="utf-8"))
        limit = int(cfg["runtime"]["custom_gpt"]["instruction"]["max_characters"])
        if actual > limit:
            errors.append(f"Instruction too long: {actual} > {limit}")

    kp = build / "builder" / "knowledge-package"
    files = [p for p in kp.rglob("*") if p.is_file()] if kp.exists() else []
    limit = int(cfg["runtime"]["custom_gpt"]["knowledge"]["max_files"])
    if len(files) > limit:
        errors.append(f"Too many Knowledge files: {len(files)} > {limit}")

    required = [
        build / "builder" / "instructions.md",
        build / "builder" / "conversation-starters.md",
        build / "builder" / "capabilities.md",
        build / "README.md",
        build / "COMPATIBILITY.md",
        build / "VERSION",
        build / "MANIFEST.json",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(build)}")
    return errors


def validate_chat(root: Path, cfg: dict) -> list[str]:
    errors = []
    build = root / "build" / "chat"
    if not build.exists():
        return ["Chat build directory missing"]

    required = [
        build / "START-HERE.md",
        build / "VERSION",
        build / "MANIFEST.json",
        build / "assistant" / "instructions.md",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(build)}")

    for p in build.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(build)
        if any(part in FORBIDDEN_PARTS for part in rel.parts):
            errors.append(f"Forbidden runtime path: {rel}")
    return errors


def validate_claude(root: Path, cfg: dict) -> list[str]:
    errors=[]
    build=root/"build"/"claude-projects"
    if not build.exists():
        return ["Claude Projects build directory missing"]

    required=[
        build/"START-HERE.md",
        build/"VERSION",
        build/"MANIFEST.json",
        build/"RUNTIME-REQUIREMENTS.md",
        build/"assistant"/"instructions.md",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required Claude file: {p.relative_to(build)}")

    rcfg=cfg["runtime"]["claude_projects"]
    canonical=(root/rcfg["source"]["instructions"]).read_bytes()
    instr=build/"assistant"/"instructions.md"
    if instr.exists() and instr.read_bytes()!=canonical:
        errors.append("Claude instruction is not byte-identical to canonical instruction")

    source_k=root/rcfg["source"]["knowledge"]
    build_k=build/"knowledge"
    expected={p.relative_to(source_k).as_posix() for p in source_k.rglob("*") if p.is_file() and p.name!="KNOWLEDGE.md"}
    actual={p.relative_to(build_k).as_posix() for p in build_k.rglob("*") if p.is_file()} if build_k.exists() else set()
    if actual!=expected:
        errors.append(f"Claude Knowledge differs from canonical: expected={sorted(expected)}, actual={sorted(actual)}")
    return errors


def validate_opencode(root: Path, cfg: dict) -> list[str]:
    errors=[]
    build=root/"build"/"opencode"
    if not build.exists():
        return ["OpenCode build directory missing"]

    required=[
        build/"START-HERE.md",
        build/"VERSION",
        build/"MANIFEST.json",
        build/"RUNTIME-REQUIREMENTS.md",
        build/"assistant"/"instructions.md",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required OpenCode file: {p.relative_to(build)}")

    rcfg=cfg["runtime"]["opencode"]
    canonical=(root/rcfg["source"]["instructions"]).read_bytes()
    instr=build/"assistant"/"instructions.md"
    if instr.exists() and instr.read_bytes()!=canonical:
        errors.append("OpenCode instruction is not byte-identical to canonical instruction")

    source_k=root/rcfg["source"]["knowledge"]
    build_k=build/"knowledge"
    expected={p.relative_to(source_k).as_posix() for p in source_k.rglob("*") if p.is_file() and p.name!="KNOWLEDGE.md"}
    actual={p.relative_to(build_k).as_posix() for p in build_k.rglob("*") if p.is_file()} if build_k.exists() else set()
    if actual!=expected:
        errors.append(f"OpenCode Knowledge differs from canonical: expected={sorted(expected)}, actual={sorted(actual)}")
    return errors


def validate_declared_artifacts(root: Path, cfg: dict) -> list[str]:
    errors=[]
    dist=root/"dist"
    expected=set()
    project_artifact=cfg.get("build_system",{}).get("current",{}).get("project_artifact",{})
    if project_artifact.get("enabled"):
        expected.add(project_artifact["artifact_name"].format(version="0.0.0-ci"))
    for runtime_id,rcfg in (cfg.get("runtime") or {}).items():
        if not isinstance(rcfg,dict) or rcfg.get("status")!="active":
            continue
        pattern=rcfg.get("artifact_name")
        if not pattern:
            errors.append(f"Active runtime missing artifact_name: {runtime_id}")
            continue
        expected.add(pattern.format(version="0.0.0-ci"))
    actual={p.name for p in dist.glob("*.zip")} if dist.exists() else set()
    if actual!=expected:
        errors.append(f"Declared artifact mismatch: actual={sorted(actual)} expected={sorted(expected)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cfg = load_cfg(root)

    errors = []
    errors.extend(validate_declared_artifacts(root, cfg))
    errors.extend(validate_chat(root, cfg))
    if cfg["runtime"]["custom_gpt"]["enabled"]:
        errors.extend(validate_custom(root, cfg))
    if cfg["runtime"].get("claude_projects", {}).get("status") == "active":
        errors.extend(validate_claude(root, cfg))
    if cfg["runtime"].get("opencode", {}).get("status") == "active":
        errors.extend(validate_opencode(root, cfg))

    if errors:
        print("VALIDATION: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
