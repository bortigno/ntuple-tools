# %load samples.py
import ROOT
import pandas as pd
import python.selections as selections

version = 'v80'
version_V8 = version
version_V9 = 'v81'


# -------------------------------------------------------------------------

samples_ele = [
    Sample('ele_flat2to100_PU0', 'PU0', version, 'ele'),
    Sample('ele_flat2to100_PU200', 'PU200', version, 'ele')
    ]

samples_ele_V8 = [
    Sample('ele_flat2to100_PU0', 'PU0', version_V8, 'V8'),
    Sample('ele_flat2to100_PU200', 'PU200', version_V8, 'V8')
    ]


samples_ele_V9 = [
    Sample('ele_flat2to100_PU0', 'PU0', version_V9, 'V9'),
    Sample('ele_flat2to100_PU200', 'PU200', version_V9, 'V9')
    ]

samples_photons = [
    Sample('photon_flat8to150_PU0', 'PU0', version, 'photon'),
    Sample('photon_flat8to150_PU200', 'PU200', version, 'photon')
    ]

samples_photons_V8 = [
    Sample('photon_flat8to150_PU0', 'PU0', version_V8, 'V8'),
    Sample('photon_flat8to150_PU200', 'PU200', version_V8, 'V8')
    ]

samples_photons_V9 = [
    Sample('photon_flat8to150_PU0', 'PU0', version_V9, 'V9'),
    Sample('photon_flat8to150_PU200', 'PU200', version_V9, 'V9')
    ]

samples_pions = [
    Sample('pion_flat2to100_PU0', 'PU0', version, 'pions'),
    ]

samples_nugus = [
    Sample('nugun_alleta_pu0', 'PU0', version, 'mb'),
    Sample('nugun_alleta_pu200', 'PU200', version, 'mb')
    ]

samples_nugunrates = [
    Sample('nugun_alleta_pu200', 'PU200', version, 'mb')
    ]

samples_nugunrates_V8 = [
    Sample('nugun_alleta_pu200', 'PU200', version, 'V8')
    ]

samples_nugunrates_V9 = [
    Sample('nugun_alleta_pu200', 'PU200', version, 'V9')
    ]
