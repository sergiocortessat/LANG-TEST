# Python environment — uv + `.venv` (this project)

Use this guide when you are unsure whether you are using **project Python** (`.venv`) or **system Python**, or when you need to add/remove packages.

---

## Quick start (this repo)

```bash
cd /Users/laburo/Documents/NEOLAND-BACKEDN-STUDY-PYTHON

make sync     # first time, or after pulling dependency changes
make dev      # FastAPI at http://127.0.0.1:8000/docs
```

You do **not** need to activate `.venv` if you use `make …` or `uv run …` (uv picks `.venv` for you).

---

## Three pieces to remember

| Piece | Role |
|--------|------|
| **`uv`** (global CLI) | Installed once on your machine (`~/.local/bin/uv`). Creates envs, installs deps, runs commands. **Not** the same as `pip install fastapi` globally. |
| **`pyproject.toml`** | What this project **directly** depends on (e.g. FastAPI, uvicorn). Like `dependencies` in `package.json`. |
| **`uv.lock`** | Exact versions of **every** package (including transitive deps like Pydantic). Like `package-lock.json`. **Commit this file.** |
| **`.venv/`** | Project-local Python + installed packages. Gitignored; recreated with `uv sync`. |

Flow:

```text
pyproject.toml  →  uv sync  →  .venv/ + uv.lock
```

There is **no** `requirements.txt` in this project anymore.

---

## Install `uv` on your machine (one time)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Add to shell (installer usually adds this to `~/.zshrc`):

```bash
. "$HOME/.local/bin/env"
```

Test in a **new** terminal:

```bash
which uv
uv --version
```

---

## Every time you open the project

**Option A — recommended (no activation):**

```bash
cd /Users/laburo/Documents/NEOLAND-BACKEDN-STUDY-PYTHON
make dev
# or: uv run python -m mypy src
```

**Option B — classic activate (optional):**

```bash
source .venv/bin/activate
python --version
# prompt may show (.venv)
deactivate   # when done
```

Run `make sync` (or `uv sync --all-groups`) when:

- First clone
- Someone changed `pyproject.toml` or `uv.lock`
- You switched branches with dependency changes

---

## Check which Python you are using

```bash
which python
python --version
uv run which python
```

**Good (this project):**

```text
.../NEOLAND-BACKEDN-STUDY-PYTHON/.venv/bin/python
```

**Bad (system — wrong for installed packages):**

```text
/usr/bin/python3
/opt/homebrew/bin/python3
```

With activation:

```bash
source .venv/bin/activate
which python
```

---

## Cursor / VS Code

`.vscode/settings.json` points the editor at:

```json
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

**Editor Run / debugger / autocomplete** → uses `.venv`.

**Integrated terminal** → uses system Python until you `source .venv/bin/activate` or use `uv run` / `make`. Open a new terminal after changing `~/.zshrc`.

Pyright config: `pyrightconfig.json` (`include`: `src`, `venv`: `.venv`).

---

## Makefile shortcuts

From repo root:

| Command | Action |
|---------|--------|
| `make sync` / `make install` | `uv sync --all-groups` |
| `make help` | List targets |

---

## Troubleshooting: `externally-managed-environment`

macOS/Homebrew Python blocks **system** `pip install`. You should not need system pip for this project.

**Fix:** use uv only:

```bash
uv sync
uv add <package>
```

If `.venv` is broken, recreate it:

```bash
rm -rf .venv
uv sync --all-groups
```

---

## Cheat sheet

```bash
cd /Users/laburo/Documents/NEOLAND-BACKEDN-STUDY-PYTHON

make sync
make dev

uv add httpx
uv remove httpx
uv tree

uv run mypy src
source .venv/bin/activate   # optional
deactivate
```

---

## Mental model

```text
uv (global)     = npm/pnpm binary on your PATH
pyproject.toml  = package.json "dependencies"
uv.lock         = lockfile
.venv/          = node_modules (Python packages live here)

make dev        = npm run dev
uv add foo      = npm install foo --save
uv sync         = npm ci / pnpm install
```

```text
System Python  = shared building kitchen
Project .venv  = your apartment kitchen (this repo only)

uv run / make  → use apartment kitchen without "activating"
source .venv/bin/activate  → same kitchen, classic shell habit
```
