#!/usr/bin/env python3
# -*-coding: utf-8 -*-

"""
Minox Stats Script v 0.1 28/02/15
Michael O'Sullivan
"""

import numpy as np
import matplotlib.pyplot as plt
import sys, os, glob

from scipy.stats import itemfreq    # for frequency count
from pprint import pprint           # similar to Ruby's inspect

# processed column indices
date_index = 0
raw_items_index = 1
proof_items_index = 2
files_index = 3

# params
outfile_name = "stats_feb.pdf"
infile_name = "data/stats_24_feb.csv"

x_label = "Count"
y_label = "Frequency"

def read_file(input_file):
    '''Read the file lines into a multi-array'''
    file_data = open(input_file, 'r')
    result = []
    for line in file_data:
        # get rid of comments
        first = line.find('#')
        if first >= 0:
            line = line[:first]
        if not line:
            continue
        columns = line.strip().split(",")
        #result.append(columns)
        result.append(process_columns(columns,date_index))
    file_data.close()
    return np.array(result)

def process_columns(columns, date_index):
    return [np.datetime64(columns[date_index])] + [int(m) for m in columns[-3:]]

def frequency_count(in_np_array):
    unique, counts = np.unique(in_np_array, return_counts=True)

def interquartile_stats(in_np_array):
    q75, q25 = np.percentile(in_np_array, [75, 25])
    iqr = q75 - q25
    return [iqr, q25, q75]

"""
For Numpy >= 1.9 there is a better way:
def numpy_frequency_count(in_np_array):
    ''' Numpy 1.9 required for return_counts '''
    unique, counts = np.unique(x, return_counts=True)
    return np.asarray((unique, counts)).T
"""

def main():
    lines = read_file(infile_name)
    proof_items_count = lines[:,proof_items_index]
    file_counts = lines[:,files_index]
    proof_items_freq = itemfreq(proof_items_count)
    file_count_freq = itemfreq(file_counts)

    # zero frequency values are from mileage-only claims, which we don't need
    proof_items_freq[0][1] = 'NaN'
    file_count_freq[0][1] = 'NaN'
    # print some output

    pprint(proof_items_freq)
    pprint(file_count_freq)

    print("Median non-mileage claim items per claim: {}".format(np.median(proof_items_count)))
    iqr_claims = interquartile_stats(proof_items_count)
    iqr_files = interquartile_stats(file_counts)
    print("IQR: {}, Q25: {}, Q75: {}".format(iqr_claims[0], iqr_claims[1], iqr_claims[2]) )
    print("Median files per claim: {}".format(np.median(file_counts)))
    print("IQR: {}, Q25: {}, Q75: {}".format(iqr_files[0], iqr_files[1], iqr_files[2]) )
    print("Max files per claim: {}".format(np.max(file_counts)))
    print("Max non-mileage claim_items per claim: {}".format(np.max(proof_items_count)))
    print("Max claim_items per claim: {}".format(np.max(lines[:,raw_items_index ])))

    # Create a new 8 x 6 80 dpi figure
    plt.figure(figsize=(8,6), dpi=80)

    # Create a new subplot from a 1 x 1 grid
    plt.subplot(1,1,1)



    # Plot the claim item count frequency freq v count
    plt.plot(proof_items_freq[:,0], proof_items_freq[:,1], 'k.', linewidth=1.0, label="Non-Mileage Items")

    # Plot the file count frequency freq v count
    plt.plot(file_count_freq[:,0], file_count_freq[:,1], 'wo', linewidth=2.0, label="Files")

    # Legend in upper right
    plt.legend(loc='best', ncol=1, numpoints=1)

    plt.xlabel("Count")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == '__main__':
    main()


