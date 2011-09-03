# encoding: utf-8

"""Running this example should produce:

Tests starting.

Feature: Mathematics.
    Scenario: Basic operations.
        Given: A number, x, that is odd.
          And: A number, y, that is even.
            When: Multiplied together.
                Then: The result is even.
            When: Added together.
                Then: The result is odd.

Finished.

If something went wrong (for example, a magical division by zero when testing
the multiplication result ;) you would see the following:

Tests starting.

Feature: Mathematics.
    Scenario: Basic operations.
        Given: A number, x, that is odd.
          And: A number, y, that is even.
            When: Multiplied together.
                Then: The result is even.
                      Traceback (most recent call last):
                        File "/Users/amcgregor/Projects/Marrow/src/marrow.testing/marrow/testing/__init__.py", line 51, in fast
                          environ = self(environ)
                        File "/Users/amcgregor/Projects/Marrow/src/marrow.testing/marrow/testing/__init__.py", line 41, in __call__
                          result = self.fn(environ)
                        File "/Users/amcgregor/Projects/Marrow/src/marrow.testing/examples/simple.py", line 72, in is_even
                          1/0
                      ZeroDivisionError: integer division or modulo by zero
            When: Added together.
                Then: The result is odd.

Finished.
"""

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
    suite(workers=10, method='fast')
