#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]

def load_cfg():
    return yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))

def expected_runtime_assets(cfg, version):
    names=[]
    for runtime_id, rcfg in (cfg.get("runtime") or {}).items():
        if not isinstance(rcfg, dict) or rcfg.get("status")!="active":
            continue
        pattern=rcfg.get("artifact_name")
        if not pattern:
            raise SystemExit(f"Active runtime missing artifact_name: {runtime_id}")
        names.append(pattern.format(version=version))
    return sorted(names)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--version", required=True)
    p.add_argument("--dist", type=Path, default=ROOT/"dist")
    p.add_argument("--print-paths", action="store_true")
    a=p.parse_args()

    cfg=load_cfg()
    expected=expected_runtime_assets(cfg,a.version)
    metadata=["SHA256SUMS.txt","DELIVERY-MANIFEST.json"]
    required=expected+metadata
    missing=[name for name in required if not (a.dist/name).is_file()]
    actual_runtime=sorted(p.name for p in a.dist.glob("*.zip") if p.name in set(expected))

    if missing or actual_runtime!=expected:
        print("FAILED: declarative release assets", file=sys.stderr)
        if missing:
            print("missing:", *missing, sep="\n- ", file=sys.stderr)
        if actual_runtime!=expected:
            print("expected runtime assets:", *expected, sep="\n- ", file=sys.stderr)
            print("actual runtime assets:", *actual_runtime, sep="\n- ", file=sys.stderr)
        return 1

    if a.print_paths:
        for name in required:
            print(str(a.dist/name))
    else:
        print(f"OK: {len(expected)} active runtime assets + 2 metadata files verified")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
