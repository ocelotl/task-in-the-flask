from task_in_the_flask import hello_world


def test_hello_world():
    assert hello_world() == "<p>Hello, World!</p>"
