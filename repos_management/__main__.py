from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _run_python_script(script_name: str, args: list[str]) -> int:
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    cmd = [sys.executable, str(script_path), *args]
    return subprocess.call(cmd)


def cmd_rdme_toml2md(ns: argparse.Namespace) -> int:
    args: list[str] = ["--input", ns.input]
    if ns.output:
        args += ["--output", ns.output]
    if ns.overwrite:
        args += ["--overwrite"]
    return _run_python_script("convert_toml_to_readme.py", args)


def cmd_rdme_md2toml(ns: argparse.Namespace) -> int:
    args: list[str] = ["--input", ns.input]
    if ns.output:
        args += ["--output", ns.output]
    if ns.overwrite:
        args += ["--overwrite"]
    if ns.verbose:
        args += ["--verbose"]
    return _run_python_script("readme_to_toml.py", args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m repos_management",
        description="HIT-A repository management CLI",
    )

    sp = p.add_subparsers(dest="group", required=True)

    # rdme
    rdme = sp.add_parser("rdme", help="README/TOML conversion")
    rdme_sp = rdme.add_subparsers(dest="command", required=True)

    toml2md = rdme_sp.add_parser("toml2md", help="Convert readme.toml -> README.md")
    toml2md.add_argument(
        "--input", "-i", required=True, help="Input TOML file or directory"
    )
    toml2md.add_argument("--output", "-o", help="Output path (single-file mode only)")
    toml2md.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing README"
    )
    toml2md.set_defaults(func=cmd_rdme_toml2md)

    md2toml = rdme_sp.add_parser("md2toml", help="Convert README.md -> readme.toml")
    md2toml.add_argument(
        "--input", "-i", required=True, help="Input README file or directory"
    )
    md2toml.add_argument(
        "--output", "-o", help="Output TOML path (single-file mode only)"
    )
    md2toml.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing TOML"
    )
    md2toml.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    md2toml.set_defaults(func=cmd_rdme_md2toml)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    func = getattr(ns, "func", None)
    if func is None:
        parser.print_help()
        return 2
    return int(func(ns))


if __name__ == "__main__":
    raise SystemExit(main())
