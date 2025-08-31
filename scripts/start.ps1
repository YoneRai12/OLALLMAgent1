Param()
$cfg = Get-Content ../config/model.yaml | ConvertFrom-Yaml
$current = $cfg.current
Write-Host "Starting OLALLMAgent1 with model $current"
if($current -eq '20B'){
  ./launch_20b.ps1
}else{
  ./launch_120b.ps1
}
python -m backend.server
