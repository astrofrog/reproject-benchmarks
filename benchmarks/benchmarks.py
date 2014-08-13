# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os

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

        self.header_in = fits.Header.fromtextfile(os.path.join(ROOT, 'data/gc_ga.hdr'))
        self.header_out = fits.Header.fromtextfile(os.path.join(ROOT, 'data/gc_eq.hdr'))

        self.header_out_size = self.header_out.copy()
        self.header_out_size['NAXIS'] = 2
        self.header_out_size['NAXIS1'] = 600
        self.header_out_size['NAXIS2'] = 550

        self.array_in = np.ones((700, 690))

        self.hdu_in = fits.ImageHDU(self.array_in, self.header_in)

        self.wcs_in = WCS(self.header_in)
        self.wcs_out = WCS(self.header_out)
        self.shape_out = (600, 550)

    def time_bilinear(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='bilinear')

    def time_flux_conserving(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='flux-conserving')

    def mem_bilinear(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='bilinear')

    def mem_flux_conserving(self):
        reproject(self.hdu_in, self.header_out_size, projection_type='flux-conserving')
