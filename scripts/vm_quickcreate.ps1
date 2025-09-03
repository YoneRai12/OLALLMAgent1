Param([string]$Name="OLALLMAgentVM")
Write-Host "Creating Hyper-V VM $Name" -ForegroundColor Cyan
New-VM -Name $Name -MemoryStartupBytes 4GB -Generation 2
Set-VMProcessor -VMName $Name -Count 4
# Enable GPU-P
Add-VMGpuPartitionAdapter -VMName $Name
Set-VM -Name $Name -AutomaticStopAction ShutDown
Write-Host "VM created. Install Windows and enable remote Playwright." -ForegroundColor Green
