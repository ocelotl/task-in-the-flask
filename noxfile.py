from nox import session


@session
def test(session):
    session.install("pytest")
    session.run("pytest")


@session
def lint(session):
    session.install("flake8")
    session.run("flake8")
