<div align="center">

# repos-management

Tooling for managing course repositories in **HIT-A**.

[English](README.md) | [中文](README.zh-CN.md)

</div>

---

## What this repo does

This repository provides:

- A **single CLI** entrypoint for common operations:
  - Convert `readme.toml` ⇄ `README.md`
- The **reusable GitHub Actions workflow** used by course repositories for bidirectional lossless conversion.

The preferred way to use this repo is:

```bash
python3 -m repos_management --help
```

---

## Requirements

- Python **3.11+**
- Optional (recommended): [GitHub CLI](https://cli.github.com/) (`gh`)

---

## Quickstart

### 1) Convert TOML → README

```bash
python3 -m repos_management rdme toml2md --input path/to/readme.toml --overwrite
```

### 2) Convert README → TOML

```bash
python3 -m repos_management rdme md2toml --input path/to/README.md --overwrite
```

## CLI reference

### `rdme toml2md`

Convert `readme.toml` → `README.md`.

```bash
python3 -m repos_management rdme toml2md --input <file-or-dir> [--output <file>] [--overwrite]
```

- If `--input` is a directory, it scans `**/readme.toml` and writes `README.md` next to each file.

### `rdme md2toml`

Convert `README.md` → `readme.toml`.

```bash
python3 -m repos_management rdme md2toml --input <file-or-dir> [--output <file>] [--overwrite] [--verbose]
```

- If `--input` is a directory, it scans `**/README.md` and writes `readme.toml` next to each file.

## Lecturers TOML schema (breaking change)

Only the **new** lecturers schema is supported:

```toml
[lecturers]

[[lecturers.intro]]
content = "..."  # optional
# author is optional
# author = { name = "", link = "", date = "" }

[[lecturers.items]]
name = "郑宜峰"

[[lecturers.items.reviews]]
content = "挺好的老师，交流时感觉很亲切。"
# author is optional
# author = { name = "xxx", link = "xxx", date = "xxx" }

[[lecturers.summary]]
content = "..."  # optional
```

Legacy TOML `[[lecturers]]` / `[[lecturers.reviews]]` is **not supported** and will raise an error.

---

## How course repositories CI works (high-level)

A typical course repository contains:

- `.github/workflows/trigger-workflow.yml`

This workflow calls the reusable workflow in this repo:

```yaml
uses: HIT-A/repos-management/.github/workflows/reusable_worktree_generate.yml@main
```

After `repos-management` changes are merged to `main`, course repositories continue running their own workflows with the reusable bidirectional pipeline.

---

## Maintenance scripts

Some power tools remain in `./scripts/` (use with care):

### Conversion Scripts (kept)
- `convert_toml_to_readme.py` - Convert TOML to README
- `readme_to_toml.py` - Convert README to TOML

### CI Scripts (kept)
- `rdme_autogen.py` - Used by course repositories CI to orchestrate bidirectional conversion
