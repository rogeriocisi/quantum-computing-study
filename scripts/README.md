# Scripts — Runnable Entry Points 🚀

This directory contains **standalone execution scripts** that import and orchestrate the reusable modules from `../src/`.

> These are **runners**, not importable modules. They are meant to be run directly from the command line.

## 📋 Available Scripts

| Script | Description |
| :--- | :--- |
| `capstone_demo.py` | Capstone pipeline demo: local simulation + optional IBM Quantum Runtime submission. |

## ▶️ How to Run

```bash
# From the project root
python scripts/capstone_demo.py
```

## 📌 Convention (from `docs/system/constitution.md`)
- Scripts import from `src/` — never the other way around.
- No business logic should live here; logic belongs in `src/`.
- New execution scripts should be added here and documented in this README.
