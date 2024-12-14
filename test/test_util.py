import pytest


def test_upper():
    assert 'foo'.upper() == 'FOO'
    
def test_isupper():
    assert 'FOO'.isupper()
    
def test_failed_upper():
    assert 'foo'.upper() == 'FOO'