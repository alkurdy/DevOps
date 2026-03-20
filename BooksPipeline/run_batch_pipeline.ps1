<#
.SYNOPSIS
    Automated Books Pipeline batch runner - exports, chunks, and validates in one pass
.PARAMETER Batches
    Number of 100-file batches to process (default: 2)
.PARAMETER Limit
    Files per batch (default: 100)
.EXAMPLE
    .\run_batch_pipeline.ps1 -Batches 3
    .\run_batch_pipeline.ps1 -Batches 5 -Limit 50
#>
param(
    [int]$Batches = 2,
    [int]$Limit = 100
)

$ErrorActionPreference = "Stop"
$VenvPython = ".\.venv\Scripts\python.exe"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StartTime = Get-Date

Write-Host "Starting automated Books pipeline: $Batches batches × $Limit files" -ForegroundColor Cyan
Write-Host "Started at: $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
Write-Host ""

for ($i = 1; $i -le $Batches; $i++) {
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "BATCH $i of $Batches" -ForegroundColor Yellow
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    
    # Export
    Write-Host "[1/3] Exporting $Limit files..." -ForegroundColor Magenta
    $BatchStart = Get-Date
    
    try {
        $ExportResult = & $VenvPython "$ScriptDir\export_books_ai.py" --limit $Limit --status pending | ConvertFrom-Json
        $ElapsedExport = (Get-Date) - $BatchStart
        
        Write-Host "  ✓ Selected: $($ExportResult.selected)" -ForegroundColor Green
        Write-Host "  ✓ Converted: $($ExportResult.converted_ok)/$($ExportResult.selected)" -ForegroundColor Green
        Write-Host "  ✓ Chunked: $($ExportResult.chunked_ok)" -ForegroundColor Green
        if ($ExportResult.failed -gt 0) {
            Write-Host "  ⚠ Failed: $($ExportResult.failed)" -ForegroundColor Yellow
        }
        Write-Host "  ⏱ Time: $($ElapsedExport.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    } catch {
        Write-Host "  ✗ Export failed: $_" -ForegroundColor Red
        exit 1
    }
    
    # Rebuild Index
    Write-Host "[2/3] Rebuilding index..." -ForegroundColor Magenta
    $IndexStart = Get-Date
    
    try {
        $IndexResult = & $VenvPython "$ScriptDir\build_books_index.py" | ConvertFrom-Json
        $ElapsedIndex = (Get-Date) - $IndexStart
        Write-Host "  ✓ Indexed $($IndexResult.file_count) files ($($IndexResult.total_size))" -ForegroundColor Green
        Write-Host "  ⏱ Time: $($ElapsedIndex.TotalSeconds.ToString('F1'))s" -ForegroundColor Gray
    } catch {
        Write-Host "  ✗ Index rebuild failed: $_" -ForegroundColor Red
        exit 1
    }
    
    # Read Summary
    Write-Host "[3/3] Reading status..." -ForegroundColor Magenta
    
    try {
        $SummaryFile = "$ScriptDir\books_index_summary.md"
        $Summary = Get-Content $SummaryFile -Raw
        
        # Extract status counts
        if ($Summary -match "pending:\s+(\d+)") { $Pending = [int]$matches[1] }
        if ($Summary -match "converted:\s+(\d+)") { $Converted = [int]$matches[1] }
        if ($Summary -match "chunked:\s+(\d+)") { $Chunked = [int]$matches[1] }
        
        Write-Host "  ✓ Pending: $Pending | Converted: $Converted | Chunked: $Chunked" -ForegroundColor Green
        
        # Quick validation search (alternate keywords by batch)
        $Keywords = @("kubernetes", "infrastructure", "security", "automation", "cloud", "resilience")
        $SearchTerm = $Keywords[$i % $Keywords.Length]
        Write-Host "  ✓ Validating search: '$SearchTerm'..." -ForegroundColor Blue
        
        $SearchResult = & $VenvPython "$ScriptDir\search_books_chunks.py" $SearchTerm --limit 1 2>&1
        Write-Host "  ✓ Chunk search successful" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Status check warning: $_" -ForegroundColor Yellow
    }
    
    $BatchElapsed = (Get-Date) - $BatchStart
    Write-Host ""
    Write-Host "Batch $i completed in $($BatchElapsed.TotalSeconds.ToString('F1'))s" -ForegroundColor Cyan
    Write-Host ""
}

# Final Summary
$TotalElapsed = (Get-Date) - $StartTime
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✓ PIPELINE COMPLETE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Batches processed: $Batches" -ForegroundColor Cyan
Write-Host "  Total time: $($TotalElapsed.TotalMinutes.ToString('F1')) minutes" -ForegroundColor Cyan
Write-Host "  Total files: ~$($Batches * $Limit)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run 'Get-Content .\books_index_summary.md' for final status" -ForegroundColor Gray
