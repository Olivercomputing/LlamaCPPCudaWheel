"""
Custom setup.py to produce a platform-specific wheel tag.

The upstream binaries are Linux x86_64 ELF files linked against CUDA,
so the wheel must be tagged as a platform wheel rather than "any".
"""

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel


class PlatformWheel(bdist_wheel):
    """Build a platform wheel without tying it to one CPython ABI."""

    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        _, _, platform = super().get_tag()
        return "py3", "none", platform


setup(
    cmdclass={"bdist_wheel": PlatformWheel},
)
