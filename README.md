# LANG-TEST — AI Invoice Assistant lab

A small Python lab for learning LangChain, LangGraph, MCP, and LangSmith.

We build it in stages. **Stage 0 is environment only** — no LangChain yet.

## Stage 0 — environment

You need:

- [uv](https://docs.astral.sh/uv/) (this repo already uses it)
- [Ollama](https://ollama.com) running locally
- A pulled model, for example `llama3.2` or `qwen2.5-coder:7b`

```bash
cp .env.example .env    # already done if you cloned this working copy
make sync
make check-env
```

`make check-env` should print `OK` and list your Ollama models.

Edit `OLLAMA_MODEL` in `.env` if you want to use `qwen2.5-coder:7b` instead of `llama3.2`.

Do **not** put API keys in git. `.env` is gitignored.

## Stage 1 — LangChain talks to Ollama

```bash
make lesson-1
```

Sends one chat prompt through LangChain to your local Ollama model.

## Stage 2 — prompts and structured output

```bash
make lesson-2
```

Turns the sample Flower Export invoice into a Pydantic `Invoice` object (fields, not a paragraph).

## Stage 3 — Python function vs LangChain tool

```bash
make lesson-3
```

`is_overdue` is a normal function we call. `lookup_supplier` is a tool the model may request.

## Later stages (not built yet)

4. LangGraph
5. MCP filesystem tools
6. LangSmith tracing
7. Junior-facing guide
