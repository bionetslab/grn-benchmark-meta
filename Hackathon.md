
# 1 Hackathon challenges

## 1.1 How to work on a hackathon challenge?
### 1.1.1 Project assignment
1. Pick next available project and assign it to yourself
2. Reads paper and update summary table with missing information
3. Find the code or software online
4. Check if tutorials exist by the authors and update summary sheet.
5. Check if tutorials exist by external authors
6. Find which data has been used by the authors and how it was preprocessed.
7. If available, find the code used for the preprocessing.
8. Check if the authors simulate benchmark data

11. Find the settings the authors used in the publication to generate the figures.
12. Update the data set information sheet with the relevant information.

### 1.1.2 Software assessment

#### 1.1.2.1 Workflow.
1. Install software and create log file according to this file: https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-019-09406-4/MediaObjects/41467_2019_9406_MOESM1_ESM.pdf
3. Check if Minimal working example exists and run if available
4. Check if code exists for creating the figures in the article
5. Attempt to replicate the examples/figures shown in the if not available using the data set(s) supplied in the study.
6. Create script allowing the execution of the tool using all reference data sets.
7. Document method parameters, inputs and outputs.
8. Create Docker container 
9. Supply yaml file for a conda environment.
10. Push code to github repo
11. Create markdown  README in project folder
12. Wiki page with methodology, rationale, parameters, etc.
13. Update secondary evaluation criteria list 
14.  Find the code of benchmark simulation if available
10. Generate benchmark data. 


#### 1.1.2.2 Troubleshooting:
1. Installation fails, document issues. 
2. Run fails, document issues (Memory, CPU, bugs)
3. Run takes more than the allocated time.
4. Other problems occur. Documentation necessary. See reporting sheet.

#### Script input and output requirements
##### Input
- Script needs to be able to read Seurat object and case+control tsv's if in R
- Script needs to read Anndata object and case+control tsv's if in python
- all parameters of the method need to be callable via the script.

#### Output
- Tool needs to output the results in the following standardized format.
	- Edge List
	- Node list
	- ...
- Tool may also output the standard output format, if any significant value for the user is to be expected.


# ToDos

## Software specification
- [ ] #task Define and explain input and output formats
- [ ] #task Define standard output folder structure.
- [ ] #task Define standard for specifying hyperparameters/settings for the evaluation when not using standard settings (.yaml)


## Collaboration specification
- [ ] #task Set up wiki page
- [x] #task Set up Github repository ✅ 2024-01-10
- [ ] #task Define Github folder structure
- [ ] #task Create Wiki page and standard structure

## Teaching material
- [ ] #task Introduction to molecular biology
- [ ] #task Introduction to Scanpy/Anndata
- [ ] #task Introduction to R/tidyverse/bioconductor
- [ ] #task Checklist deliverables


Tag 1: 8.04
Morgens 
Introductoin Mol
tidy data

Nachmittags:
Project selection

Tag 2:
Introdutction to Introduction to R/tidyverse/bioconductor

Tag 3:
Hack

Tag 4: 11.04.

Tag 5 Presentation:

