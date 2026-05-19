#!/usr/bin/env bash
set -euo pipefail

git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
echo "Installed repository git hooks from .githooks/"
