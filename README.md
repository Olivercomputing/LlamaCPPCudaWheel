# llama-cpp-cuda-binaries

A GitHub Actions pipeline that automatically repackages the pre-built
[ai-dock/llama.cpp-cuda](https://github.com/ai-dock/llama.cpp-cuda) binary
releases into a platform-specific Python wheel (`.whl`).

The published distribution is :

- Package name: `llama-cpp-cuda-binaries`
- Import name: `llama_cpp_cuda_binaries`
- Wheel tag: `py3-none-manylinux_2_34_x86_64`

## How it works

1. **Daily cron** (06:00 UTC) or **manual dispatch** triggers the workflow.
2. The workflow fetches the **latest release** from `ai-dock/llama.cpp-cuda`
   (or a specific tag you provide).
3. All `.tar.gz` assets are downloaded and extracted into the wheel's package
   data directory, preserving the top-level CUDA directory that already exists
   inside each archive.
4. A platform-tagged wheel (`py3-none-manylinux_2_34_x86_64`) is built.
5. The workflow publishes:
   - a versioned GitHub release named `wheel-b<UPSTREAM_BUILD>`
   - a rolling GitHub release named `wheel-latest`
   - a GitHub Pages "simple" package index for `pip`
6. A duplicate-check ensures the same upstream tag is never repackaged twice.
7. Older versioned releases are pruned, keeping the 10 most recent.

## Installation

Install the newest published wheel without naming a build number:

```bash
pip install --extra-index-url "https://Olivercomputing.github.io/LlamaCPPServerWheel/simple/" llama-cpp-cuda-binaries
```

That command uses the GitHub Pages simple index, which always points `pip`
at the newest published wheel for this repository.

If you want a pinned build, install from a versioned release URL:

```bash
pip install "https://github.com/Olivercomputing/LlamaCPPServerWheel/releases/download/wheel-b8192/llama_cpp_cuda_binaries-8192-py3-none-manylinux_2_34_x86_64.whl"
```

If you prefer to download the wheel manually from the repo's
[Releases](../../releases) page, install it with:

```bash
pip install llama_cpp_cuda_binaries-<VERSION>-py3-none-manylinux_2_34_x86_64.whl
```

The rolling `wheel-latest` release also exists, but its asset filename still
contains the package version, so it is less convenient as a stable `pip`
install target than the simple index above.

To use the GitHub Pages install path, set **Settings → Pages → Build and
deployment** to **GitHub Actions** so the workflow can publish the index.

## What You Get

This wheel does not contain a compiled Python extension module. It contains:

- a small pure-Python helper package
- the upstream `llama.cpp` CUDA binaries and shared libraries under `data/`

That is why the wheel is tagged `py3-none-manylinux_2_34_x86_64` instead of a
CPython-version-specific tag like `cp311` or `cp312`.

## Python API

After installation:

```python
import llama_cpp_cuda_binaries

# Package version (matches llama.cpp build number)
llama_cpp_cuda_binaries.version()          # e.g. "8192"

# Upstream release tag
llama_cpp_cuda_binaries.upstream_tag()     # e.g. "b8192"

# Path to binaries — use in subprocess calls, scripts, etc.
llama_cpp_cuda_binaries.bin_path()                  # root data dir
llama_cpp_cuda_binaries.bin_path("cuda-12.8")       # specific CUDA variant

# List all shipped CUDA variants
llama_cpp_cuda_binaries.available_variants()         # ["cuda-12.8"]
```

On import, the package also adds the binary directories to `$PATH`, so you
can call bundled executables like `llama-server` directly from a shell after
`import llama_cpp_cuda_binaries`.

## Manual trigger

Go to **Actions → Repackage llama.cpp-cuda as Python Wheel → Run workflow**
and optionally provide a specific release tag (e.g. `b8192`). Leave it blank
to use the latest release.

## Repository structure

```
.github/workflows/repackage-wheel.yml   # the CI pipeline
pyproject.toml                           # wheel build metadata
setup.py                                 # wheel-tag override to py3-none-<platform>
setup.cfg                                # bdist_wheel config
src/llama_cpp_cuda_binaries/
    __init__.py                          # Python helper API
    VERSION                              # populated at build time
    UPSTREAM_TAG                         # populated at build time
    data/                                # extracted binaries (populated at build time)
```

## License

This repackaging pipeline is released under the MIT License.
The llama.cpp binaries themselves are subject to the
[llama.cpp license](https://github.com/ggml-org/llama.cpp/blob/master/LICENSE).
