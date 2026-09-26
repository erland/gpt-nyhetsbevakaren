#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    status=yaml.safe_load((ROOT/"migration-status.yaml").read_text(encoding="utf-8"))

    if status.get("progress",{}).get("last_completed_step")!=9:
        errors.append("migration-status.yaml markerar inte steg 9 som klart")
    if status.get("state",{}).get("overall")!="pass":
        errors.append("migration-status.yaml har inte overall: pass")

    active=[rid for rid,rcfg in (cfg.get("runtime") or {}).items() if isinstance(rcfg,dict) and rcfg.get("status")=="active"]
    expected={"chat_zip","custom_gpt","claude_projects","opencode","openai_plugin"}
    if set(active)!=expected:
        errors.append(f"Oväntad aktiv runtime-uppsättning: {sorted(active)}")

    for doc in ["README.md","PROJECT.md","STATUS.md"]:
        text=(ROOT/doc).read_text(encoding="utf-8")
        for marker in ["Chat ZIP","Custom GPT","Claude Projects","OpenCode","OpenAI Plugin"]:
            if marker not in text:
                errors.append(f"{doc} saknar runtime-markör: {marker}")

    release=cfg.get("release",{}).get("github",{})
    if release.get("asset_selection")!="active_runtimes":
        errors.append("Release asset_selection måste vara active_runtimes")
    if set(release.get("include_metadata") or [])!={"SHA256SUMS.txt","DELIVERY-MANIFEST.json"}:
        errors.append("Release metadata-uppsättning är fel")

    caps=cfg["capabilities"]["requirements"]
    if caps["web_research"]["level"]!="required" or caps["source_navigation"]["level"]!="required":
        errors.append("Webbresearch/source navigation måste vara required")
    if caps["scheduling_action"]["level"]!="optional":
        errors.append("Direkt schemaläggning måste vara optional")

    state=cfg["state"]
    if state["persistent_workspace_required"] is not False:
        errors.append("Persistent workspace får inte krävas")
    if state["conversation_state"]["authoritative"] is not False:
        errors.append("Chatthistorik får inte vara auktoritativ state")
    if state["portable_state"]["scheduling_prompt"]["self_contained"] is not True:
        errors.append("Schemaläggningsprompten måste vara självförsörjande")

    if errors:
        print("FAILED: final release readiness")
        for e in errors:
            print("-",e)
        return 1

    print("OK: final release readiness")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
