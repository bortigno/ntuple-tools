# %load settings.py
# from samples import get_label_dict
import python.selections as selections
import python.collections as collections

import pprint



def get_label_dict(selections):
    dictionary = {}
    for sel in selections:
        dictionary[sel.name] = sel.label
    return dictionary



# === samples =====================================================
samples = []

samples = samples_ele_V8
samples += samples_ele_V9


sample = 'V9'

do_rate = True

# === TP ==========================================================
# tps = ['EG', 'TkEG', 'TkEle', 'TkIsoEle']
tps = ['DEF', 'HMvDR', 'HMvDRRebin', 'HMvDRsTC', 'HMvDRTrue']

# === TP selections ================================================
tp_select = {}
tp_select['DEF'] = ['Em', 'all']
tp_select['DEFNC'] = tp_select['DEF']
tp_select['HMvDR'] = tp_select['DEF']
tp_select['HMvDRNC0'] = tp_select['DEF']
tp_select['HMvDRNC1'] = tp_select['DEF']
tp_select['HMvDRRebin'] = tp_select['DEF']
tp_select['HMvDRsTC'] = tp_select['DEF']
tp_select['HMvDRTrue'] = tp_select['DEF']


tp_select['EG'] = ['EGq2', 'EGq3']

tp_select['TkEG'] = get_label_dict(selections.tkeg_qual_selections).keys()
tp_select['TkEle'] = ['EGq2', 'EGq3']

tp_select['TkEle'] = ['EGq2', 'EGq3', 'EGq2Iso0p2', 'EGq3Iso0p2', 'EGq2Iso0p3', 'EGq3Iso0p3']
tp_select['TkIsoEle'] = ['EGq2', 'EGq3', 'EGq2Iso0p2', 'EGq3Iso0p2', 'EGq2Iso0p3', 'EGq3Iso0p3']
tp_select['L1Trk'] = ['all', 'Pt2', 'Pt10']

# ==== GEN selections ===============================================

gen_select = ['GENEtaBC', 'GENEtaD']
# gen_select = ['GEN', 'GENEtaA', 'GENEtaB', 'GENEtaC', 'GENEtaD', 'GENEtaE',
#               'GENEtaAB', 'GENEtaABC', 'GENEtaBC', 'GENEtaBCD', 'GENEtaBCDE' ]

# tp_select['TkEG'] = ['EGq2EtaBC', 'EGq3EtaBC', 'EGq2EtaBCM2', 'EGq3EtaBCM2', 'EGq2EtaBCM2s', 'EGq3EtaBCM2s','EGq2EtaBCM3', 'EGq3EtaBCM3', 'EGq2EtaBCM3s', 'EGq3EtaBCM3s','EGq2EtaBCM4', 'EGq3EtaBCM4']



event_manager = collections.EventManager()

all_tpsets = {}
for collection in event_manager.collections:
    all_tpsets[collection.name] = collection.label


# all_tpsets = {'DEF': 'dRC3d',
#               'DEFCalib': 'NNDR Calib v1',
#               'DEFNC': 'dRC3d + new Th',
#               'HMvDR': 'HistoMaxC3d + dR(layer)',
#               'HMvDRNC0': 'HMC3d+dR(layer)+NC0',
#               'HMvDRNC1': 'HMC3d+dR(layer)+NC1',
#               'EG': 'EG',
#               'TkEG': 'TkEG',
#               'TkEle': 'TkEle',
#               'TkIsoEle': 'TkIsoEle',
#               'L1Trk': 'L1Track'}


# ==== adapt the plot retrieval
tpsets = {}
tpset_selections = {}
gen_selections = {}

for tp in tps:
    tpsets[tp] = all_tpsets[tp]

if 'DEF' in tps or 'HMvDR' in tps:
    if do_rate:
        tpset_selections.update(get_label_dict(selections.tp_rate_selections))
    else:
        tpset_selections.update(get_label_dict(selections.tp_match_selections))
if 'EG' in tps:
    if do_rate:
        tpset_selections.update(get_label_dict(selections.eg_rate_selections))
    else:
        tpset_selections.update(get_label_dict(selections.eg_pt_selections))
if 'TkEG' in tps:
    if do_rate:
        tpset_selections.update(get_label_dict(selections.tkeg_rate_selections))
    else:
        tpset_selections.update(get_label_dict(selections.tkeg_pt_selections))
if 'TkEle' in tps or 'TkIsoEle' in tps:
    if do_rate:
        tpset_selections.update(get_label_dict(selections.tkisoeg_rate_selections))
    else:
        tpset_selections.update(get_label_dict(selections.tkisoeg_pt_selections))
if 'L1Trk' in tps:
    tpset_selections.update(get_label_dict(selections.tracks_selections))


gen_selections.update(get_label_dict(selections.gen_part_selections))
gen_selections.update({'nomatch': ''})


pp = pprint.PrettyPrinter(indent=4)
print '--- TPs: '
pp.pprint(tps)
print '--- TP selections:'
pp.pprint(tp_select)
print '--- GEN selections:'
print gen_select
