# Script para extraer datos completos de Excel
param(
    [string]$FilePath
)

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    $workbook = $excel.Workbooks.Open($FilePath)
    
    Write-Host "=== ARCHIVO: $FilePath ==="
    Write-Host "Hojas disponibles:"
    foreach ($sheet in $workbook.Sheets) {
        Write-Host "  - $($sheet.Name)"
        
        # Obtener rango usado
        $usedRange = $sheet.UsedRange
        $rowCount = $usedRange.Rows.Count
        $colCount = $usedRange.Columns.Count
        Write-Host "    Filas: $rowCount, Columnas: $colCount"
    }
    
    $workbook.Close($false)
    $excel.Quit()
    
    # Liberar COM objects
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
} catch {
    Write-Host "Error: $_"
    if ($excel) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}
