# Halogenase
This repository provides the profile hidden Markov model (pHMM) for flavin-dependent tryptophan halogenase (Trp-FDH) and Python script for filtering result of pHMM search and leave-one-out cross-validation.

>## Pre-installed programs
* Python version 2.7.12 or higher with argparse library
* HMMER3.0 package version 3.1b2 or higher
* Clustal Omega version 1.2.4 or higher

>## Filtering result of pHMM search
* ### pHMM search
  - To perform the pHMM search, *hmmscan* in HMMER3.0 package is used with "--domtblout" option.   
  - A query should be included as protein sequences in the FASTA format file.   
```
USAGE:
$ hmmscan --domtblout output_file_name.domtblout pHMM/Trp_FDH.hmm query.fasta
```

* ### Filtering .domtblout file
  - To filter the .domtblout file, ```code/domtblout_filtering.py``` is used.   
  - According to the threshold for e-value and pHMM model coverage, the search result is filtered.
```
USAGE:
$ python domtblout_filtering.py -i example/example_input.domtblout -o example/example_output.domtblout -e e-value -c model_coverage
```

>## Leave-one-out cross-validation (LOOCV)
* LOOCV
  - To perform the LOOCV, ```code/leave-one-out_hmmscan.py``` is used.
  - Input file of this code is in ```pHMM/Trp-FDH.fasta```.
  - Training data and test data are generated as many as the number of sequences in the input file, respectively.
  - To build pHMMs of training data, multiple sequence alignment (MSA) are performed by Clustal Omega (v1.2.4).
  - Using the results of MSA (.sto file), pHMM models were constructed by *hmmbuild* in HMMER3.0 package.
  - The pHMM search with the pHMM or training data and test set is executed.
  - The pHMM search results are summarized in terms of evalue (avg. std., and median of evalue).
 
```
USAGE:
$ python leave-one-out_hmmscan.py --fasta pHMM/Trp-FDH.fasta
```
