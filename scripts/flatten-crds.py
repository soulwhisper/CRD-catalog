#!/usr/bin/env python3
"""Strip helm directives from vendored CRDs and emit a flat dir of single-CRD YAMLs."""
from __future__ import annotations
import re, sys, yaml
from pathlib import Path

_LINE = re.compile(r"^[ \t]*\{\{-?.*?-?\}\}[ \t]*$", re.MULTILINE)
_INLINE = re.compile(r"\{\{-?.*?-?\}\}", re.DOTALL)

def strip_helm(text: str) -> str:
    return _INLINE.sub("_helm_", _LINE.sub("", text))

def main(src: Path, dst: Path) -> int:
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for path in sorted(src.rglob("*")):
        if not path.is_file() or path.suffix not in (".yaml", ".yml"):
            continue
        try:
            docs = list(yaml.safe_load_all(strip_helm(path.read_text("utf-8"))))
        except yaml.YAMLError as e:
            print(f"warn: skipping {path}: {e}", file=sys.stderr)
            continue
        for doc in docs:
            if not (isinstance(doc, dict) and doc.get("kind") == "CustomResourceDefinition"):
                continue
            api = doc.get("apiVersion", "")
            if api != "apiextensions.k8s.io/v1":
                print(f"warn: {path}: unsupported {api}", file=sys.stderr)
                continue
            name = doc.get("metadata", {}).get("name")
            if not name:
                print(f"warn: {path}: CRD missing metadata.name", file=sys.stderr)
                continue
            (dst / f"{name}.yaml").write_text(yaml.safe_dump(doc), "utf-8")
            written += 1
    print(f"flattened {n} CRDs to {dst}", file=sys.stderr)
    return 0 if n else 1

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
