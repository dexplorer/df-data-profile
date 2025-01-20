import setuptools

setuptools.setup(
    name="dp_app",
    version="1.0.0",
    scripts=["./scripts/dp_app"],
    author="Me",
    description="Data profiling app install.",
    url="https://github.com/dexplorer/df-data-profile",
    packages=["dp_app"],
    # packages = find_packages(),
    install_requires=[
        "setuptools",
        "spacy==3.8.3",
    ],
    python_requires=">=3.12",
)
