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
from scipy.stats import percentileofscore
from pprint import pprint           # similar to Ruby's inspect

# raw column indices
raw_date_index = 1

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
    return [np.datetime64(columns[raw_date_index])] + [int(m) for m in columns[-3:]]

def frequency_count(in_np_array):
    unique, counts = np.unique(in_np_array, return_counts=True)

def get_ratio_data(num_array, den_array):
    # might be able to do this with a mask instead ...
    out_num_list = []
    out_den_list = []
    for index, val in enumerate(den_array):
        print(num_array[index])
        if den_array[index] != 0:
            out_num_list.append(num_array[index])
            out_den_list.append(den_array[index])
    out_num_array = np.array(out_num_list)
    out_den_array = np.array(out_den_list)
    return out_num_array/(1.0 * out_den_array)

def interquartile_stats(in_np_array):
    q75, q25 = np.percentile(in_np_array, [75, 25])
    iqr = q75 - q25
    return [iqr, q25, q75]

"""
For Numpy >= 1.9 there is a better way:
def numpy_frequency_count(in_np_array):
    unique, counts = np.unique(x, return_counts=True)
    return np.asarray((unique, counts)).T
"""

def main():
    lines = read_file(infile_name)
    proof_items_count = lines[:,proof_items_index]
    file_counts = lines[:,files_index]
    proof_items_freq = itemfreq(proof_items_count)
    file_count_freq = itemfreq(file_counts)

    min_date = lines[:,date_index].min()
    max_date = lines[:,date_index].max()

    plot_title = "Dates: {} to {}".format(min_date, max_date)

    total_claims = proof_items_count.size
    total_nonmileage_claims = total_claims - proof_items_freq[0][1]

    print("Total claims: {}".format(total_claims))
    print("Total non-mileage claims: {}".format(total_nonmileage_claims))

    items_per_file = get_ratio_data(proof_items_count, file_counts)

    # zero frequency values are from mileage-only claims, which we don't need
    proof_items_freq[0][1] = 'NaN'
    file_count_freq[0][1] = 'NaN'

    #pprint(proof_items_freq)
    #pprint(file_count_freq)

    print("Median non-mileage claim items per claim: {}".format(np.median(proof_items_count)))
    iqr_claims = interquartile_stats(proof_items_count)
    iqr_files = interquartile_stats(file_counts)
    print("IQR: {}, Q25: {}, Q75: {}".format(iqr_claims[0], iqr_claims[1], iqr_claims[2]) )
    print("Median files per claim: {}".format(np.median(file_counts)))
    print("IQR: {}, Q25: {}, Q75: {}".format(iqr_files[0], iqr_files[1], iqr_files[2]) )
    print("Max files per claim: {}".format(np.max(file_counts)))
    print("Max non-mileage claim_items per claim: {}".format(np.max(proof_items_count)))
    print("Max claim_items per claim: {}".format(np.max(lines[:,raw_items_index ])))
    print("20 Claim items percentile: {}".format(percentileofscore(proof_items_count, 20)))
    print("20 Files items percentile: {}".format(percentileofscore(file_counts, 20)))
    iqr_ratio = interquartile_stats(items_per_file)
    print("Median claim items per file: {}".format(np.median(items_per_file)))
    print("2 claim items per file percentile: {}".format(percentileofscore(items_per_file, 2)))
    print("3 claim items per file percentile: {}".format(percentileofscore(items_per_file, 3)))
    print("5 claim items per file percentile: {}".format(percentileofscore(items_per_file, 5)))
    print("10 claim items per file percentile: {}".format(percentileofscore(items_per_file, 10)))
    print("IQR: {}, Q25: {}, Q75: {}".format(iqr_ratio[0], iqr_ratio[1], iqr_ratio[2]) )

    # Create a new 8 x 6 80 dpi figure
    fig = plt.figure(figsize=(8,6), dpi=80)

    # Create a new subplot from a 2 x 1 grid
    # -------------- Top Plot
    top_plt = fig.add_subplot(2,1,1)  # rows, columns, id

    # Plot the claim item count frequency freq v count
    top_plt.plot(proof_items_freq[:,0], proof_items_freq[:,1], 'k.', linewidth=1.0, label="Non-Mileage Items")
    # Plot the file count frequency freq v count
    top_plt.plot(file_count_freq[:,0], file_count_freq[:,1], 'wo', linewidth=2.0, label="Files")
    # Legend in upper right
    top_plt.legend(loc='best', ncol=1, numpoints=1, fontsize=12)

    top_plt.set_title(plot_title)

    # -------------- Bottom plot
    btm_plt = fig.add_subplot(2,1,2)  # rows, columns, id
    btm_plt.loglog(proof_items_freq[:,0], proof_items_freq[:,1], 'k.', linewidth=1.0, label="Non-Mileage Items")
    btm_plt.loglog(file_count_freq[:,0], file_count_freq[:,1], 'wo', linewidth=2.0, label="Files")
    btm_plt.axis('tight')

    # Set common labels
    fig.text(0.5, 0.04, 'count', ha='center', va='center')
    fig.text(0.06, 0.5, 'frequency', ha='center', va='center', rotation='vertical')

    plt.savefig(outfile_name)

if __name__ == '__main__':
    main()


