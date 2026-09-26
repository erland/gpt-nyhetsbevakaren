#!/usr/bin/env python3
from pathlib import Path
import subprocess
import yaml

ROOT=Path(__file__).resolve().parents[1]

CANONICAL_MARKERS=[
    "Skilj publiceringsdatum från händelsedatum.",
    "Händelsebaserad deduplicering",
    "Håll isär verifierade fakta, osäkra uppgifter och analys.",
    "Rapportera hellre färre starka nyheter än utfyllnad.",
    "sök oberoende verifiering och markera osäkerhet",
    "skriv sakligt och neutralt",
    "självförsörjande schemaläggningsprompt",
    "anta inte minne mellan körningar",
]

REQUIRED_COVERAGE={
    "profile_creation",
    "source_strategy",
    "freshness",
    "importance",
    "event_deduplication",
    "report_format",
    "uncertainty",
    "scheduling",
}

REQUIRED_E2E={
    "e2e-daily-ai",
    "e2e-weekly-agentic-ai",
    "e2e-swedish-election",
    "e2e-many-sources-one-event",
    "e2e-thin-window",
    "e2e-scheduling-after-report",
    "e2e-scheduling-file-and-task",
}

def tracked_files():
    r=subprocess.run(["git","ls-files"],cwd=ROOT,text=True,capture_output=True,check=True)
    return [x.strip() for x in r.stdout.splitlines() if x.strip()]

def main():
    errors=[]
    cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    canonical=(ROOT/cfg["instructions"]["canonical"]).read_text(encoding="utf-8")
    manifest=yaml.safe_load((ROOT/cfg["testing"]["manifest"]).read_text(encoding="utf-8"))

    for marker in CANONICAL_MARKERS:
        if marker not in canonical:
            errors.append(f"Canonical instruktion saknar robustness-marker: {marker}")

    coverage=set(manifest.get("coverage") or [])
    missing_cov=sorted(REQUIRED_COVERAGE-coverage)
    if missing_cov:
        errors.append(f"Eval-manifest saknar coverage: {missing_cov}")

    required_ids=set(manifest.get("required_e2e_ids") or [])
    missing_ids=sorted(REQUIRED_E2E-required_ids)
    if missing_ids:
        errors.append(f"Eval-manifest saknar obligatoriska E2E-scenarier: {missing_ids}")

    caps=cfg["capabilities"]["requirements"]
    if caps["web_research"]["level"]!="required":
        errors.append("Aktuell nyhetsbevakning måste kräva webbresearch")
    if caps["source_navigation"]["level"]!="required":
        errors.append("Källöppning/source navigation måste vara required")
    if caps["scheduling_action"]["level"]!="optional":
        errors.append("Direkt schemaläggning ska vara optional")

    state=cfg["state"]
    if state["persistent_workspace_required"] is not False:
        errors.append("Persistent workspace får inte vara required")
    if state["conversation_state"]["authoritative"] is not False:
        errors.append("Chatthistorik får inte vara auktoritativ state")
    if state["portable_state"]["scheduling_prompt"]["self_contained"] is not True:
        errors.append("Schemaläggningsprompten måste vara självförsörjande")

    active=[rid for rid,rcfg in cfg["runtime"].items() if isinstance(rcfg,dict) and rcfg.get("status")=="active"]
    if set(active)!={"chat_zip","custom_gpt","claude_projects","opencode","openai_plugin"}:
        errors.append(f"Oväntad aktiv runtime-uppsättning: {sorted(active)}")

    files=tracked_files()
    for path in files:
        norm=path.replace("\\","/")
        if norm.startswith(("build/","dist/")) or "/__pycache__/" in norm or norm.startswith("__pycache__/"):
            errors.append(f"Genererad fil är spårad: {path}")
        if norm.endswith((".pyc",".pyo",".DS_Store")):
            errors.append(f"Oönskad fil är spårad: {path}")

    plugin=cfg["runtime"]["openai_plugin"]
    if plugin["compatibility"].get("external_integrations")!="none":
        errors.append("Plugin får inte deklarera externa integrationer")
    if plugin["compatibility"].get("scheduling_action")!="optional":
        errors.append("Plugin får inte kräva direkt schemaläggning")

    if errors:
        print("FAILED: news robustness/hygiene")
        for e in errors: print("-",e)
        return 1

    print("OK: freshness, source quality, event deduplication, uncertainty, political neutrality, scheduling portability and hygiene")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
