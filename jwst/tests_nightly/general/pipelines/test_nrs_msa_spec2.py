import os
import shutil
import pytest
from astropy.io import fits as pf
from jwst.pipeline.calwebb_spec2 import Spec2Pipeline

pytestmark = [
    pytest.mark.usefixtures('_jail'),
    pytest.mark.skipif(not pytest.config.getoption('bigdata'),
                       reason='requires --bigdata')
]

def test_nrs_msa_spec2(_bigdata):
    """

    Regression test of calwebb_spec2 pipeline performed on NIRSpec MSA data.

    """
    curdir = os.path.abspath(os.curdir)
    # copy over input-specific reference files, such as MSA Metadata file
    msafile = os.path.join(_bigdata, 'pipelines',
                           'jw95065006001_0_short_msa.fits')
    shutil.copy(msafile, curdir)

    # define primary output name
    na = 'F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1_mod_cal.fits'
    nin = 'F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1_mod.fits'

    # define step for use in test
    step = Spec2Pipeline()
    step.output_file = na
    step.save_bsub = False
    step.output_use_model = True
    step.resample_spec.save_results = True
    step.resample_spec.skip = True
    step.extract_1d.save_results = True
    step.extract_1d.smoothing_length = 0
    step.extract_1d.bkg_order = 0
    step.run(os.path.join(_bigdata,'pipelines',nin))

    nbname = 'f170lp-g235m_mos_observation-6-c0e0_001_dn_nrs1_mod_cal_ref.fits'
    nb = os.path.join(_bigdata,'pipelines', nbname)
                      
    h = pf.open(na)
    href = pf.open(nb)
    newh = pf.HDUList([h['primary'],h['sci',1],h['err',1],h['dq',1],h['relsens',1],h['wavelength',1],
                                    h['pathloss_pointsource',1],h['wavelength_pointsource',1],
                                    h['pathloss_uniformsource',1],h['wavelength_uniformsource',1],
                                    h['barshadow',1],
                                    h['sci',2],h['err',2],h['dq',2],h['relsens',2],h['wavelength',2],
                                    h['pathloss_pointsource',2],h['wavelength_pointsource',2],
                                    h['pathloss_uniformsource',2],h['wavelength_uniformsource',2],
                                    h['barshadow',2],
                                    h['sci',3],h['err',3],h['dq',3],h['relsens',3],h['wavelength',3],
                                    h['pathloss_pointsource',3],h['wavelength_pointsource',3],
                                    h['pathloss_uniformsource',3],h['wavelength_uniformsource',3],
                                    h['barshadow',3],
                                    h['sci',4],h['err',4],h['dq',4],h['relsens',4],h['wavelength',4],
                                    h['pathloss_pointsource',4],h['wavelength_pointsource',4],
                                    h['pathloss_uniformsource',4],h['wavelength_uniformsource',4],
                                    h['barshadow',4],
                                    h['sci',5],h['err',5],h['dq',5],h['relsens',5],h['wavelength',5],
                                    h['pathloss_pointsource',5],h['wavelength_pointsource',5],
                                    h['pathloss_uniformsource',5],h['wavelength_uniformsource',5],
                                    h['barshadow',5],
                                    h['sci',6],h['err',6],h['dq',6],h['relsens',6],h['wavelength',6],
                                    h['pathloss_pointsource',6],h['wavelength_pointsource',6],
                                    h['pathloss_uniformsource',6],h['wavelength_uniformsource',6],
                                    h['barshadow',6],
                                    h['sci',7],h['err',7],h['dq',7],h['relsens',7],h['wavelength',7],
                                    h['pathloss_pointsource',7],h['wavelength_pointsource',7],
                                    h['pathloss_uniformsource',7],h['wavelength_uniformsource',7],
                                    h['barshadow',7],
                                    h['sci',8],h['err',8],h['dq',8],h['relsens',8],h['wavelength',8],
                                    h['pathloss_pointsource',8],h['wavelength_pointsource',8],
                                    h['pathloss_uniformsource',8],h['wavelength_uniformsource',8],
                                    h['barshadow',8],
                                    h['sci',9],h['err',9],h['dq',9],h['relsens',9],h['wavelength',9],
                                    h['pathloss_pointsource',9],h['wavelength_pointsource',9],
                                    h['pathloss_uniformsource',9],h['wavelength_uniformsource',9],
                                    h['barshadow',9],
                                    h['sci',10],h['err',10],h['dq',10],h['relsens',10],h['wavelength',10],
                                    h['pathloss_pointsource',10],h['wavelength_pointsource',10],
                                    h['pathloss_uniformsource',10],h['wavelength_uniformsource',10],
                                    h['barshadow',10]])
    newhref = pf.HDUList([href['primary'],href['sci',1],href['err',1],href['dq',1],href['relsens',1],href['wavelength',1],
                                          href['pathloss_pointsource',1],href['wavelength_pointsource',1],
                                          href['pathloss_uniformsource',1],href['wavelength_uniformsource',1],
                                          href['barshadow',1],
                                          href['sci',2],href['err',2],href['dq',2],href['relsens',2],href['wavelength',2],
                                          href['pathloss_pointsource',2],href['wavelength_pointsource',2],
                                          href['pathloss_uniformsource',2],href['wavelength_uniformsource',2],
                                          href['barshadow',2],
                                          href['sci',3],href['err',3],href['dq',3],href['relsens',3],href['wavelength',3],
                                          href['pathloss_pointsource',3],href['wavelength_pointsource',3],
                                          href['pathloss_uniformsource',3],href['wavelength_uniformsource',3],
                                          href['barshadow',3],
                                          href['sci',4],href['err',4],href['dq',4],href['relsens',4],href['wavelength',4],
                                          href['pathloss_pointsource',4],href['wavelength_pointsource',4],
                                          href['pathloss_uniformsource',4],href['wavelength_uniformsource',4],
                                          href['barshadow',4],
                                          href['sci',5],href['err',5],href['dq',5],href['relsens',5],href['wavelength',5],
                                          href['pathloss_pointsource',5],href['wavelength_pointsource',5],
                                          href['pathloss_uniformsource',5],href['wavelength_uniformsource',5],
                                          href['barshadow',5],
                                          href['sci',6],href['err',6],href['dq',6],href['relsens',6],href['wavelength',6],
                                          href['pathloss_pointsource',6],href['wavelength_pointsource',6],
                                          href['pathloss_uniformsource',6],href['wavelength_uniformsource',6],
                                          href['barshadow',6],
                                          href['sci',7],href['err',7],href['dq',7],href['relsens',7],href['wavelength',7],
                                          href['pathloss_pointsource',7],href['wavelength_pointsource',7],
                                          href['pathloss_uniformsource',7],href['wavelength_uniformsource',7],
                                          href['barshadow',7],
                                          href['sci',8],href['err',8],href['dq',8],href['relsens',8],href['wavelength',8],
                                          href['pathloss_pointsource',8],href['wavelength_pointsource',8],
                                          href['pathloss_uniformsource',8],href['wavelength_uniformsource',8],
                                          href['barshadow',8],
                                          href['sci',9],href['err',9],href['dq',9],href['relsens',9],href['wavelength',9],
                                          href['pathloss_pointsource',9],href['wavelength_pointsource',9],
                                          href['pathloss_uniformsource',9],href['wavelength_uniformsource',9],
                                          href['barshadow',9],
                                          href['sci',10],href['err',10],href['dq',10],href['relsens',10],href['wavelength',10],
                                          href['pathloss_pointsource',10],href['wavelength_pointsource',10],
                                          href['pathloss_uniformsource',10],href['wavelength_uniformsource',10],
                                          href['barshadow',10]])
    result = pf.diff.FITSDiff(newh, newhref,
                              ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX'],
                              rtol = 0.00001)


    assert result.identical, result.report()

    #na = 'f170lp-g235m_mos_observation-6-c0e0_001_dn_nrs1_mod_s2d.fits'
    #nb = _bigdata+'/pipelines/F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1_s2d_ref.fits'
    #h = pf.open(na)
    #href = pf.open(nb)
    #newh = pf.HDUList([h['primary'],h['sci',1],h['wht',1],h['con',1],h['relsens',1],
    #                                h['sci',2],h['wht',2],h['con',2],h['relsens',2],
    #                                h['sci',3],h['wht',3],h['con',3],h['relsens',3],
    #                                h['sci',4],h['wht',4],h['con',4],h['relsens',4],
    #                                h['sci',5],h['wht',5],h['con',5],h['relsens',5]])
    #newhref = pf.HDUList([href['primary'],href['sci',1],href['wht',1],href['con',1],href['relsens',1],
    #                                      href['sci',2],href['wht',2],href['con',2],href['relsens',2],
    #                                      href['sci',3],href['wht',3],href['con',3],href['relsens',3],
    #                                      href['sci',4],href['wht',4],href['con',4],href['relsens',4],
    #                                      href['sci',5],href['wht',5],href['con',5],href['relsens',5]])
    #result = pf.diff.FITSDiff(newh, newhref,
    #                          ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX'],
    #                          rtol = 0.00001)
    #assert result.identical, result.report()

    na = 'F170LP-G235M_MOS_observation-6-c0e0_001_DN_NRS1_mod_x1d.fits'
    nbname = 'f170lp-g235m_mos_observation-6-c0e0_001_dn_nrs1_mod_x1d_ref.fits'
    nb = os.path.join(_bigdata, 'pipelines', nbname)
    h = pf.open(na)
    href = pf.open(nb)
    newh = pf.HDUList([h['primary'],h['extract1d',1],h['extract1d',2],h['extract1d',3],h['extract1d',4],h['extract1d',5],h['extract1d',6],h['extract1d',7],h['extract1d',8],h['extract1d',9],h['extract1d',10]])
    newhref = pf.HDUList([href['primary'],href['extract1d',1],href['extract1d',2],href['extract1d',3],href['extract1d',4],href['extract1d',5],href['extract1d',6],href['extract1d',7],href['extract1d',8],href['extract1d',9],href['extract1d',10]])
    result = pf.diff.FITSDiff(newh, newhref,
                              ignore_keywords = ['DATE','CAL_VER','CAL_VCS','CRDS_VER','CRDS_CTX'],
                              rtol = 0.00001)

    assert result.identical, result.report()
