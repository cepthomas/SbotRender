import sys
import os
import traceback
import unittest
from unittest.mock import MagicMock

# Set up the sublime emulation environment.
import emu_sublime_api as emu

# Import the code under test.
import sbot_common as sc
import sbot_render


#-----------------------------------------------------------------------------------
class TestRender(unittest.TestCase):  # TODOT more tests

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip('')
    def test_basic(self):
        pass