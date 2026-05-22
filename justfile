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

[doc('Build JSON schemas')]
[script]
build:
  python3 ./scripts/openapi2jsonschema.py "${SRC_DIR}" "${OUT_DIR}"

[doc('Strip helm + flatten _sources into out/_clean')]
[script]
prepare:
  python3 ./scripts/flatten-crds.py "${SRC_DIR}" "${OUT_DIR}/_clean"

[doc('Render JSON schemas + HTML site into out/site')]
render: prepare
  crd-schema-publisher convert -d "${OUT_DIR}/_clean" -o "${OUT_DIR}/site" --render
  rm -rf "${OUT_DIR}/site/_meta"

[doc('Full pipeline')]
_all: sync prepare render

[doc('Lint all files')]
[script]
lint:
  prek run --all-files
