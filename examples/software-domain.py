# encoding: utf-8

"""Programmer-domain Behaviour Driven Development example.

From: http://en.wikipedia.org/wiki/Behavior_Driven_Development#Programmer-domain_examples_and_behavior

Sample output: (can you fix the bug?)

Feature: Lists behave in predictable ways.
    Scenario: Lists should know when they are empty.
        Given: A new list.
            When: Nothing is added.
                Then: The list should be empty.
            When: We add an object.
                Then: The list should not be empty.
                      Traceback (most recent call last):
                        File ".../marrow.testing/marrow/testing/__init__.py", line 51, in fast
                          environ = self(environ)
                        File ".../marrow.testing/marrow/testing/__init__.py", line 41, in __call__
                          result = self.fn(environ)
                        File ".../software-domain.py", line 52, in list_not_empty
                          assert len(environ.l) != 0, "List is empty!"
                      AssertionError: List is empty!

"""


from __future__ import unicode_literals, print_function

import operator

from marrow.testing import Suite


suite = Suite()


@suite.feature("lists behave in predictable ways")
def lists(environ):
    pass


@lists.scenario("lists should know when they are empty")
def test_empty(environ):
    pass


@test_empty.given("a new list")
def create_list(environ):
    environ.l = []
    return environ


@create_list.when("nothing is added")
def add_nothing(environ):
    pass


@create_list.when("we add an object")
def add_object(environ):
    pass


@add_nothing.then("the list should be empty")
def list_not_empty(environ):
    assert len(environ.l) == 0, "List is not empty!"


@add_object.then("the list should not be empty")
def list_not_empty(environ):
    assert len(environ.l) != 0, "List is empty!"


if __name__ == '__main__':
    suite(workers=10, method='fast')
