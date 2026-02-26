#!/usr/bin/env python3
"""
Build script for VideoCaptioner using PyInstaller.

Usage:
    python scripts/build.py          # Build for current platform
    python scripts/build.py --clean  # Clean build artifacts first

Requirements:
    pip install pyinstaller
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SPEC_FILE = ROOT_DIR / "VideoCaptioner.spec"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"


def clean():
    """Remove previous build artifacts."""
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            print(f"Removing {d}")
            shutil.rmtree(d)


def build():
    """Run PyInstaller with the spec file."""
    if not SPEC_FILE.exists():
        print(f"ERROR: Spec file not found: {SPEC_FILE}")
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(SPEC_FILE),
        "--noconfirm",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
    ]

    print(f"Building VideoCaptioner for {platform.system()} ({platform.machine()})...")
    print(f"Command: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if result.returncode != 0:
        print("\nBuild FAILED!")
        sys.exit(1)

    # Print output location
    output_dir = DIST_DIR / "VideoCaptioner"
    if platform.system() == "Darwin":
        app_bundle = DIST_DIR / "VideoCaptioner.app"
        if app_bundle.exists():
            print(f"\nmacOS app bundle: {app_bundle}")
    if output_dir.exists():
        print(f"\nBuild output: {output_dir}")

    print("\nBuild SUCCESS!")


def verify():
    """Basic verification that the build output exists and has expected files."""
    output_dir = DIST_DIR / "VideoCaptioner"
    if not output_dir.exists():
        print("ERROR: Build output directory not found")
        sys.exit(1)

    # Check executable
    if platform.system() == "Windows":
        exe = output_dir / "VideoCaptioner.exe"
    else:
        exe = output_dir / "VideoCaptioner"

    if not exe.exists():
        print(f"ERROR: Executable not found: {exe}")
        sys.exit(1)

    # PyInstaller places bundled data in _internal/ directory
    internal_dir = output_dir / "_internal"
    data_root = internal_dir if internal_dir.exists() else output_dir

    # Check resource directories are bundled
    expected_resources = [
        "resource/assets/logo.png",
        "resource/fonts/LXGWWenKai-Regular.ttf",
        "resource/subtitle_style/default.json",
        "resource/translations",
        "app/core/prompts/split/semantic.md",
    ]

    missing = []
    for res in expected_resources:
        if not (data_root / res).exists():
            missing.append(res)

    if missing:
        print("WARNING: Missing bundled resources:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("All expected resources found in bundle.")

    print(f"\nExecutable size: {exe.stat().st_size / (1024*1024):.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="Build VideoCaptioner")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts first")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing build")
    args = parser.parse_args()

    if args.verify_only:
        verify()
        return

    if args.clean:
        clean()

    build()
    verify()


if __name__ == "__main__":
    main()
