# encoding: utf-8

from __future__ import unicode_literals, print_function

import operator

from marrow.testing import Suite


@Suite.decorated
def suite(environ):
    # Setup.
    print("Tests starting.\n")
    
    yield
    
    # Tear-down.
    print("Finished.")


@suite.feature("mathematics")
def mathematics(environ):
    pass


@mathematics.scenario("basic operations")
def operations(environ):
    return environ


@operations.given("a number, x, that is odd")
def x_odd(environ):
    environ.x = 27
    return environ


@x_odd.given("a number, y, that is even")
def x_odd_y_even(environ):
    environ.y = 42
    return environ


@x_odd_y_even.when("multiplied together")
def multiplied(environ):
    environ.result = operator.mul(environ.x, environ.y)
    return environ


@multiplied.then("the result is even")
def is_even(environ):
    assert 'result' in environ, "Result missing."
    assert environ.result % 2 == 0, "Result (%d) is not even!" % (environ.result, )


@x_odd_y_even.when("added together")
def added(environ):
    environ.result = operator.add(environ.x, environ.y)
    return environ


@added.then("the result is odd")
def is_odd(environ):
    assert 'result' in environ, "Result missing."
    assert environ.result % 2 == 1, "Result (%d) is not odd! %r" % (environ.result, dict(environ))


if __name__ == '__main__':
    suite(workers=10, method='chain')
