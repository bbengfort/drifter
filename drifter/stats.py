# drifter.stats
# A statistics package for drifter results
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 12 10:40:10 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: stats.py [] benjamin@bengfort.com $

"""
A statistics package for drifter results.
"""

##########################################################################
## Imports
##########################################################################

import json
import numpy as np

from collections import defaultdict
from drifter.chart import chart_times

##########################################################################
## Time Series
##########################################################################

class TimeSeries(object):
    """
    An object that holds a dictionary of various time series for display.
    """

    @classmethod
    def load(klass, stream):
        """
        Load a stats object from a JSON data file on disk
        """
        instance = klass()
        data     = json.load(stream)
        for label, series in data.items():
            instance.extend(label, series)
        return instance

    def __init__(self):
        self.data = defaultdict(list)

    def __getitem__(self, series):
        return np.array(self.data[series])

    def __setitem__(self, series, val):
        self.data[series] = val

    def __contains__(self, series):
        return series in self.data

    def __iter__(self):
        for item in self.data:
            yield item

    def __len__(self):
        return len(self.data)

    def items(self):
        """
        Iterate through series, values pairs of data
        """
        for item in self.data.items():
            yield item

    def get(self, series, default=None):
        """
        Get a timeseries if exists, else default
        """
        return self.data.get(series, default)

    def pop(self, series, default=None):
        """
        Pop a timeseries if exists, else default
        """
        return self.data.pop(series, default)

    def append(self, series, value):
        """
        Append a value to a particular timeseries
        """
        self.data[series].append(value)

    def extend(self, series, values):
        """
        Extend a particular timeseries with values
        """
        self.data[series].extend(values)

    def mean(self, series):
        """
        Returns the mean value for a particular series
        """
        return np.mean(self[series])

    def median(self, series):
        """
        Returns the median value for a particular series
        """
        return np.median(self[series])

    def stddev(self, series):
        """
        Returns the standard deviation of a particular series
        """
        return np.std(self[series])

    def variance(self, series):
        """
        Returns the variance of a particular series
        """
        return np.var(self[series])

    def max(self, series):
        """
        Returns the maximum value of a particular series
        """
        return np.amax(self[series])

    def min(self, series):
        """
        Returns the lowest value of a particular series
        """
        return np.amin(self[series])

    def statistics(self):
        """
        Returns all statistics for the various series
        """
        stats = {}
        for label, times in self.items():
            stats[label] = {
                'mean': np.mean(times),
                'median': np.median(times),
                'stddev': np.std(times),
                'variance': np.var(times),
                'max': np.amax(times),
                'min': np.amin(times)
            }
        return stats

    def pprint(self, title=None):
        """
        Pretty prints the statistics for the timeseries
        """
        output = []
        for label, stats in self.statistics().items():
            output.append("Statistics for the %s series:" % label)
            for stat, val in stats.items():
                output.append("    %s: %0.3f" % (stat.title(), val))
        return "\n".join(output)

    def display(self, title=None, **kwargs):
        """
        Creates line plots of the data using matplotlib
        """
        title = title or "Statistics for %i series" % len(self)
        chart_times(self, title=title, **kwargs)

    def dump(self, stream, **kwargs):
        """
        Dump the data to a JSON file
        """
        json.dump(self.data, stream, **kwargs)

