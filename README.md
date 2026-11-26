# ohtuvarasto26

[![CI](https://github.com/vvvilho/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/vvvilho/ohtuvarasto/actions/workflows/main.yml)
[![codecov](https://codecov.io/github/vvvilho/ohtuvarasto/graph/badge.svg?token=BFR1HH9DVS)](https://codecov.io/github/vvvilho/ohtuvarasto)

## Warehouse web app

Install dependencies and start the Flask app from the repository root:

```sh
uv sync
uv run python src/app.py
```

Then open <http://127.0.0.1:5000>. Warehouses and their inventory are kept in
memory while the app is running.
