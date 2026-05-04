"""UI Login tests — bind BDD scenarios."""
import pytest
from pytest_bdd import scenarios

scenarios("../../features/login.feature")
