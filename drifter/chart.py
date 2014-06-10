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

def chart_times(times, title=None, saveto=None):
    """
    Creates a simple line chart of times
    """
    fig, axe = plt.subplots(figsize=(9,7))
    axe.plot(times, '-ro')

    if title:
        axe.set_title(title)
    plt.ylabel('milliseconds')
    plt.xlabel('run index')

    if saveto:
        plt.savefig(saveto)
    else:
        plt.show()
