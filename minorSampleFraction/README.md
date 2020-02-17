# MixedGermlineSamples

## Problem Statement

The objective is to write software that classifies SNP counts for mixed germline samples (a minority
sample mixed with a majority sample, e.g., through a contamination mechanism) and estimates the
fraction of the minority sample. For example, allele counts at these generic positions suggest
majority homozygous or heterozygous alleles, with a minority background adding fine structure to
that signature.

The objective is then to identify which SNPs are likely to be informative (i.e., not matching the
majority allele pattern) and calculate the minority sample fraction.

## Inputs:
Any number of .csv files.  They should have three columns with the headers: "dbSNP.ID", "allele",  and "count".

## Outputs:
The output is three .csv's:
1)  the raw file with all .csv's combined (for error checking).

2)  List of all the SNP's per input file.  Column one contains the input file names, the second column
contains the SNP ID, and the third is a flag as to whether or not that SNP is informative (matching the majority allele pattern).

3)  Minority sample fraction per input file: column one contains the input
file names, and the second column contains the estimated minority sample fraction, and the third
column is the uncertainty in that fraction.

If you have questions contact Katie Harding
