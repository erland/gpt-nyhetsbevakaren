#!/usr/bin/env python3
from pathlib import Path
import json
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]

def load_yaml(path): return yaml.safe_load(path.read_text(encoding="utf-8"))
def load_json(path): return json.loads(path.read_text(encoding="utf-8"))

def validate(instance,schema_path,label,errors):
    try:
        Draft202012Validator(load_json(ROOT/schema_path)).validate(instance)
    except Exception as exc:
        errors.append(f"{label}: {exc}")

def main():
    errors=[]
    cfg=load_yaml(ROOT/"gpt-project.yaml")

    for key,schema in [
        ("capabilities","schemas/capability-contract.schema.json"),
        ("artifacts","schemas/artifact-contract.schema.json"),
        ("state","schemas/state-contract.schema.json"),
        ("tools","schemas/tool-contract.schema.json"),
    ]:
        if key not in cfg:
            errors.append(f"gpt-project.yaml saknar {key}")
        else:
            validate(cfg[key],schema,key,errors)

    canonical=ROOT/cfg["instructions"]["canonical"]
    if not canonical.is_file():
        errors.append("Canonical instruktion saknas")
    else:
        text=canonical.read_text(encoding="utf-8")
        for marker in cfg["instructions"]["core_contract"]["required_markers"]:
            if marker not in text:
                errors.append(f"Canonical instruktion saknar marker: {marker}")

    caps=cfg["capabilities"]["requirements"]
    if caps["web_research"]["level"]!="required":
        errors.append("web_research måste vara required")
    if caps["source_navigation"]["level"]!="required":
        errors.append("source_navigation måste vara required")
    if caps["scheduling_action"]["level"]!="optional":
        errors.append("Direkt schemaläggning ska vara optional")
    if caps["persistent_state"]["level"]!="not_required":
        errors.append("Persistent state ska vara not_required")

    state=cfg["state"]
    if state["persistent_workspace_required"] is not False:
        errors.append("Persistent workspace får inte krävas")
    if state["conversation_state"]["authoritative"] is not False:
        errors.append("Chatthistorik får inte vara auktoritativ state")
    if state["portable_state"]["scheduling_prompt"]["self_contained"] is not True:
        errors.append("Schemaläggningsprompten måste vara självförsörjande")

    outputs=cfg["artifacts"]["outputs"]
    for required in ("news_profile","news_report","scheduling_prompt"):
        if required not in outputs:
            errors.append(f"Obligatorisk artefakt saknas: {required}")

    tools=cfg["tools"]["tools"]
    web=[t for t in tools if t["id"]=="web-research"]
    if len(web)!=1 or web[0]["requirement"]!="required":
        errors.append("web-research tool-contract saknas eller är inte required")

    for tool in tools:
        script=tool.get("script")
        if script and not (ROOT/script).is_file():
            errors.append(f"Deklarerat script saknas: {script}")

    if errors:
        print("FAILED: GPT Builder 1.5 platform contracts")
        for e in errors: print("-",e)
        return 1

    print("OK: GPT Builder 1.5 platform contracts")
    print("Validated: required web research/source navigation, portable artifacts, non-persistent state and development tools")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
