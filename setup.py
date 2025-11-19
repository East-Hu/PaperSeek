"""
Paper-to-Action Setup Script
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# 读取依赖
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")

setup(
    name="paper-to-action",
    version="0.1.0",
    author="East-Hu",
    author_email="",
    description="自动化论文爬取与智能摘要工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/East-Hu/paper-to-action",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "paper-robot=paper_to_action.cli.interface:main",
            "pr=paper_to_action.cli.interface:main",  # 简短别名
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
