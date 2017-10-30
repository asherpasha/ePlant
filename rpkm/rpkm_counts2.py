import pandas as pd
import pickle
import HTSeq
import collections
import json

def GTFReader(gtf): #GFF is a format for annotation data
    gtf_file = HTSeq.GFF_Reader(gtf)
    exons = HTSeq.GenomicArrayOfSets( "auto", stranded=False ) #enables labelling of each position with multiple gene ids
    for feature in gtf_file:
        if feature.type == "exon":
            exons[ feature.iv ] += feature.attr["gene_id"] #actually labels each exonic position to all associated gene ids
    return exons

def GetFeatures(SRR):
    counts = collections.Counter( )
    almnt_file = HTSeq.BAM_Reader(SRR) #iterables are of type Alignment, with attributes .read, .aligned, and .iv
    for almnt in almnt_file:
        if not almnt.aligned: #aligned is a Boolean indicating if a read was aligned to the reference
            counts[ "_unmapped" ] += 1
            continue
        gene_ids = set()
        for iv, val in exons[almnt.iv].steps(): #cycles through all exonic intervals (with sequence-uninterrupted labelling) shared by the read almnt.iv
            gene_ids |= val #combines all gene id labels from the positions overlapping with the read
        if len(gene_ids) == 1: #for reads that were aligned to exons belonging to exactly one gene
            gene_id = list(gene_ids)[0]
            counts[ gene_id ] += 1
        elif len(gene_ids) == 0: #for reads that were not aligned to any exons
            counts[ "_no_feature" ] += 1
        else:	# for reads that were aligned to exons belonging to more than one gene
            counts[ "_ambiguous" ] += 1
    # for gene_id in counts:
    #print(gene_id, counts[ gene_id ])
    return counts

def CountsToJson(counter, file_name):
    counterJson = json.dumps(counter)
    with open(file_name, "w") as outfile:
        json.dump(counterJson, outfile)


#constants=====================================================================#

gtf = "/home/eesteban/files/araport.gtf"
exons = GTFReader(gtf)
pickle_out = open("/home/eesteban/files/gtf_exons.pickle", "wb")
pickle.dump(exons, pickle_out)
pickle_out.close()

SRR3581889 = "/home/eesteban/SRR3581889/accepted_hits.bam"
SRR3581889 = GetFeatures(SRR3581889)
CountsToJson(SRR3581889, "/home/eesteban/files/SRR3581889_counts2.json")
# SRR3581336 = "/DATA/Klepikova/SRR3581336/accepted_hits.bam"
# SRR3581336 = GetFeatures(SRR3581336)

# file_name = "/home/thuang/files/SRR3581336.txt"
# json_counter = CountsToJson(SRR3581336, file_name)

# gtf = pd.read_csv("/home/thuang/files/araport.gtf", sep = "\t", header = None)
# cleaned_gtf = CleanUpGtf(gtf)

# pickle_in = open("/home/thuang/files/counts.pickle", "rb")
# counts = pickle.load(pickle_in)
