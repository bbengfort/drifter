# tests.api_tests
# Tests for the API module
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 10 10:51:26 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: api_tests.py [] benjamin@bengfort.com $

"""
Tests for the API module
"""

##########################################################################
## Imports
##########################################################################

import drifter
import unittest

from drifter.api import *

##########################################################################
## Test case
##########################################################################

class DrifterTestCase(unittest.TestCase):

    def test_init_from_settings(self):
        """
        Assert that settings are included on drifter init
        """
        drifter = Drifter()
        self.assertEqual(drifter.api_root, settings['api_root'])
        self.assertEqual(drifter.api_key, settings['api_key'])

    def test_init_override(self):
        """
        Assert that settings can be overrode in drifter
        """
        drifter = Drifter('http://www.google.com', 'bob')
        self.assertEqual(drifter.api_root, 'http://www.google.com')
        self.assertEqual(drifter.api_key, 'bob')

    def test_endpoint_construction(self):
        """
        Test the drifter endpoint construction
        """
        drifter = Drifter()
        self.assertEqual('https://local.api.cobrain.com/sizes', drifter.build_endpoint('sizes'))
        self.assertEqual('https://local.api.cobrain.com/catalogs/43', drifter.build_endpoint('catalogs', '43'))
        self.assertEqual('https://local.api.cobrain.com/catalogs/43/products', drifter.build_endpoint('catalogs', '43', 'products'))
        self.assertEqual('https://local.api.cobrain.com/catalogs/43/products', drifter.build_endpoint('catalogs/43/products'))
