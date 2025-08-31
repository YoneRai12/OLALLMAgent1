#!/usr/bin/env bash
set -e
CFG=$(python -c "import yaml,sys;print(yaml.safe_load(open('config/model.yaml'))['current'])")
echo "Starting OLALLMAgent1 with model $CFG"
if [ "$CFG" = "20B" ]; then
  pwsh scripts/launch_20b.ps1 >/dev/null 2>&1 || true
else
  pwsh scripts/launch_120b.ps1 >/dev/null 2>&1 || true
fi
python -m backend.server
