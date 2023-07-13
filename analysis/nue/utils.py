import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

from sklearn.metrics import confusion_matrix
from mlreco.visualization.metrics import *

def make_confusion_matrix(df_plot, truth_name='Truth', pred_name='Prediction', normalize='true', ax=None):
    
    labels     = sorted(set(list(df_plot[truth_name].unique()) + list(df_plot[pred_name].unique())))
    row_labels = sorted(set(list(df_plot[truth_name].unique())))
    col_labels = sorted(set(list(df_plot[pred_name].unique())))
    
    cm = confusion_matrix(df_plot[truth_name], df_plot[pred_name], normalize=normalize, labels=labels)
    cm_counts = confusion_matrix(df_plot[truth_name], df_plot[pred_name], labels=labels)
    
    cm = cm[:, np.where(cm.sum(axis=0) > 0)[0]]
    cm_counts = cm_counts[:, np.where(cm_counts.sum(axis=0) > 0)[0]]

    cm = cm[np.where(cm.sum(axis=1) > 0)[0], :]
    cm_counts = cm_counts[np.where(cm_counts.sum(axis=1) > 0)[0], :]
    
    im = heatmap(cm * 100, 
             row_labels, 
             col_labels, 
             ax=ax, cmap="Blues")
    texts = annotate_heatmap(im, unc=cm_counts, valfmt="{:.2f}% \n ({:.0f})", fontsize=20)
    
    return im, texts, (row_labels, col_labels)


def reconstruct_nu_energy(df):
    
    df_nu_ints = []
    for key, group in df.groupby(['Index', 'true_interaction_id']):
        protons = group.query('true_particle_type == 4 and true_particle_is_primary == 1')
        electrons = group.query('true_particle_type == 1 and true_particle_semantic_type == 0 and true_particle_is_primary == 1')
        photons = group.query('true_particle_type == 0 and true_particle_is_primary == 1')

        if group['true_num_primary_electrons'].max() <= 0:
            continue

        row_dict = {
            'num_protons': int(protons.shape[0]),
            'num_electrons': int(electrons.shape[0]),
            'num_photons': int(photons.shape[0]),
            'reco_KE_protons': protons['reco_csda_kinetic_energy'].sum(),
            'true_KE_protons': protons['true_csda_kinetic_energy'].sum(),
            'true_Einit_protons': (protons['true_energy_init'] - PROTON_MASS).sum(),
            'reco_E_electrons': (electrons['reco_particle_depositions_sum'] * res_lsq.x + ELECTRON_MASS).sum(),
            'true_E_electrons': (electrons['true_particle_depositions_sum'] * res_lsq.x + ELECTRON_MASS).sum(),
            'true_Einit_electrons': electrons['true_energy_init'].sum(),
            'electron_is_contained': electrons['true_particle_is_contained'].max(),
            'true_nu_energy': group['true_nu_energy_init'].mean(),
            'true_nu_interaction_type': group['true_nu_interaction_type'].unique()[0],
            'true_topology': group['true_topology'].max()
        }
        row_dict['true_reco_E'] = row_dict['true_KE_protons'] + row_dict['true_E_electrons']
        row_dict['true_Einit_sum'] = row_dict['true_Einit_protons'] + row_dict['true_Einit_electrons']
        row_dict['reco_reco_E'] = row_dict['reco_KE_protons'] + row_dict['reco_E_electrons']

        df_nu_ints.append(row_dict)

    df_nu_ints = pd.DataFrame(df_nu_ints)
    return df_nu_ints