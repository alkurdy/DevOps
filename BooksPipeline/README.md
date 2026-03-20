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
