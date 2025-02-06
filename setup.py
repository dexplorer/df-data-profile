import setuptools

setuptools.setup(
    name="dp_app",
    version="1.0.2",
    scripts=["./scripts/dp_app"],
    author="Me",
    description="Data profiling app install.",
    url="https://github.com/dexplorer/df-data-profile",
    packages=["dp_app"],
    # packages = find_packages(),
    install_requires=[
        "setuptools",
        "spacy==3.8.3",
        "utils@git+https://github.com/dexplorer/utils#egg=utils-1.0.3",
        "metadata@git+https://github.com/dexplorer/df-metadata#egg=metadata-1.0.9",
        "app_calendar@git+https://github.com/dexplorer/df-app-calendar#egg=app_calendar-1.0.2",
    ],
    python_requires=">=3.12",
)
