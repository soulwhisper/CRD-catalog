#!/usr/bin/env bash
set -euo pipefail
shopt -s globstar nullglob

SOURCE_DIR="${1:?usage: build.sh <source-dir> <output-file>}"
OUTPUT_FILE="${2:?usage: build.sh <source-dir> <output-file>}"
SOURCE_DIR="$(cd "${SOURCE_DIR%/}" && pwd)"
mkdir -p "$(dirname "$OUTPUT_FILE")"

if [[ -f "$SOURCE_DIR/kind.yaml" ]]; then
    WORK="$(mktemp -d)"
    trap 'rm -rf "$WORK"' EXIT
    cp -r "$SOURCE_DIR/vendor" "$WORK/vendor"
    ./scripts/kind-extract.sh "$SOURCE_DIR" "$WORK" "$OUTPUT_FILE"
else
    # Strip inline helm directives — no standard CRD field contains `{{...}}`.
    find "$SOURCE_DIR/vendor" -name '*.yaml' -exec sd '\{\{[^}]*\}\}' '' {} \;
    files=("$SOURCE_DIR"/vendor/**/*.yaml "$SOURCE_DIR"/vendor/**/*.yml)
    [[ ${#files[@]} -gt 0 ]] || { echo "no vendored YAML in $SOURCE_DIR — run 'vendir sync'" >&2; exit 1; }
    yq eval-all 'select(.kind == "CustomResourceDefinition")' "${files[@]}" > "$OUTPUT_FILE"
fi

[[ -s "$OUTPUT_FILE" ]] || { echo "no CRDs extracted from $SOURCE_DIR" >&2; exit 1; }
