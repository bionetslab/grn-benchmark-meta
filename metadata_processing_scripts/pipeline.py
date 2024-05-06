#!/usr/bin/env python
import pypiper
import os
import argparse
import pandas as pd
import os.path as op
import numpy as np
from codecarbon import OfflineEmissionsTracker
import re
import numpy as np

parser = argparse.ArgumentParser(description='Write a short description here')

# add any custom args here
# e.g. parser.add_argument('--foo', help='foo help')

# once you've established all your custom arguments, we can add the default
# pypiper arguments to your parser like this:
parser.add_argument('--geo', help='foo help')
parser.add_argument('--basepath', help = 'full basepath')
parser.add_argument('--fasta', help = 'fasta genome file')
parser.add_argument('--gtf', help = 'genome annotation file')
parser.add_argument('--bwa', help = 'precomputed bwa index', default=None)
parser.add_argument('-f', '--feather_ranking')      # option that takes a value
parser.add_argument('-s', '--feather_score')
parser.add_argument('-m', '--motif_annotations') # on/off flag
parser.add_argument('-t', '--tempdir', default = '/tmp/cistarget')

parser = pypiper.add_pypiper_args(parser)


args = parser.parse_args()
basename_out = op.basename(args.geo)
outfolder = basename_out.replace('.txt', '') # Choose a folder for your results

## Create tracker object and start tracking.
tracker = OfflineEmissionsTracker(country_iso_code="DEU", project_name = f'{outfolder}.cc.log', output_dir=outfolder, log_level = 'error')
tracker.start()


pm = pypiper.PipelineManager(name="my_pipeline", outfolder=outfolder,args=args)

os.makedirs(outfolder, exist_ok=True)
# Timestamps to delineate pipeline sections are easy:
pm.timestamp("Starting downloads.")
# Read pandas data frame
identifiers = pd.read_csv(args.geo, sep='\t', header = None)
print(identifiers)
identifiers.columns = ['StudyID', 'SampleName']
# 1. download the data from SRA
# 1a. add files to cleanup list
geofetch_cmd = f'geofetch -i {args.geo} -f {outfolder}'
target_file = op.join(outfolder, f'{outfolder}_SRA.csv')
pm.run(geofetch_cmd, target_file) 
print(target_file)
mapping = pd.read_csv(target_file)
mapping = mapping.loc[:, ['Run', 'SampleName', 'avgLength']].merge(identifiers)
print(mapping)
folder = args.basepath
# 2. Make fastqs.
# 2a. add files to clean up list
for r in mapping.Run:
    dumpfile = op.join(r, f'{r}.sra')
    print(dumpfile)
    fasterq_dump_cmd = f'fasterq-dump {dumpfile} -O {r}'
    pm.clean_add(dumpfile)
    ll = os.listdir(op.join(folder, r))
    fqs = [x for x in ll if 'fastq.gz' in x]
    if len(fqs)==0:
        target_file = op.join(r, f'{r}_2.fastq')
        print(target_file)
        pm.run(fasterq_dump_cmd, target_file)
    else:
        print('Files already gzipped')

# 3. Run nextflow pipeline
# 3.a. Make the sample sheet.
pm.timestamp("Starting nextflow.")

mapping['sample'] = 'Control'
tracker.flush()
print(mapping)
for i in range(mapping.shape[0]):
    r = mapping.loc[:, 'Run'][i]
    ll = os.listdir(op.join(folder, r))
    fq = re.compile(r"fastq$")
    fqs = [x for x in ll if fq.match(x)]

    for mf in fqs:
        mff = op.join(folder, r, mf)
        if f'_2.fastq' in mff:
            mapping.loc[i,'fastq_2'] = f'{mff}.gz' 
        if f'_1.fastq' in mff:
            mapping.loc[i,'fastq_1'] =  f'{mff}.gz'
        
        gzip_cmd = f'pigz {mff}'
        target_file = op.join(f'{mff}.gz')
        pm.run(gzip_cmd, target_file)   
        pm.clean_add(target_file)
        pm.clean_add(mff)

tracker.flush()
def get_read_length(rl):
    ## iGenomes precomputed readlength return the largest possible one.
    for i in [200, 150, 100, 75, 50]:
        if rl % i != rl:
            return i

print(mapping.columns)
# 3a. Be happy
rl = np.max(mapping.avgLength)/2
rl = get_read_length(rl)


# mapping['replicate'] = mapping.groupby(['sample', 'StudyID']).cumcount() +1
# mapping = mapping.loc[:, ['sample', 'fastq_1', 'fastq_2', 'replicate']]
# print(mapping)
samplesheet =op.join(outfolder, 'samplesheet.csv')
# mapping.to_csv(samplesheet, index= False)

if args.recover:
    nextflow_resume = '-resume'
    print('Resume')
else:
    nextflow_resume = ''

## If the reference is available, construct relevant param for commandline
## else save the reference.
if args.bwa is None:
    bwa_index = '--save-reference'
else:
    bwi = args.bwa
    print(bwi)
    bwa_index = f"--bwa_index {bwi}"


cmd_nextflow = f'~/Software/nextflow run nf-core/atacseq -r 2.1.2 -profile singularity --input {samplesheet} --outdir {outfolder} --read_length {rl} --fasta -with-trace --max_cpus 60 --fasta {args.fasta} --gtf {args.gtf} {nextflow_resume} {bwa_index}'

print(cmd_nextflow)
nextflow_target = op.join(outfolder, 'multiqc', 'broad_peak', 'multiqc_report.html')

pm.run(cmd_nextflow, nextflow_target)
# otherwise problematic
tracker.flush()


## Run pycistarget on all files.
file_list =  os.listdir(f'{outfolder}/bwa/merged_replicate/macs2/broad_peak')
file_list = [fn for fn in file_list if fn.endswith(".broadPeak")]

for fn in file_list:
    cmd_pycistarget = f'python grn-benchmark-meta/metadata_processing_scripts/run_pycistarget.py -b {outfolder}/bwa/merged_replicate/macs2/broad_peak/{fn} -f {args.feather_ranking} -s {args.feather_score} -m {args.motif_annotations} -o {outfolder}/pycistarget/{fn} -t /data/bionets/og86asub/spill/'
    pycistarget_target = f'{outfolder}/pycistarget/{fn}/DEM_Cistrome_Database.bed'
    pm.run(cmd_pycistarget, pycistarget_target)

tracker.flush()
pm.stop_pipeline()
tracker.stop()