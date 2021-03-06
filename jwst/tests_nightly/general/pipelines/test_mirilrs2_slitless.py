import os
import pytest
from astropy.io import fits as pf
from jwst.pipeline.calwebb_spec2 import Spec2Pipeline

pytestmark = [
    pytest.mark.usefixtures('_jail'),
    pytest.mark.skipif(not pytest.config.getoption('bigdata'),
                       reason='requires --bigdata')
]

def test_mirilrs2pipeline1(_bigdata):
    """

    Regression test of calwebb_spec2 pipeline performed on MIRI LRS slitless data.

    """

    step = Spec2Pipeline()
    step.save_bsub=True,
    step.save_results=True
    step.resample_spec.save_results = True
    step.cube_build.save_results = True
    step.extract_1d.save_results = True
    step.run(_bigdata+'/pipelines/jw80600012001_02101_00003_mirimage_rateints.fits')

    n_cr = 'jw80600012001_02101_00003_mirimage_calints.fits'
    h = pf.open(n_cr)
    n_ref = _bigdata+'/pipelines/jw80600012001_02101_00003_mirimage_calints_ref.fits'
    href = pf.open(n_ref)
    newh = pf.HDUList([h['primary'],h['sci'],h['err'],h['dq'],h['relsens']])
    newhref = pf.HDUList([href['primary'],href['sci'],href['err'],href['dq'],href['relsens']])
    result = pf.diff.FITSDiff(newh, newhref,
                              ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX'],
                              rtol = 0.00001)
    assert result.identical, result.report()

    n_cr = 'jw80600012001_02101_00003_mirimage_x1dints.fits'
    h = pf.open(n_cr)
    n_ref = _bigdata+'/pipelines/jw80600012001_02101_00003_mirimage_x1dints_ref.fits'
    href = pf.open(n_ref)
    newh = pf.HDUList([h['primary'],h['extract1d',1],h['extract1d',2],h['extract1d',3],h['extract1d',4]])
    newhref = pf.HDUList([href['primary'],href['extract1d',1],href['extract1d',2],href['extract1d',3],href['extract1d',4]])
    result = pf.diff.FITSDiff(newh, newhref,
                              ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX'],
                              rtol = 0.00001)
    assert result.identical, result.report()
