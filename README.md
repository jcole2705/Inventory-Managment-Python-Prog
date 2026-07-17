# Inventory Control System

A Python/Tkinter desktop application built during my engineering internship with the
North Carolina Department of Adult Correction to automate asset inventory management —
replacing a manual, one-by-one folder creation process with batch operations.

## What it does

- **Batch record creation** — paste lists of serial numbers, owner names, and models,
  and the app generates a folder per asset with a metadata file (serial, owner, model, status)
- **Status classification** — assets are tagged as Located, Surplus, or In Stock
- **Filename sanitization** — strips illegal characters from serials so records are always valid paths
- **Integrated file transfer** — select files and copy them into any asset folder, with
  per-file error handling so one failure doesn't halt the batch
- **Live operation console** — every action logs to an in-app output panel

## Why I built it

The department needed an inventory management system for its assets. Creating each record
manually would have taken hours; I built this instead. It went from idea to working tool
self-directed — nobody asked for it, the manual process was just slow.

## Tech

- Python 3, Tkinter (standard library only — no external dependencies)
- `pathlib` for filesystem operations, `shutil.copy2` to preserve file metadata
