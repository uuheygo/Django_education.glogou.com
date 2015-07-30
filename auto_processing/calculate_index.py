# Note 1: This function only calculate China marketing index for now, it will not calculate Japan and Asian marketing index.
# Note 2: At this moment, it uses simple method to calculated re-normalized composite index. This need to revisit.  __BL_WARNING__
#
from weight_factor import wf_china_marketing_list
from data_quantization import calculate_normalized_index_with_quantization
from data_quantization import calculate_composite_index_with_quantization

# format of input file, two dimensional array
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
# output: four file names.
#         a file name of normalized index,
#         a file name of composite index,
#         a file name of renormalized index,
#         a file name of renormalized composite index calculated with simple algorithm,
#
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
    # output name format will be: indexes_2015_07_09_09_00_02
    index_arr_file = 'indexes_' + '_'.join(filename.split('_')[1:])

    # file to hold renormalized data, output name format will be: indexes_re_2015_07_09_09_00_02
    index_re_arr_file = 'indexes_re_' + '_'.join(filename.split('_')[1:])

    # Note: the following line to open two files using 'with' does not work for Python 2.6.8, which is the version
    # of Python on Linux crawler server. Python 2.6.8 only supports only one file using 'with'
    #
    # with open(index_arr_file, 'w') as output_index_arr_file, open(index_re_arr_file, 'w') as output_index_re_arr_file:
    try:
        output_index_arr_file = open(index_arr_file, 'w')
        output_index_re_arr_file = open(index_re_arr_file, 'w')

        # calculate normalized index, return in two dimension array
        index_arr = calculate_normalized_index(count_arr, list_average)

        # calculate re-normalized index, return in two dimension array
        index_re_arr = calculate_normalized_index_with_quantization(index_arr)

        for i in range(len(index_arr)):
            output_index_arr_file.write(str(i + 1) + '\t' + '\t'.join(str(x) for x in index_arr[i]) + '\n')

        for i in range(len(index_re_arr)):
            output_index_re_arr_file.write(str(i + 1) + '\t' + '\t'.join(str(x) for x in index_re_arr[i]) + '\n')

        # __FIX_ME__, The following two lines will not be needed if we upgrade python to a newer version
        # so that we can use 'with' to open two files.
        output_index_arr_file.close()
        output_index_re_arr_file.close()

    except:
        print 'File creation error in process_data()'

    # calculate composite indexes and output to file, wf_list holds the weighted factor
    composite_index_list = calculate_composite_index(wf_list, index_arr)
    composite_index_file = 'composite_index_'  + '_'.join(filename.split('_')[1:])
    with open(composite_index_file, 'w') as output_composit_index:
        for i in range(len(composite_index_list)):
            output_composit_index.write(str(i + 1) + '\t' + str(composite_index_list[i]) + '\n')

    # it uses simple method to calculated re-normalized composite index. This need to revisit.  __BL_WARNING__
    composite_index_with_quantization_list = calculate_composite_index_with_quantization(composite_index_list)
    composite_index_re_file = 'composite_re_index_'  + '_'.join(filename.split('_')[1:])
    with open(composite_index_re_file, 'w') as output_composit_re_index:
        for i in range(len(composite_index_with_quantization_list)):
            output_composit_re_index.write(str(i + 1) + '\t' + str(composite_index_with_quantization_list[i]) + '\n')

    return output_index_arr_file.name, output_composit_index.name, output_index_re_arr_file.name, output_composit_re_index.name

# input: a file name of  raw, unprocessed crawled data
# output: four file names.
#         a file name of normalized index,
#         a file name of composite index,
#         a file name of renormalized index,
#         a file name of renormalized composite index calculated with simple algorithm,
#
#         the file name for normalized index will be: indexes_2015_07_09_09_00_02
#         the file name for composite index will be: composite_index_2015_07_09_09_00_02
#         the file name for renormalized index will be: indexes_re_2015_07_09_09_00_02
#         the file name for renormlized composite index will be: composite_re_index_2015_07_09_09_00_02
def calculate_indexes(filename):
    return process_data(filename, wf_china_marketing_list)
    
    
    
    
    