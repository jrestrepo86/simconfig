from setuptools import setup


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="simconfig",
    version="3.0",
    description="Configuración de Simulaciones",
    long_description=readme(),
    url="https://jrinckoar@bitbucket.org/jrinckoar/simulationconfig.git",
    author="Juan F. Restrepo",
    author_email="juan.restrepo@uner.edu.ar",
    license="MIT",
    packages=["simconfig"],
    entry_points={
        "console_scripts": ["simconfig = simulationconfig.simconfig:main"],
    },
    install_requires=[
        "progress",
        "pandas",
    ],
    test_suite="nose.collector",
    tests_require=["nose", "nose-cover3"],
    zip_safe=False,
)
