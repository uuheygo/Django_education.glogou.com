# Note: This function only calculate China marketing index for now, it will not calculate Japan and Asian marketing index.
#
from weight_factor import wf_china_marketing_list

# ------------input format------------
# id "gg index en", "gg index hk", "gg news","gg site", "bd index ch", "bd index en", "bd news ch", "bd news en", "bd site", "yh index en", "yh index jp"
# delimited by tab
# 11 indexes
#
# __BL__FIX_THIS_, for more generic case, calculate average shall exclude the "extreme value", "those outliers",
# because the "extreme value" or outliers can be wrong data from data sources.
def calculate_average(arr):
    # list of sums
    list_sum = [0] * len(arr[0])
    
    # calculate sums
    for count_list in arr:
        for i in range(len(list_sum)):
            list_sum[i] += count_list[i]
    #print list_sum
    
    # calculate averages
    list_average = []
    num_lines = len(arr)
    for sum in list_sum:
        list_average.append(sum / num_lines)
        
    return list_average

# convert counts to normalized indexes
# Input: count_arr, a two dimension array of raw count,
#        avearge_list, a one dimension array which contains the average of above two dimension arrays.
# output: a two dimension array of normalized data.
#
# ___FIX_THIS__, average can be zero for more generic case. Need to handle such situation
def calculate_normalized_index(count_arr, average_list):
    index_arr = []
    for count_list in count_arr:
        index_list = []
        for count, average in zip(count_list, average_list):
            index_list.append(count * 1.0 / average)
        index_arr.append(index_list)
        #print index_list
    return index_arr

# calculate composite index with weighted factors
# Input: index_arr, a two dimension array of normalized index.,
#        wf_list,, a one dimension array which contains the weight factor
# output: a one dimension array of composite_index_list
def calculate_composite_index(wf_list, index_arr):
    composite_index_list = [] # composite indexes
    for index_list in index_arr:
        composite_index = 0
        for index, wf in zip(index_list, wf_list):
            composite_index += index * wf
        composite_index_list.append(composite_index)
    
    return composite_index_list

# input: a file name of  raw, unprocessed crawled data
# output: a file name of normalized index, a file name of composite index
def process_data(filename, wf_list):
    # read all indexes into a 2-D array
    count_arr = []
    
    with open(filename, 'r') as f:
        for line in f.readlines()[1:]: # data is from 2nd line
            count_arr.append([int(count) for count in line.strip().split('\t')[1:]])
    #print count_arr
    
    list_average = calculate_average(count_arr)
    print list_average
    
    # calculate individual indexes and output to file
    index_arr_file = 'indexes_' + '_'.join(filename.split('_')[1:])
    with open(index_arr_file, 'w') as output_index_arr_file:
        index_arr = calculate_normalized_index(count_arr, list_average)
        for i in range(len(index_arr)):
            output_index_arr_file.write(str(i + 1) + '\t' + '\t'.join(str(x) for x in index_arr[i]) + '\n')
    
    # calculate composite indexes and output to file
    
    #----------china market----------
    #     "gg index en"           3
    #     "gg index hk"           4
    #     "gg news"               2
    #     "gg site"               3
    #     "bd index ch"           8
    #     "bd index en"           2
    #     "bd news ch"            7
    #     "bd news en"            2
    #     "bd site"               7
    #     "yh index en"           0
    #     "yh index jp"           0
    

    composite_index_list = calculate_composite_index(wf_list, index_arr)
    composite_index_file = 'composite_index_'  + '_'.join(filename.split('_')[1:])
    with open(composite_index_file, 'w') as output_composit_index:
        for i in range(len(composite_index_list)):
            output_composit_index.write(str(i + 1) + '\t' + str(composite_index_list[i]) + '\n')
    
    return output_index_arr_file.name, output_composit_index.name

# input: a file name of  raw, unprocessed crawled data
# output: a file name of normalized index, a file name of composite index
def calculate_indexes(filename):
    return process_data(filename, wf_china_marketing_list)
    
    
    
    
    