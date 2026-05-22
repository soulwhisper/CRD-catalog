set lazy
set quiet
set positional-arguments
set script-interpreter := ['bash', '-euo', 'pipefail']
set shell := ['bash', '-euo', 'pipefail', '-c']

[private]
default:
  @just --list

[doc('Lint all files')]
[script]
lint:
  prek run --all-files
