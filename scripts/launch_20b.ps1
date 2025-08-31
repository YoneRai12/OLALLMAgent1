Param()
Write-Host "Launching 20B model via Ollama" -ForegroundColor Green
# Pull model if not exists
ollama pull gpt-oss-20b-q4_k_m 2>$null
Start-Process -FilePath ollama -ArgumentList "run gpt-oss-20b-q4_k_m" -NoNewWindow
Start-Sleep -Seconds 2
