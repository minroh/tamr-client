from pathlib import Path
import sys

from invoke import task

beta = "TAMR_CLIENT_BETA=1"


def _find_packages(path: Path):
    for pkg in path.iterdir():
        if pkg.is_dir() and len(list(pkg.glob("**/*.py"))) >= 1:
            yield pkg


@task
def lint(c):
    c.run("poetry run flake8 .", echo=True, pty=True)


@task
def format(c, fix=False):
    check = "" if fix else "--check"
    c.run(f"poetry run black {check} .", echo=True, pty=True)


@task
def typecheck(c, warn=True):
    exit_code = 0
    repo = Path(".")

    tc = repo / "tamr_client"
    result = c.run(f"poetry run mypy --package {tc}", echo=True, pty=True, warn=warn)
    if not result.exited == 0:
        exit_code = result.exited

    tc_tests = " ".join(
        str(x) for x in (repo / "tests" / "tamr_client").glob("**/*.py")
    )
    c.run(f"poetry run mypy {tc_tests}", echo=True, pty=True, warn=warn)
    if not result.exited == 0:
        exit_code = result.exited

    sys.exit(exit_code)


@task
def test(c):
    c.run(f"{beta} poetry run pytest", echo=True, pty=True)


@task
def docs(c):
    c.run(
        f"{beta} poetry run sphinx-build -b html docs docs/_build -W",
        echo=True,
        pty=True,
    )
