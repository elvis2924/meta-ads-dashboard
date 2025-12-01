$excel = $null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

Write-Host "Done!"
