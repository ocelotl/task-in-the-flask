from nox import session


@session(reuse_venv=True)
def test(session):
    session.install("-e", ".")
    session.install("pytest")
    session.install("ipdb")

    if session.posargs:
        session.run("pytest", *session.posargs)
    else:
        session.run("pytest", "tests")


@session
def lint(session):
    session.install("flake8")
    session.run("flake8")
