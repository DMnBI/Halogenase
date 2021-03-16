# Halogenase
This repository provides the profile hidden Markov model (pHMM) for flavin-dependent tryptophan halogenase (Trp-FDH) and Python script for filtering result of pHMM search.

>## Pre-installed programs
* Python version 2.7.12 or higher with argparse library
* HMMER3.0 package version 3.1b2 or higher

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

