#!/usr/bin/env python

import argparse
import sys
import os
import editdist
import re


"""
    The primer file passed to the -c arg must contain primer name and sequence in this format:
    
    primer_name primer_seq
    
    Example:
    
    primer1 AAAAAAAAAAAAAAAAA
"""


parser = argparse.ArgumentParser(description='Demultiplex a whole lane fastq file in individual files, removing the primers sequences.')
parser.add_argument('-f', dest = "fqfile", metavar='FASTQ_FILE', type=argparse.FileType('r'), help='Input fastq file (required)', required=True)
parser.add_argument('-c', dest="primers",  metavar='PRIMERS_FILE', help='File with primers name and sequence (required)', required=True)
parser.add_argument('-fuzzy', dest = "fuzzy", type=int, metavar='MISMATCHES', help='Allow a number of mismatches when demultiplexing')
parser.add_argument('-o', dest = "outdir", type=str, metavar='OUTDIR', help='Output directory',default=".")



args = parser.parse_args()

fqfile = args.fqfile
fuzzy = args.fuzzy
outdir = args.outdir
primers = {}
outfiles = {}
primers_file = open(args.primers)
newdir = outdir + '/Demultiplexed' 
if not os.path.exists(newdir):
    os.makedirs(newdir)

for line in primers_file:
    l = re.split('\s+', line)
    primers[l[0]] = l[1].upper()
    outfilename = newdir + '/' + l[0] + '.fq'
    outfiles[l[0]] = open(outfilename, 'w')

lost = open(newdir + '/' + 'lost.fq', 'w')

l1_1 = fqfile.readline()
l1_2 = fqfile.readline()
l1_3 = fqfile.readline()
l1_4 = fqfile.readline()

while l1_1:
    found = False
    for key in primers.keys():
        seq = primers[key]
        if l1_2.startswith(seq):
            found = True
        if not found and fuzzy:
            seqstart = l1_2[:len(seq)]
            dist = editdist.distance(seq, l1_2[:len(seq)])
            if dist <= fuzzy:
                found = True
        if found:
            new_l1_2 = l1_2[len(seq) - 4:]
            new_l1_4 = l1_4[len(seq) - 4:]
            outfiles[key].write(l1_1 + new_l1_2 + l1_3 + new_l1_4)
            break
            
    if not found:
        lost.write(l1_1 + l1_2 + l1_3 + l1_4)
        
    l1_1 = fqfile.readline()
    l1_2 = fqfile.readline()
    l1_3 = fqfile.readline()
    l1_4 = fqfile.readline()

fqfile.close()
primers_file.close()
for f in outfiles.values():
    f.close()
lost.close()
