"""
noxfile.py for running tests to find the lower bounds of the dependencies. (or any other versions incompatible with the current version)

Version used: nox-2024.10.9
"""
import nox

# Add the versions to test in sorted order

PYTEST_VERSIONS_TO_TEST = [
    "8.3.4",  # Tested ok with snappylapy 0.1.0
    "8.0.0",  # Tested ok with snappylapy 0.1.0
    "7.4.4",  # Tested ok with snappylapy 0.1.0
    "7.0.0",  # Tested ok with snappylapy 0.1.0
    # "6.2.5",  # Failed in snappylappy 0.1.0
    # "5.4.3",  # Failed in snappylappy 0.1.0
]

JSONPICKLE_VERSIONS_TO_TEST = [
    "4.0.1",  # Tested ok with snappylapy 0.1.0
    "3.4.2",  # Tested ok with snappylapy 0.1.0
    "2.2.0",  # Tested ok with snappylapy 0.1.0
    "1.5.2",  # Tested ok with snappylapy 0.1.0
    "1.4.2",  # Tested ok with snappylapy 0.1.0
    "1.0",  # Tested ok with snappylapy 0.1.0
    # "0.9.6",  # Failed in snappylapy 0.1.0
    # "0.3.0",  # Failed in snappylapy 0.1.0
]

@nox.session(venv_backend="conda")
@nox.parametrize("pytest_version", PYTEST_VERSIONS_TO_TEST)
def package_pytest(session, pytest_version: str):
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.install(f"pytest=={pytest_version}")
    # Print the pytest version
    session.run("poetry", "run", "pytest", "--version")
    session.run("poetry", "run", "pytest", "tests")
    session.run("poetry", "run", "mypy", "snappylapy")
    session.run("poetry", "run", "ruff", "check", "snappylapy")

@nox.session(venv_backend="conda")
@nox.parametrize("jsonpickle_version", JSONPICKLE_VERSIONS_TO_TEST)
def package_jsonpickle(session, jsonpickle_version: str):
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.install(f"jsonpickle=={jsonpickle_version}")
    session.run("poetry", "run", "pytest", "tests")
    session.run("poetry", "run", "mypy", "snappylapy")
    session.run("poetry", "run", "ruff", "check", "snappylapy")

@nox.session(venv_backend="conda")
def lower_bound_of_all_packages(session):
    session.install("poetry")
    session.run("poetry", "install", external=True)
    lowest_pytest_version = PYTEST_VERSIONS_TO_TEST[-1]
    lowest_jsonpickle_version = JSONPICKLE_VERSIONS_TO_TEST[-1]
    session.install(f"pytest=={lowest_pytest_version}")
    session.install(f"jsonpickle=={lowest_jsonpickle_version}")
    session.run("poetry", "run", "pytest", "tests")
    session.run("poetry", "run", "mypy", "snappylapy")
    session.run("poetry", "run", "ruff", "check", "snappylapy")
