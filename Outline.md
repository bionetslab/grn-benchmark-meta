# 1 How to conduct a systematic benchmark
## 1.1 References

Mangul, S., Martin, L.S., Hill, B.L. _et al._ Systematic benchmarking of omics computational tools. _Nat Commun_ **10**, 1393 (2019). https://doi.org/10.1038/s41467-019-09406-4

Weber, L.M., Saelens, W., Cannoodt, R. _et al._ Essential guidelines for computational method benchmarking. _Genome Biol_ **20**, 125 (2019). https://doi.org/10.1186/s13059-019-1738-8

# 2 Benchmark plan

## 2.1 Define purpose and scope of benchmark

### 2.1.1 Purpose

1. Benchmarking differential network enrichment tools for RNASeq data and provide guidelines regarding performance
2. Making a reproducible pipeline for metaGRN available to the community
3. Allow the future evaluation of novel methods against a reference.

### 2.1.2 Scope
Data: RNA Seq data from high throughput sequencing data
Technologies: Popular HTP sequencing based technologies (10XGenomics, SmartSeq, Rhapsody)

### Secondary outcomes
- Standard tissue specific GRNs with auxiliary level of information.
- Differential tissue specific consensus Gene Regulatory Networks

## 2.2 Include all relevant methods

### Compile list of relevant publications
- [ ] #task ⏫ Perform Pubmed, Google scholar, and Semantic scholar search
- [ ] #task Categorize methods by algorithmic methodological approach
- [ ] #task prioritize methods by popularity, age
- [ ] #task Create summary table for all methods with name, reference, year, etc; code availability/web page, dependencies, operating system, GUI, tutorial, algorithm category
- [ ] #task Check benchmark/evaluation strategy of the original papers.

### 2.2.1 Inclusion criteria:
1. Any method which constructs differential gene regulatory networks from HTP RNASeq data.

### Exclusion criteria:
1. No publicly available code
2. Cannot be installed with reasonable effort.
3. Cannot be executed with reasonable execution time.
4. Methods requiring additional data modalities which cannot by generated from the gene expression input data or are publicly available such as reference genomes.

## 2.3 Select (or design) representative data sets

### 2.5.1 Ground truth 

#### Plausible ground truth 
1. Atac validation
2. Dorothea, or other validated tools
3. [ ] #task check BEELine publication for ground truth generation

##### ATAC validation

Find matched RNA and ATAC or other open chromatin data and validate eges in the following way. In order for an edge to be counted as a bona-fide differentially regulated edge, the edge needs to be called as differential based on the GEX data and the DNA needs to be accessible in the predicted upregulated edge and less accessible in the predicted downregulated edge. Question is if this is not too restrictive because the DNA could be open but for some reason not read.

- [ ] #task Find matching ATAC and GEX data (n>10)
- [ ] #task find healthy ATAC and GEX for tissues.
- [ ] #task preprocess data in a unified manner.
- [ ] #task call (differential) open chromatin regions
- [ ] #task call (differential) TF binding activity?
- [ ] #task call (differential) enhancer activity.
- [ ] #task Create summary sheet for study information used for validation in the original tool validation  (Database, Study Accession, Publication, Control Sample Accessions included, alternative Accession, file location)
- [ ] #task Create Data folder to collect information (levels: organism, tissue, technology, Accession)
- [ ] #task Create separate data folder and summary sheet for truly matched data from the same biological sample
- [ ] #task Create separate data folder for unmatched healthy tissue ATAC and RNA data to do a tissue wise benchmark.


### Validation pipeline:
1. Compute all GRNs possible for a tool within a time budget AND Compute aggregate GRN for each tool over all individual GRNS.
2. Validate edges using ATAC data. (maybe different levels of evidence): Should we use the indvidual runs, or should we aggregate n runs to form a consensus.
	1. Evaluate scores of the individual GRNs per tool (Are the GRNs good, although they may differ between runs, or does the tool just sometimes randomly find a good GRN?, or never good solution)
	2. If tool finds random good nets, what would be the time budget? Probably not a question we want to ask, if we have no possibility of finding the relevant net from our solution space.
	3. Evaluate scores of the aggregated net (Good consensus, poor consensus.)
3. Generate tool ranking by aggregating the evidence score of the edges.
4. Generate metaNet of the tools, and compute the envidence score based on the ATAC data. Questions answered: Is it worth it running several tools, or should we just run the best scoring tool.


##### Use experimentally validated TF target interactions.
Difficulty here probably will be that we do not see negative interactions and the predicted interactions are not condition specific.

### Experimental data

- Datasets used by the authors of the studies. 
- Bulk RNASeq data
- [ ] #task create minimal data objects in different formats (Seurat, Anndata, tsv) for different bulk technologies for testing and development
- [ ] #task Compile or obtain from a repository list of bulk RNASeq test datasets, uniformly preprocessed.
- Single cell RNASeq data
- [ ] #task Create minimal test datasets in different formats (Seurat, Anndata) for different single cell technologies for testing and development
- [ ] #task Compile or obtain from an online repository a list of single cell datasets uniformly preprocessed, if possible.
- [ ] #task DO NOT Create data information sheet with data used for the evaluation of the studies. (Database, Study Accession, Publication) Useless.
- [ ] #task Create folder for evaluation data only.
- [ ] #task Create different data object with differing subsets of genes, samples, etc. To evaluate tool usability for different data sizes. - Parameter search: Maximal number of comparisons within fixed computational budget
- [ ] #task Create priorization strategy for staying within the budget for grid search/ parameter search


## 2.4 Choose appropriate parameter values and software versions

### Software version
- Latest software
- Most appropriate version if specified by the authors


### Parameter combination
- Recommended setting by the author
- Parameter search: Maximal number of comparisons within fixed computational budget
- [ ] #task Create priorization strategy for staying within the budget for grid search/ parameter search

## 2.5 Evaluate methods according to key quantitative performance metrics

### Evaluation framework
The benchmark will be written as a Nextflow pipeline which will be usable in benchmark mode and in run mode.

- [ ] #task Create evaluation mode for pipeline
	- [ ] Ship/Download data when running in benchmark mode.
	- [ ] Set/load standard parameters for tool 
	- [ ] If applicable, load hyperparameters
	- [ ] Create evaluation script for solution quality
	- [ ] Set up ressource monitoring, internal (nextflow) and for emission/energy scaphandre, codecarbon?


#### 2.5.1.1 Complex target
- Graph similarity
- Tree similarity
- Distribution similarity
- Custom metrics

#### 2.5.1.2 Continuous target
- Root mean square error
- Distance measures
- Pearson correlation
- Sum of absolute log-ratios
- Log-modulus
- Cross-entropy
- Prediction accuracy (supervised)

#### 2.5.1.3 Discrete target
- True positive rate (TPR)
- False positive rate (FPR)
- False discovery rate (FDR)
- Sensitivity and specificity
- precision and recall
- F1 score
- Adjusted Rand index
- Normalized mutual information
- ROC / TPR-FDR / PR curves
- Area under ROC / PR curves
- Classification accuracy (supervised

### 2.5.2 No ground truth
#### 2.5.2.1 Solution quality
- Stability
- Stochasticity
- Robustness
- Null comparisons

##### How to measure stability
1. Set time budget
2. Run tool as many times as possible within time budget
3. Compute deviation of the rank of an edge from the median rank of the edge.
4. Lower deviation > higher confidence edge.
5. Threshold median network based on edge standard deviation
6. Report: Distribution of standard deviations. Which other metrics?
7. Same can be done for nodes, if tool returns a ranked node list.

Robustness to targeted removal of gene?
Robustness to random removal of gene?

#### 2.5.2.2 Computational performance
- Runtime, per dataset, average over all datasets.
- Scalability
- Memory requirements
- Energy requirements


#### Agreement of tools/methods with each other. 
1. Look at edge intersection of the best networks in pairwise comparison between tools
2. Compute intersection score I as: Size of intersection set/size of smaller network.
	1. Make heatmap of the intersection scores. 
	2. Cluster heatmap and see if tools with similar methods deliver similar results.
3. Rank similar tools based on network size in comparison to evidence score. 
	1. Plot size of the best network per tool vs. Atac evidence score
4. Per edge in aggregated meta network using the top n tools of a tool category, look at ranking of edge in the tool to obtain concordance to the meta net. Probably not very interesting.




## 2.6 Evaluation criteria: secondary measures
### 2.5.3 Qualitative

- User-friendliness
- Documentation quality
- Installation procedures
- Freely available / open source
- Code quality
- Use of unit testing
- Use of continuous integration
- Replicability of the figures from the publication  (Network reproducible or not.)
- MVE
-

- [ ] #task Create excel/google sheet with secondary evaluation criteria  

## 2.7 Interpretation, guidelines, and recommendations

- Clear presentation of the results from the user's perspective
- State limitations
- Tasks.
	- [ ] #task Design evaluation metric representation and collect relevant variables that need to be measured to avoid over computation.



Heatmap: y:tool, x: data


## 2.8 Publication and reporting of results
- Journal article
- Wiki page on our webpage
- Nextflow pipeline


## 2.9 Enabling future extensions
- [ ] #task Nextflow pipeline should be clearly documented to allow the easy addition of novel methods
- [ ] 
## 2.10 Reproducible research best practices






