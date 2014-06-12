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
import copy
import socket
import progressbar

from drifter.api import Drifter
from drifter.conf import settings
from requests.exceptions import *
from drifter.stats import TimeSeries

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

def progress():
    """
    Constructs the progressbar widget and returns a function.
    """
    widgets = [
        'Sent: ',
        progressbar.Counter(),
        ' requests (',
        progressbar.Timer(),
        ')'
    ]
    return progressbar.ProgressBar(widgets=widgets)

def wait_for_return(msg="Hit Return to continue"):
    keys = raw_input(msg)
    return True

##########################################################################
## Runner Module
##########################################################################

class Runner(object):
    """
    Runs a drift
    """

    def __init__(self, runs=100, **kwargs):
        self.runs     = runs
        self.wait     = kwargs.pop('wait', None)
        self.drifter  = Drifter(**kwargs)
        self.results  = TimeSeries()



    @timeit
    def execute(self, method, *args, **kwargs):
        """
        Runs the requested method the number of times, aggregating times
        """
        wait  = kwargs.pop('wait', self.wait)
        label = kwargs.pop('label', "run #%i" % (len(self.results) + 1))
        pbar  = progress()

        for idx in pbar(xrange(0, self.runs)):
            start = time.time()

            try:
                data  = method(*args, **kwargs)
            except (Timeout, socket.timeout):
                self.results.append(label, -1)
                continue

            finit = time.time()
            delta = finit - start
            self.results.append(label, delta * 1000)

            if wait: time.sleep(wait)

        return self.results[label]

    def get_runner(self, endpoint, default=None):
        """
        Returns the runner function for the specified endpoint.
        """
        action = "%s_runner" % endpoint
        if hasattr(self, action):
            action = getattr(self, action)
            if callable(action):
                return action
        return default

    def categories_runner(self, label="GET /categories", **kwargs):
        """
        Runs the category endpoint for times
        """
        endpoint = self.drifter.build_endpoint('categories')
        return self.execute(self.drifter.get, endpoint, label=label, **kwargs)

    def brands_runner(self, label="GET /merchants", **kwargs):
        """
        Runs the brands endpoint for times
        """
        endpoint = self.drifter.build_endpoint('merchants')
        return self.execute(self.drifter.get, endpoint, label=label, **kwargs)

    def sizes_runner(self, label="GET /sizes", **kwargs):
        """
        Runs the sizes endpoint for times
        """
        endpoint = self.drifter.build_endpoint('sizes')
        return self.execute(self.drifter.get, endpoint, label=label, **kwargs)

    def run(self, endpoints, labels=None, prompt=False, **kwargs):
        """
        Runs a set of endpoints in a complete fashion.
        """
        times = []
        for idx, endpoint in enumerate(endpoints):
            if prompt and idx > 0:
                wait_for_return()

            action = self.get_runner(endpoint)
            if action is None:
                raise Exception("Could not find runner for endpoint '%s'" % endpoint)

            if labels:
                _, time = action(label=labels[idx], **kwargs)
            else:
                _, time = action(**kwargs)
            times.append(time)

        return times

    def display(self, title=None, **kwargs):
        """
        Graphs the results of the runner
        """
        title = title or "Drifter with %i Runs" % len(self.results)
        self.results.display(title=title, **kwargs)

    def statistics(self):
        """
        Computes various statistics for the runner results
        """
        return self.results.statistics()

    def dump(self, stream, **kwargs):
        """
        Dumps the results to JSON
        """
        self.results.dump(stream, **kwargs)

if __name__ == '__main__':
    pass
