#!/usr/bin/env python
# coding: utf-8

# In[127]:


import pycistarget
# Load cistarget functions
from pycistarget.motif_enrichment_cistarget import *
import pyranges as pr
import os
import argparse

from pycistarget.motif_enrichment_dem import *
from pycistarget.utils import *
import os.path as op


# In[ ]:


parser = argparse.ArgumentParser(
                    prog='Call cistarget',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('-b', '--bedfile')           # positional argument
parser.add_argument('-f', '--feather_ranking')      # option that takes a value
parser.add_argument('-s', '--feather_score')
parser.add_argument('-m', '--motif_annotations') # on/off flag
parser.add_argument('-t', '--tempdir', default = '/tmp/cistarget')
parser.add_argument('-o', '--outdir')
args = parser.parse_args()


os.makedirs(args.outdir, exist_ok=True)
# In[2]:


# read bedfiles. Change numeric chromosomes to chrN style notation
region_sets =pr.read_bed(args.bedfile)
region_sets = region_sets[region_sets.Chromosome.isin([str(i) for i in range(1, 23)])]
region_sets.Chromosome = ['chr'+(i) for i in region_sets.Chromosome ]


# In[5]:


# Run, using precomputed database
cistarget_dict = run_cistarget(ctx_db = args.feather_ranking,
                              region_sets = region_sets,
                              specie = 'homo_sapiens',
                              auc_threshold = 0.005,
                              nes_threshold = 3.0,
                              rank_threshold = 0.05,
                              annotation = ['Direct_annot', 'Orthology_annot'],
                              annotation_version = 'v10nr_clust',
                              path_to_motif_annotations = args.motif_annotations,
                              n_cpu = 4,
                              _temp_dir=args.tempdir)



# In[129]:


# Export all results as bed files.
def get_all_results_as_bed(cistarget_dict, database='Region_set', mode = 'Cistrome'):
    '''
    Get all cistroms from the results.
    database in ['Region_set', 'Database'] like Cistarget, the Region set
    is the input region and Database is the same hit but in the external database
    '''
    for c in cistarget_dict.keys():
        if mode == 'Cistrome':
            cistrome_names = cistarget_dict[c].cistromes[database]
        elif mode == 'Motif':
            cistrome_names = cistarget_dict[c].motif_hits[database]
        list_of_ranges = []
        for k in cistrome_names:
            #print(k)
            if mode == 'Cistrome':
                cebpa_cistrome = cistarget_dict[c].cistromes[database][k]
            elif mode == 'Motif':
                cebpa_cistrome = cistarget_dict[c].motif_hits[database][k]
            cebpa_cistrome = pr.PyRanges(region_names_to_coordinates(cebpa_cistrome))
            s = pd.Series(data = [k]*len(cebpa_cistrome), name="Name")
            cebpa_cistrome = cebpa_cistrome.insert(s)
            list_of_ranges.append(cebpa_cistrome)
    list_of_ranges = pr.concat(list_of_ranges)
    return list_of_ranges


# In[128]:


# Run the export function on all possible combinations
for db in ['Region_set', 'Database']:
    for m in ['Motif', 'Cistrome']:
        res = get_all_results_as_bed(cistarget_dict, database=db, mode = m)
        res.to_bed(op.join(args.outdir, f'{m}_{db}.bed'))


# In[15]:


# identify differentially enriched motifs (DEMs)
DEM_dict = DEM(dem_db = args.feather_score,
    region_sets = region_sets,
    specie = 'homo_sapiens',
    contrasts = 'Other',
    name = 'DEM',
    fraction_overlap = 0.4,
    max_bg_regions = 500,
    adjpval_thr = 0.05,
    log2fc_thr = 1,
    mean_fg_thr = 0,
    motif_hit_thr = None,
    cluster_buster_path = None,
    path_to_genome_fasta = None,
    path_to_motifs = None,
    annotation_version = 'v10nr_clust',
    path_to_motif_annotations = args.motif_annotations,
    motif_annotation = ['Direct_annot', 'Orthology_annot'],
    n_cpu = 4,
    tmp_dir = args.tempdir,
    _temp_dir=args.tempdir)



# In[171]:


# Save all to bed. 
def get_all_dem_motifs_as_bed_dem(cistarget_dict, database='Region_set', mode = 'Cistrome'):
    '''
    Get all cistroms from the results.
    database in ['Region_set', 'Database'] like Cistarget, the Region set
    is the input region and Database is the same hit but in the external database
    '''

    cistrome_names = cistarget_dict.motif_hits[database].keys()
    list_of_ranges = []
    for k in cistrome_names: # Chromosome
        #print(k)
        for m in cistarget_dict.motif_hits[database][k].keys():
            cebpa_cistrome = cistarget_dict.motif_hits[database][k][m]
            cebpa_cistrome = pr.PyRanges(region_names_to_coordinates(cebpa_cistrome))
            s = pd.Series(data = [k]*len(cebpa_cistrome), name="Name")
            cebpa_cistrome = cebpa_cistrome.insert(s)
            list_of_ranges.append(cebpa_cistrome)
    list_of_ranges = pr.concat(list_of_ranges)
    return list_of_ranges

from pycistarget.utils import *
def get_all_dem_cistromes_as_bed_dem(cistarget_dict, database='Region_set'):
    '''
    Get all cistroms from the results.
    database in ['Region_set', 'Database'] like Cistarget, the Region set
    is the input region and Database is the same hit but in the external database
    '''
    cistrome_names = cistarget_dict.cistromes[database].keys()
    
    list_of_ranges = []
    for k in cistrome_names: # Chromosome
        #print(k)
        for m in cistarget_dict.cistromes[database][k].keys():
            cebpa_cistrome = cistarget_dict.cistromes[database][k][m]
            cebpa_cistrome = pr.PyRanges(region_names_to_coordinates(cebpa_cistrome))
            s = pd.Series(data = [k]*len(cebpa_cistrome), name="Name")
            cebpa_cistrome = cebpa_cistrome.insert(s)
            list_of_ranges.append(cebpa_cistrome)
    list_of_ranges = pr.concat(list_of_ranges)
    return list_of_ranges


# In[172]:


for db in ['Region_set', 'Database']:
    res = get_all_dem_motifs_as_bed_dem(DEM_dict, database=db)
    res.to_bed(op.join(args.outdir, f'DEM_Motif_{db}.bed'))


# In[173]:


for db in ['Region_set', 'Database']:
    res = get_all_dem_cistromes_as_bed_dem(DEM_dict, database=db)
    res.to_bed(op.join(args.outdir, f'DEM_Cistrome_{db}.bed'))

