from pinnacle import pinnacle
import pytest
import pathlib
import os
PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

def test_gen_dir_name():
    import secrets
    import string
    ALPHABET = string.ascii_letters + string.digits
    new_dir = ''.join(secrets.choice(ALPHABET) for i in range(10))
    return new_dir

def test_tst1():
    assert (1+1)==2
