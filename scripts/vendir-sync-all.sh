#!/usr/bin/env bash
set -euo pipefail

dirs=("$@")
[[ ${#dirs[@]} -eq 0 ]] && mapfile -t dirs < <(find sources -mindepth 2 -maxdepth 2 -type d)

for dir in "${dirs[@]}"; do
    [[ -f "$dir/vendir.yml" ]] || continue
    echo ">>> $dir" >&2
    (cd "$dir" && vendir sync)
    # Pre-strip helm directives so build.sh doesn't mutate vendored files.
    find "$dir/vendor" -name '*.yaml' -exec sd '\{\{[^}]*\}\}' '' {} \;
done
