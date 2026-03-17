<div align="center">

# repos-management

用于管理 **HIT-A** 组织下课程仓库的工具集。

[中文](README.zh-CN.md) | [English](README.md)

</div>

---

## 本仓库做什么

本仓库提供：

- 一个统一的 **Python CLI** 入口，用于常用操作：
  - `readme.toml` ⇄ `README.md` 双向转换
- 课程仓库用于双向无损互转的 **reusable GitHub Actions workflow**。

推荐使用方式：

```bash
python3 -m repos_management --help
```

---

## 环境要求

- Python **3.11+**
- 可选（推荐）：[GitHub CLI](https://cli.github.com/)（`gh`）

---

## 快速开始

### 1) TOML → README

```bash
python3 -m repos_management rdme toml2md --input path/to/readme.toml --overwrite
```

### 2) README → TOML

```bash
python3 -m repos_management rdme md2toml --input path/to/README.md --overwrite
```

## CLI 参考

### `rdme toml2md`

将 `readme.toml` 转换为 `README.md`。

```bash
python3 -m repos_management rdme toml2md --input <文件或目录> [--output <文件>] [--overwrite]
```

- 若 `--input` 是目录，会扫描 `**/readme.toml`，并在同目录生成 `README.md`

### `rdme md2toml`

将 `README.md` 转换为 `readme.toml`。

```bash
python3 -m repos_management rdme md2toml --input <文件或目录> [--output <文件>] [--overwrite] [--verbose]
```

- 若 `--input` 是目录，会扫描 `**/README.md`，并在同目录生成 `readme.toml`

## lecturers TOML 结构（破坏性变更）

仅支持 **新版** lecturers 结构：

```toml
[lecturers]

[[lecturers.intro]]
content = "..."  # 可选
# author 可选
# author = { name = "", link = "", date = "" }

[[lecturers.items]]
name = "郑宜峰"

[[lecturers.items.reviews]]
content = "挺好的老师，交流时感觉很亲切。"
# author 可选
# author = { name = "xxx", link = "xxx", date = "xxx" }

[[lecturers.summary]]
content = "..."  # 可选
```

旧版 `[[lecturers]]` / `[[lecturers.reviews]]` **不再支持**，会直接报错。

---

## 课程仓库 CI 工作方式（概览）

典型课程仓库包含：

- `.github/workflows/trigger-workflow.yml`

它会调用本仓库的 reusable workflow：

```yaml
uses: HIT-A/repos-management/.github/workflows/reusable_worktree_generate.yml@main
```

当 `repos-management` 的改动合并到 `main` 后，课程仓库会通过各自 workflow 继续走双向互转流程。

---

## 维护脚本

部分"强力工具"仍保留在 `./scripts/` 下（谨慎使用）：

### 转换脚本（保留）
- `convert_toml_to_readme.py` - TOML 转 README
- `readme_to_toml.py` - README 转 TOML

### CI 脚本（保留）
- `rdme_autogen.py` - 课程仓库 CI 中用于编排双向互转
