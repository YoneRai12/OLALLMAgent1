Param()
$payload = @{messages=@(@{role="user";content="use browse"});tools=@(@{name="browse";description="Open URL";parameters=@{type="object";properties=@{url=@{type="string"}};required=@("url")}})} | ConvertTo-Json -Depth 5
$response = Invoke-WebRequest -Uri http://localhost:8000/chat -Method POST -Body $payload -ContentType 'application/json'
try {
    $json = $response.Content | ConvertFrom-Json
    if($json.tool_calls){ Write-Host "Tool call OK"; exit 0 } else { Write-Error "Missing tool_calls"; exit 1 }
} catch {
    Write-Error "Invalid JSON"; exit 1
}
