#!/usr/bin/env python

import argparse
import sys
import os
import re
import gzip

"""
    The primer file passed to the -c arg must contain primer name and sequence in this format:
    
    primer_name primer_seq
    
    Example:
    
    primer1 AAAAAAAAAAAAAAAAA
"""


parser = argparse.ArgumentParser(description='Demultiplex a whole lane fastq file in individual files, removing the primers sequences.')
parser.add_argument('-f', dest = "fqfile", metavar='FASTQ_FILE', type=str, help='Input fastq file (required)', required=True)
parser.add_argument('-c', dest="primer",  metavar='PRIMER SEQUENCE', type=str,help='Primer sequence for demultiplex', required=True)
parser.add_argument('-trim', dest = "trim", type=int, metavar='TRIMMED LENGTH', help='Trim to x number of bases (default=75)',default=75)
parser.add_argument('-prefix', dest = "prefix", type=str, metavar='PREFIX', help='Prefix for output files',default="unknown")

args = parser.parse_args()

fqfile = gzip.open(args.fqfile,"rt")
trimmed_size = args.trim
primer = args.primer
fname = args.prefix + ".fq"
ofile = open(fname,"w")

l1_1 = fqfile.readline()
l1_2 = fqfile.readline()
l1_3 = fqfile.readline()
l1_4 = fqfile.readline()

plength = len(primer)+66

while l1_1:
    if re.search(primer,l1_2):
        new_l1_2 = l1_2[plength:(trimmed_size+plength)]
        new_l1_4 = l1_4[plength:(trimmed_size+plength)]
        ofile.write(l1_1 + new_l1_2 + "\n" + l1_3 + new_l1_4 + "\n")

    l1_1 = fqfile.readline()
    l1_2 = fqfile.readline()
    l1_3 = fqfile.readline()
    l1_4 = fqfile.readline()

fqfile.close()
ofile.close()
