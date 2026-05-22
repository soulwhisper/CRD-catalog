set lazy
set quiet
set script-interpreter := ['bash', '-euo', 'pipefail']
set shell := ['bash', '-euo', 'pipefail', '-c']

export SRC_DIR := justfile_directory() / "schemas/_sources"
export OUT_DIR := justfile_directory() / "out"

[private]
default:
  @just --list

[doc('Sync upstream CRDs')]
sync:
  cd ./schemas && vendir sync

[doc('Strip helm + flatten _sources into out/_clean')]
[script]
prepare:
  python3 ./scripts/flatten-crds.py "${SRC_DIR}" "${OUT_DIR}/_clean"

[doc('Lint all files')]
[script]
lint:
  prek run --all-files
