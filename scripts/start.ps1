Param()
$root = Split-Path -Parent $PSScriptRoot
$cfgPath = Join-Path $root "config/model.yaml"
$cfg = Get-Content $cfgPath | ConvertFrom-Yaml
$current = $cfg.current
Write-Host "Starting OLALLMAgent1 with model $current"
if($current -eq '20B'){
  & "$PSScriptRoot/launch_20b.ps1"
}else{
  & "$PSScriptRoot/launch_120b.ps1"
}
python -m backend.server
