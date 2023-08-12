import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from halcyon.common.utils import read_from_env


class UtilityTestCase(TestCase):
    @patch.dict(
        os.environ, {"str_key": "fake_value", "int_key": "5", "bool_key": "True", "list_key": "0.0.0.0, localhost"}
    )
    def test_env_variable_read(self):
        assert read_from_env("str_key", str) == "fake_value"

        assert read_from_env("int_key", str) == "5"
        assert read_from_env("int_key", int) == 5

        assert read_from_env("bool_key", bool) is True
        for item in ["0.0.0.0", "localhost"]:
            self.assertIn(item, read_from_env("list_key", list))

        # Validate default value
        assert read_from_env("invalid_key", str) is None
        assert read_from_env("invalid_key", str, default_value="fake_default") == "fake_default"

        # Validate required
        with self.assertRaises(ImproperlyConfigured):
            read_from_env("invalid_key", str, required=True)
