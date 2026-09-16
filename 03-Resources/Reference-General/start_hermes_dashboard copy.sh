#!/usr/bin/env bash
set -e
# Quick launcher for local Hermes dashboard (binds to localhost)
"${HOME}/.local/bin/hermes" dashboard --host 127.0.0.1 --port 9119 --no-open
