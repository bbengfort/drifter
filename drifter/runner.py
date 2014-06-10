# drifter.runner
# Runs a drifter on a particular endpoint
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 10 11:20:30 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: runner.py [] benjamin@bengfort.com $

"""
Runs a drifter on a particular endpoint
"""

##########################################################################
## Imports
##########################################################################

import sys
import time

from drifter.api import Drifter
from drifter.conf import settings

##########################################################################
## Decorator
##########################################################################

def timeit(func):
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        finit  = time.time()
        delta  = finit - start
        return result, delta
    return wrapper

def sysout(msg):
    """
    Writes to sys.stdout
    """
    sys.stdout.write(msg)
    sys.stdout.flush()

##########################################################################
## Runner Module
##########################################################################

class Runner(object):
    """
    Runs a drift
    """

    def __init__(self, runs=100, **kwargs):
        self.drifter  = Drifter(**kwargs)
        self.runs     = runs

    @timeit
    def execute(self, method, *args, **kwargs):
        """
        Runs the requested method the number of times, aggregating times
        """
        times = []
        debug = kwargs.pop('debug') or settings.get('debug', False)
        wait  = kwargs.pop('wait', None)

        for idx in xrange(0, self.runs):
            start = time.time()
            data  = method(*args, **kwargs)
            finit = time.time()
            delta = finit - start
            times.append(delta * 1000)

            if debug: sysout('.')
            if wait: time.sleep(wait)

        if debug: sysout('\n')
        return times

    def categories_runner(self, **kwargs):
        """
        Runs the category endpoint for times
        """
        endpoint = self.drifter.build_endpoint('categories')
        return self.execute(self.drifter.get, endpoint, **kwargs)

if __name__ == '__main__':
    pass
