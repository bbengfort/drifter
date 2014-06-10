# tests
# Testing for the drifter module
#
# Author:   Benjamin Bengfort <ben@cobrain.com>
# Created:  Tue Jun 10 10:08:35 2014 -0400
#
# Copyright (C) 2013 Cobrain Company
# For license information, see LICENSE.txt
#
# ID: __init__.py [] ben@cobrain.com $

"""
Testing for the drifter module
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Test Cases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Tests a simple world fact by asserting that 10*10 is 100.
        """
        self.assertEqual(10*10, 100)

    def test_import(self):
        """
        Can import drifter
        """
        try:
            import drifter
        except ImportError:
            self.fail("Unable to import the drifter module!")
