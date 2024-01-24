
require(data.table)


data<-fread('/home/bionets-og86asub/Documents/netmap/grn-benchmark/grn-benchmark-meta/data/metadata/GEO_accessions/GEO_accessions_PEP/GEO_accessions_PEP_raw.csv')
tissue_types<-unique(data[, .(sample_series_id, sample_source_name_ch1)])
fwrite(tissue_types, file ='/home/bionets-og86asub/Documents/netmap/grn-benchmark/grn-benchmark-meta/data/metadata/GEO_tissue.tsv', sep = '\t')

