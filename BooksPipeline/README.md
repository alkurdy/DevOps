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
