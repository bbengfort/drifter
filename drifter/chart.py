# drifter.chart
# Does matplotlib charting for the Drifter module
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: chart.py [] benjamin@bengfort.com $

"""
Does matplotlib charting for the Drifter module
"""

##########################################################################
## Imports
##########################################################################

import numpy as np
import matplotlib.pyplot as plt

##########################################################################
## Helper functions
##########################################################################

def chart_times(runs, title=None, saveto=None, units='milliseconds'):
    """
    Creates a simple line chart of times (expected is milliseconds) - pass
    in a dictionary of multiple runs where the key is the label and the
    value is the times in the units specified.
    """
    if not hasattr(runs, 'items') and not callable(runs.items):
        raise TypeError("Cannot chart a non-dictionary")

    # Graph configuration
    fig, axe = plt.subplots(figsize=(9,7))
    if title:
        axe.set_title(title)
    plt.ylabel(units)
    plt.xlabel('run index')

    # Plotting each run
    for label, times in runs.items():
        axe.plot(times, '-o', label=label)

    # Add the legend
    axe.legend()

    if saveto:
        plt.savefig(saveto)
    else:
        plt.show()
