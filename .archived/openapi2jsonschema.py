#!/usr/bin/env python3
"""
Convert vendored Kubernetes CRDs into per-version JSON Schema files for
use with yaml-language-server / kubeconform.

Usage:
    openapi2jsonschema.py <sources-dir> <out-dir>

For every *.yaml / *.yml under <sources-dir> we:
  1. strip helm template directives (``{{ ... }}``) — no standard CRD field
     legitimately contains them, so blanket-stripping is safe;
  2. parse all YAML documents and keep ``kind: CustomResourceDefinition`` ones;
  3. emit one JSON Schema per (group, kind, version) at:

         <out-dir>/<group>/<kind>_<version>.json   (lowercased)

This matches the layout served at
https://soulwhisper.github.io/k8s-schemas/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Iterator

import yaml

# Strip helm template syntax. Two cases need different handling so that the
# result still parses as YAML:
#
#   1. A line whose only content is a directive (``{{- if ... }}``,
#      ``{{- end }}``, etc.) — remove the whole line.
#   2. An inline directive used as part of a value
#      (``chart: {{ .Chart.Name }}-{{ .Chart.Version }}``) — replacing with
#      empty produces ``chart: -`` which YAML reads as a sequence entry, so
#      we substitute a benign placeholder string instead.
_LINE_ONLY_DIRECTIVE = re.compile(r"^[ \t]*\{\{-?.*?-?\}\}[ \t]*$", re.MULTILINE)
_INLINE_DIRECTIVE = re.compile(r"\{\{-?.*?-?\}\}", re.DOTALL)


def strip_helm(text: str) -> str:
    text = _LINE_ONLY_DIRECTIVE.sub("", text)
    return _INLINE_DIRECTIVE.sub("_helm_", text)


def iter_crds(root: Path) -> Iterator[tuple[Path, dict]]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in (".yaml", ".yml"):
            continue
        text = strip_helm(path.read_text(encoding="utf-8"))
        try:
            docs = list(yaml.safe_load_all(text))
        except yaml.YAMLError as exc:
            print(f"warn: skipping {path}: {exc}", file=sys.stderr)
            continue
        for doc in docs:
            if isinstance(doc, dict) and doc.get("kind") == "CustomResourceDefinition":
                yield path, doc


def write_schemas(crd: dict, out_dir: Path) -> int:
    spec = crd.get("spec") or {}
    group = spec.get("group")
    kind = (spec.get("names") or {}).get("kind")
    versions = spec.get("versions") or []
    if not (group and kind and versions):
        return 0

    written = 0
    for version in versions:
        name = version.get("name")
        schema = ((version.get("schema") or {}).get("openAPIV3Schema"))
        if not name or not schema:
            continue

        doc = dict(schema)
        doc["$schema"] = "http://json-schema.org/draft-07/schema#"
        doc["x-kubernetes-group-version-kind"] = [
            {"group": group, "kind": kind, "version": name},
        ]

        target_dir = out_dir / group.lower()
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{kind.lower()}_{name}.json"
        if target.exists():
            print(f"warn: overwriting {target}", file=sys.stderr)
        target.write_text(
            json.dumps(doc, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written += 1
    return written


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    sources = Path(argv[1])
    out = Path(argv[2])

    if not sources.is_dir():
        print(f"error: not a directory: {sources}", file=sys.stderr)
        return 1

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    total = 0
    for _, crd in iter_crds(sources):
        total += write_schemas(crd, out)

    if total == 0:
        print(f"error: no CRDs found under {sources}", file=sys.stderr)
        return 1

    print(f"wrote {total} schemas to {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
