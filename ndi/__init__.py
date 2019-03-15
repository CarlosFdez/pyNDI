"""
Mini library used to read video data from an NDI source
"""

from .lib import lib, ffi

from .finder import create_ndi_finder
from .receiver import create_receiver

# for typings
from .finder import NDIFinder, NDISource


