from setuptools import setup

deps = {
    "numpy",
}
test_deps = {
    "pytest>=7",
    "matplotlib",
}
typing_deps = {
    "mypy",
    *test_deps,
    "types-setuptools",
}
dev_deps = {
    *test_deps,
    "black",
    "isort",
    *typing_deps,
    "flake8",
    "flake8-pyproject",
}

setup(
    name="mathx",
    version="0+dev",
    python_requires=">=3.7",
    install_requires=[deps],
    extras_require={
        "test": test_deps,
        "typing": typing_deps,
        "dev": dev_deps,
    },
)
