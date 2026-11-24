#!/bin/sh
# Roda os testes do repositório e os de cada skill.
cd "$(dirname "$0")/.." || exit 1
falhou=0
for teste in tests/test_*.py tests/*/test_*.py; do
    [ -f "$teste" ] || continue
    echo "== $teste"
    python3 -B "$teste" || falhou=1
done
exit $falhou
