# Books Pipeline

This folder indexes and exports `D:\\Books` content into AI-readable markdown/chunks.

## Files
- `build_books_index.py`: scans `D:\\Books` and builds:
  - `books_index.json`
  - `books_index.csv`
  - `books_index_summary.md`
- `export_books_ai.py`: converts/chunks indexed files to:
  - `D:\\Books\\ConvertedAI`
  - `D:\\Books\\ChunkedAI`
- `query_books_index.py`: searches the index quickly by substring.

## Typical Usage

Build/refresh index:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/build_books_index.py
```

Export first 50 pending files:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/export_books_ai.py --limit 50 --status pending
```

Query index:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/query_books_index.py "systems thinking"
```

## Recurring Batch Runbook

Use this 4-step sequence for regular throughput runs.

1. Export next batch of pending files (start with 100, adjust if needed):

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/export_books_ai.py --limit 100 --status pending
```

2. Rebuild the index so status counts are current:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/build_books_index.py
```

3. Sanity-check retrieval quality from chunked output:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/search_books_chunks.py "resilience" --limit 5
```

4. Inspect `books_index_summary.md` and continue until pending reaches target threshold.

Recommended cadence:
- Daily quick run: `--limit 50`
- Weekly bulk run: `--limit 100` to `--limit 200`

## One-Shot Automation

Run batches with logging and automatic stop conditions:

```powershell
powershell.exe -ExecutionPolicy Bypass -File DevOps/BooksPipeline/run_batches.ps1 -UntilEmpty -MaxBatches 25 -Limit 100
```

Outputs are written to `DevOps/BooksPipeline/logs/`:
- `run_batches_YYYYMMDD_HHMMSS.log`
- `run_batches_YYYYMMDD_HHMMSS.json`

The script stops automatically when:
- pending reaches `0`
- no files are selected
- pending fails to improve across consecutive batches

## Pending Diagnostics

To inspect why remaining files stay pending:

```powershell
c:/Users/alkur/OneDrive/Documents/DevOps/.venv/Scripts/python.exe DevOps/BooksPipeline/diagnose_pending.py --limit 100
```

Outputs:
- `pending_diagnostics.json`
- `pending_diagnostics.md`

## MOBI Support (Calibre Fallback)

`export_books_ai.py` now attempts MOBI conversion through Calibre `ebook-convert` when direct conversion fails.

Install Calibre (or ensure `ebook-convert.exe` is on `PATH`) to enable this fallback on Windows:

```powershell
choco install calibre -y
```
