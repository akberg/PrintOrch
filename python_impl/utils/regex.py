"""
Module for regex methods to read and translate file names

Created on Fri Oct 18 2019
Author: Andreas K. Berg
"""
import re


def meta(filename, composer, title):

    # Skip composer and title
    match = re.search("^" + composer)
    if match is not None:
        filename = filename[match.start:].strip(" -")
    
    match = re.search("^" + title)
    if match is not None:
        filename = filename[match.start:].strip(" -")
    
    """
    filename is now only part details
    vln 1 or
    tpt 1 (C)
    cl 1 & 2 (A, Bb)
    cl 3 (Bass)
    fl 1 + 2
    trb 3 & tuba
    """

class NameReader():
    """
    Objectoriented approach
    """

    def __init__(self):
        self.title
        self.composer