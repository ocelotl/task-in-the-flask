from nox import session


@session
def test(session):
    session.install(".")
    session.install("pytest")
    session.install("flask")
    session.run("pytest", "tests")


@session
def lint(session):
    session.install("flake8")
    session.run("flake8")
