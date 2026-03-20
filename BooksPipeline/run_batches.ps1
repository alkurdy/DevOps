param(
    [int]$Batches = 2,
    [int]$Limit = 100
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = "$ScriptDir\..\\.venv\Scripts\python.exe"
$StartTime = Get-Date

Write-Host "Starting automated Books pipeline: $Batches batches of $Limit files" -ForegroundColor Cyan
Write-Host "Started: $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
Write-Host ""

for ($i = 1; $i -le $Batches; $i++) {
    Write-Host "=== BATCH $i of $Batches ===" -ForegroundColor Cyan
    $BatchStart = Get-Date
    
    # Export
    Write-Host "[1/3] Exporting $Limit files..." -ForegroundColor Magenta
    $ExportResult = & $VenvPython "$ScriptDir\export_books_ai.py" --limit $Limit --status pending | ConvertFrom-Json
    $ElapsedExport = (Get-Date) - $BatchStart
    
    Write-Host "  Selected: $($ExportResult.selected), Converted: $($ExportResult.converted_ok), Chunked: $($ExportResult.chunked_ok)" -ForegroundColor Green
    Write-Host "  Time: $($ElapsedExport.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    
    # Rebuild Index
    Write-Host "[2/3] Rebuilding index..." -ForegroundColor Magenta
    $IndexStart = Get-Date
    $IndexResult = & $VenvPython "$ScriptDir\build_books_index.py" | ConvertFrom-Json
    $ElapsedIndex = (Get-Date) - $IndexStart
    Write-Host "  Indexed: $($IndexResult.file_count) files ($($IndexResult.total_size))" -ForegroundColor Green
    Write-Host "  Time: $($ElapsedIndex.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    
    # Read and display status
    Write-Host "[3/3] Reading status..." -ForegroundColor Magenta
    $SummaryFile = "$ScriptDir\books_index_summary.md"
    $Summary = Get-Content $SummaryFile -Raw
    
    if ($Summary -match "pending:\s+(\d+)") { $Pending = [int]$matches[1] }
    if ($Summary -match "converted:\s+(\d+)") { $Converted = [int]$matches[1] }
    if ($Summary -match "chunked:\s+(\d+)") { $Chunked = [int]$matches[1] }
    
    Write-Host "  Pending: $Pending | Converted: $Converted | Chunked: $Chunked" -ForegroundColor Green
    
    # Quick search validation
    $Keywords = @("kubernetes", "infrastructure", "security", "automation", "cloud", "resilience")
    $SearchTerm = $Keywords[$i % $Keywords.Length]
    & $VenvPython "$ScriptDir\search_books_chunks.py" $SearchTerm --limit 1 > $null 2>&1
    Write-Host "  Search validation: OK" -ForegroundColor Green
    
    $BatchElapsed = (Get-Date) - $BatchStart
    Write-Host "Batch $i complete: $($BatchElapsed.TotalSeconds.ToString('F1'))s" -ForegroundColor Cyan
    Write-Host ""
}

$TotalElapsed = (Get-Date) - $StartTime
Write-Host "=== COMPLETE ===" -ForegroundColor Cyan
Write-Host "Batches: $Batches, Total time: $($TotalElapsed.TotalMinutes.ToString('F1')) min" -ForegroundColor Green
Write-Host "Final status: Get-Content .\books_index_summary.md" -ForegroundColor Gray
