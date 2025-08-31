Param()
Write-Host "Launching 120B model via vLLM" -ForegroundColor Yellow
$cfg = Get-Content ../config/model.yaml | ConvertFrom-Yaml
$tp = $cfg.backends."120B".tensor_parallel_size
if($env:NVIDIA_VISIBLE_DEVICES -and $env:NVIDIA_VISIBLE_DEVICES -match ","){
  $tp = $tp
}else{
  $tp = 1
  Write-Warning "Only one GPU detected; using tensor_parallel_size=1"
}
Start-Process -FilePath python -ArgumentList "-m vllm.entrypoints.openai.api_server --model $($cfg.backends."120B".model) --tensor-parallel-size $tp" -NoNewWindow
Start-Sleep -Seconds 5
