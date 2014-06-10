# drifter
# A load tester for the Phoenix-API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 10 10:12:57 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
A load tester for the Phoenix-API
"""

##########################################################################
## Imports
##########################################################################

from .conf import settings
from .runner import Runner
