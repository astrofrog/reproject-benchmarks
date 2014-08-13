# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os
import warnings

import numpy as np

from astropy.wcs import WCS
from astropy.io import fits

from reproject import reproject

ROOT = os.path.abspath(os.path.dirname(__file__))

class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """

    def setup(self):

        warnings.simplefilter('ignore')

        self.header_in = fits.Header.fromtextfile(os.path.join(ROOT, 'data/gc_ga.hdr'))
        self.header_out = fits.Header.fromtextfile(os.path.join(ROOT, 'data/gc_eq.hdr'))

        self.header_out_size = self.header_out.copy()
        self.header_out_size['NAXIS'] = 2
        self.header_out_size['NAXIS1'] = 300
        self.header_out_size['NAXIS2'] = 250

        self.array_in = np.ones((210, 215))

        self.hdu_in = fits.ImageHDU(self.array_in, self.header_in)

        self.wcs_in = WCS(self.header_in)
        self.wcs_out = WCS(self.header_out)
        self.shape_out = (300, 250)

    def time_bilinear(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='bilinear')

    def time_flux_conserving(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='flux-conserving')
