#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml


def load_cfg(root: Path) -> dict:
    return yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))


def files_under(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    cfg = load_cfg(root)

    errors: list[str] = []
    canonical_path = root / cfg["instructions"]["canonical"]
    canonical = canonical_path.read_text(encoding="utf-8")
    chat_path = root / "build/chat/assistant/instructions.md"
    custom_path = root / "build/custom-gpt/builder/instructions.md"
    claude_path = root / "build/claude-projects/assistant/instructions.md"
    opencode_path = root / "build/opencode/assistant/instructions.md"
    if not chat_path.exists():
        errors.append("Chat instruction missing")
    if not custom_path.exists():
        errors.append("Custom GPT instruction missing")
    if cfg["runtime"].get("claude_projects", {}).get("status") == "active" and not claude_path.exists():
        errors.append("Claude Projects instruction missing")
    if cfg["runtime"].get("opencode", {}).get("status") == "active" and not opencode_path.exists():
        errors.append("OpenCode instruction missing")

    markers = list(cfg.get("instructions", {}).get("core_contract", {}).get("required_markers", []) or [])
    for label, path in [("canonical", canonical_path), ("chat", chat_path), ("custom", custom_path), ("claude", claude_path), ("opencode", opencode_path)]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{label}: missing core marker: {marker}")

    if chat_path.exists() and chat_path.read_text(encoding="utf-8") != canonical:
        errors.append("Chat instruction is not byte-identical to canonical instruction")
    if claude_path.exists() and claude_path.read_text(encoding="utf-8") != canonical:
        errors.append("Claude Projects instruction is not byte-identical to canonical instruction")
    if opencode_path.exists() and opencode_path.read_text(encoding="utf-8") != canonical:
        errors.append("OpenCode instruction is not byte-identical to canonical instruction")

    canonical_k = root / cfg["knowledge_architecture"]["canonical_root"]
    chat_k = root / "build/chat/knowledge"
    custom_k = root / "build/custom-gpt/builder/knowledge-package"
    claude_k = root / "build/claude-projects/knowledge"
    opencode_k = root / "build/opencode/knowledge"
    canonical_files = files_under(canonical_k) - {"KNOWLEDGE.md"}
    chat_files = files_under(chat_k)
    custom_files = files_under(custom_k)
    claude_files = files_under(claude_k)
    opencode_files = files_under(opencode_k)
    if chat_files != canonical_files:
        errors.append(f"Chat Knowledge differs from canonical: expected={sorted(canonical_files)}, actual={sorted(chat_files)}")
    if len(canonical_files) <= int(cfg["runtime"]["custom_gpt"]["knowledge"]["max_files"]) and custom_files != canonical_files:
        errors.append(f"Custom GPT Knowledge should include all canonical files: expected={sorted(canonical_files)}, actual={sorted(custom_files)}")
    if cfg["runtime"].get("claude_projects", {}).get("status") == "active" and claude_files != canonical_files:
        errors.append(f"Claude Projects Knowledge differs from canonical: expected={sorted(canonical_files)}, actual={sorted(claude_files)}")
    if cfg["runtime"].get("opencode", {}).get("status") == "active" and opencode_files != canonical_files:
        errors.append(f"OpenCode Knowledge differs from canonical: expected={sorted(canonical_files)}, actual={sorted(opencode_files)}")

    plugin_cfg = cfg["runtime"].get("openai_plugin", {})
    if plugin_cfg.get("status") == "active":
        plugin_root = root / "build/openai-plugin" / plugin_cfg["manifest"]["name"]
        skill = plugin_root / "skills" / plugin_cfg["skill"]["id"] / "SKILL.md"
        if not skill.exists():
            errors.append("OpenAI Plugin skill missing")
        else:
            skill_text = skill.read_text(encoding="utf-8")
            if canonical.strip() not in skill_text:
                errors.append("OpenAI Plugin does not contain canonical instruction")
        plugin_k = plugin_root / "skills" / plugin_cfg["skill"]["id"] / "references" / "knowledge"
        plugin_files = files_under(plugin_k)
        if plugin_files != canonical_files:
            errors.append(f"OpenAI Plugin Knowledge differs from canonical: expected={sorted(canonical_files)}, actual={sorted(plugin_files)}")
    else:
        plugin_files = set()

    parity_doc = root / "docs/runtime-parity.md"
    if not parity_doc.exists():
        errors.append("Missing docs/runtime-parity.md")
    else:
        doc = parity_doc.read_text(encoding="utf-8")
        for phrase in ["Webbsökning", "Schemaläggning", "Händelsebaserad deduplicering", "Custom GPT", "Chat ZIP", "Claude Projects", "OpenCode", "OpenAI Plugin"]:
            if phrase not in doc:
                errors.append(f"Runtime parity report missing section marker: {phrase}")

    if errors:
        print("RUNTIME PARITY: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("RUNTIME PARITY: PASS")
    print(f"Core markers: {len(markers)}")
    print(f"Knowledge files: canonical={len(canonical_files)} chat={len(chat_files)} custom={len(custom_files)} claude={len(claude_files)} opencode={len(opencode_files)} plugin={len(plugin_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
