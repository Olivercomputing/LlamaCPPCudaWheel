"""
llama-cpp-cuda-binaries
~~~~~~~~~~~~~~~~~~~~~~~

Pre-built llama.cpp binaries with CUDA support, distributed as a Python wheel.

Usage::

    import llama_cpp_cuda_binaries

    # Path to the root data directory containing extracted binaries
    print(llama_cpp_cuda_binaries.bin_path())

    # Path to a specific CUDA version's binaries
    print(llama_cpp_cuda_binaries.bin_path("cuda-12.8"))

    # List available CUDA variants
    print(llama_cpp_cuda_binaries.available_variants())
"""

from __future__ import annotations

import os
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_DATA = _HERE / "data"


def version() -> str:
    """Return the package version (matches the upstream llama.cpp build number)."""
    return (_HERE / "VERSION").read_text().strip()


def upstream_tag() -> str:
    """Return the upstream ai-dock/llama.cpp-cuda release tag."""
    return (_HERE / "UPSTREAM_TAG").read_text().strip()


def bin_path(variant: str | None = None) -> Path:
    """Return the filesystem path to the extracted binaries.

    Parameters
    ----------
    variant : str, optional
        A CUDA variant subdirectory name such as ``"cuda-12.8"``.
        If *None*, returns the root ``data/`` directory.

    Returns
    -------
    pathlib.Path
        Absolute path to the binary directory.

    Raises
    ------
    FileNotFoundError
        If the requested variant does not exist.
    """
    if variant is None:
        return _DATA

    target = _DATA / variant
    if not target.is_dir():
        available = ", ".join(available_variants()) or "(none)"
        raise FileNotFoundError(
            f"Variant '{variant}' not found. Available: {available}"
        )
    return target


def available_variants() -> list[str]:
    """List the CUDA variant subdirectories shipped in this wheel."""
    if not _DATA.is_dir():
        return []
    return sorted(
        d.name for d in _DATA.iterdir() if d.is_dir()
    )


# Convenience: add binary dirs to PATH when the package is imported,
# so that tools like `llama-cli` are directly callable.
def _add_to_path() -> None:
    for variant_dir in _DATA.iterdir():
        if variant_dir.is_dir():
            # Add both the variant root and any bin/ subdirectory
            for candidate in [variant_dir, variant_dir / "bin"]:
                if candidate.is_dir():
                    str_path = str(candidate)
                    if str_path not in os.environ.get("PATH", ""):
                        os.environ["PATH"] = str_path + os.pathsep + os.environ.get("PATH", "")


_add_to_path()
