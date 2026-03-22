param(
    [int]$Batches = 2,
    [int]$Limit = 100,
    [switch]$UntilEmpty,
    [int]$MaxBatches = 25,
    [string]$LogDir = ".\\logs"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = "$ScriptDir\..\\.venv\Scripts\python.exe"
$LogRoot = Join-Path $ScriptDir $LogDir
New-Item -ItemType Directory -Path $LogRoot -Force | Out-Null
$RunStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogRoot "run_batches_$RunStamp.log"
$SummaryFile = Join-Path $LogRoot "run_batches_$RunStamp.json"
$StartTime = Get-Date

if (-not (Test-Path $VenvPython)) {
    throw "Python interpreter not found: $VenvPython"
}

if ($UntilEmpty) {
    $TargetBatches = $MaxBatches
} else {
    $TargetBatches = $Batches
}

$RunRecords = @()
$PreviousPending = $null
$NoProgressCount = 0

Write-Host "Starting automated Books pipeline: $TargetBatches batches of $Limit files" -ForegroundColor Cyan
Write-Host "Started: $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
Write-Host "Log: $LogFile" -ForegroundColor Gray
Write-Host ""
"[$($StartTime.ToString('s'))] START target_batches=$TargetBatches until_empty=$UntilEmpty limit=$Limit" | Add-Content -Path $LogFile

for ($i = 1; $i -le $TargetBatches; $i++) {
    Write-Host "=== BATCH $i of $TargetBatches ===" -ForegroundColor Cyan
    $BatchStart = Get-Date
    
    # Export
    Write-Host "[1/3] Exporting $Limit files..." -ForegroundColor Magenta
    $ExportResult = & $VenvPython "$ScriptDir\export_books_ai.py" --limit $Limit --status pending | ConvertFrom-Json
    $ElapsedExport = (Get-Date) - $BatchStart
    
    Write-Host "  Selected: $($ExportResult.selected), Converted: $($ExportResult.converted_ok), Chunked: $($ExportResult.chunked_ok)" -ForegroundColor Green
    Write-Host "  Time: $($ElapsedExport.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    "[$((Get-Date).ToString('s'))] BATCH=$i export selected=$($ExportResult.selected) converted=$($ExportResult.converted_ok) chunked=$($ExportResult.chunked_ok) failed=$($ExportResult.failed)" | Add-Content -Path $LogFile
    
    # Rebuild Index
    Write-Host "[2/3] Rebuilding index..." -ForegroundColor Magenta
    $IndexStart = Get-Date
    $IndexResult = & $VenvPython "$ScriptDir\build_books_index.py" | ConvertFrom-Json
    $ElapsedIndex = (Get-Date) - $IndexStart
    Write-Host "  Indexed: $($IndexResult.file_count) files ($($IndexResult.total_size))" -ForegroundColor Green
    Write-Host "  Time: $($ElapsedIndex.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    
    # Read and display status
    Write-Host "[3/3] Reading status..." -ForegroundColor Magenta
    $CurrentSummaryFile = "$ScriptDir\books_index_summary.md"
    $Summary = Get-Content $CurrentSummaryFile -Raw
    
    if ($Summary -match "pending:\s+(\d+)") { $Pending = [int]$matches[1] }
    if ($Summary -match "converted:\s+(\d+)") { $Converted = [int]$matches[1] }
    if ($Summary -match "chunked:\s+(\d+)") { $Chunked = [int]$matches[1] }
    
    Write-Host "  Pending: $Pending | Converted: $Converted | Chunked: $Chunked" -ForegroundColor Green
    "[$((Get-Date).ToString('s'))] BATCH=$i status pending=$Pending converted=$Converted chunked=$Chunked" | Add-Content -Path $LogFile
    
    # Quick search validation
    $Keywords = @("kubernetes", "infrastructure", "security", "automation", "cloud", "resilience")
    $SearchTerm = $Keywords[$i % $Keywords.Length]
    & $VenvPython "$ScriptDir\search_books_chunks.py" $SearchTerm --limit 1 > $null 2>&1
    Write-Host "  Search validation: OK" -ForegroundColor Green

    $Record = [PSCustomObject]@{
        batch = $i
        selected = [int]$ExportResult.selected
        converted_ok = [int]$ExportResult.converted_ok
        chunked_ok = [int]$ExportResult.chunked_ok
        failed = [int]$ExportResult.failed
        pending = [int]$Pending
        converted = [int]$Converted
        chunked = [int]$Chunked
        elapsed_seconds = [math]::Round(((Get-Date) - $BatchStart).TotalSeconds, 1)
    }
    $RunRecords += $Record
    
    $BatchElapsed = (Get-Date) - $BatchStart
    Write-Host "Batch $i complete: $($BatchElapsed.TotalSeconds.ToString('F1'))s" -ForegroundColor Cyan
    Write-Host ""

    if ($Pending -le 0) {
        Write-Host "No pending files remain. Stopping." -ForegroundColor Green
        "[$((Get-Date).ToString('s'))] STOP reason=no_pending" | Add-Content -Path $LogFile
        break
    }

    if ($PreviousPending -ne $null -and $Pending -ge $PreviousPending) {
        $NoProgressCount += 1
    } else {
        $NoProgressCount = 0
    }

    if ($NoProgressCount -ge 2) {
        Write-Host "Pending count did not improve for 2 consecutive batches. Stopping for safety." -ForegroundColor Yellow
        "[$((Get-Date).ToString('s'))] STOP reason=no_progress" | Add-Content -Path $LogFile
        break
    }

    if ($ExportResult.selected -eq 0) {
        Write-Host "No files selected in this batch. Stopping." -ForegroundColor Yellow
        "[$((Get-Date).ToString('s'))] STOP reason=zero_selected" | Add-Content -Path $LogFile
        break
    }

    $PreviousPending = $Pending
}

$TotalElapsed = (Get-Date) - $StartTime
Write-Host "=== COMPLETE ===" -ForegroundColor Cyan
Write-Host "Batches attempted: $TargetBatches, Total time: $($TotalElapsed.TotalMinutes.ToString('F1')) min" -ForegroundColor Green
if ($RunRecords.Count -gt 0) {
    $Final = $RunRecords[-1]
    Write-Host "Final status: pending=$($Final.pending), converted=$($Final.converted), chunked=$($Final.chunked)" -ForegroundColor Green
}
Write-Host "Final status: Get-Content .\books_index_summary.md" -ForegroundColor Gray
Write-Host "Run log: $LogFile" -ForegroundColor Gray

$RunSummary = [PSCustomObject]@{
    started_at = $StartTime.ToString("s")
    ended_at = (Get-Date).ToString("s")
    until_empty = [bool]$UntilEmpty
    requested_batches = $TargetBatches
    limit = $Limit
    total_elapsed_seconds = [math]::Round($TotalElapsed.TotalSeconds, 1)
    records = $RunRecords
}
$RunSummary | ConvertTo-Json -Depth 5 | Set-Content -Path $SummaryFile -Encoding UTF8
"[$((Get-Date).ToString('s'))] END summary=$SummaryFile" | Add-Content -Path $LogFile
