# Initial creation date: 6/30/2015
# Initial Author: _BL_
#
# Algorithm to implement non-uniform quantization
#
# The reason that non-uniform quantization is needed is because "linear quantization of the collected count"
# can NOT correctly measure the "true" marketing influence of a media. Particularly, someone times, one "extreme" data
# point can distort the index for one particular media channel or composite index.
#
# For example, assume that on average, Baidu indexed 1,000 pages of each school.. And one school with has lots of
# webpages, Baidu indexed 1,000,000 pages. If we use uniform normalization, this one particular data point distort
# not only index for Baidu indexing, but overall composite (even if we exclude "outlier" when we calculate average).
#
# There are multiple ways to do non-uniform quantization.
# Method 1:  u-law type quantization.
# Method 2:  logarithmic quantization
#
# We will choose method 2, because
# a. It is simple to implement
# b. Because "marketing influence" has the "compounding" effect. So the "true measure" of "marketing influence"
#    shall take logarithmic of collected data.
#
# Implementation details:
#  At this moment, for each data point x, since it is normalized data, so on average ,it is close to 1, but it can still
#  have large range, anyway from 0 to large number. To avoid negative value of logarithm, we multiply each number
#  by 1000, then take 10, and convert to db.
#  we use 20*log10(x*1000) = 20*log10(x) + 60
#  If this number is less than 0, which means x < 0.001, then, we set above to 0.
#
# NOTE, __TO_IMPROVE__
# 1. For 1st order approximation, we use the same non-uniform quantization for each media,
#    For better approximation, we shall use different non-uniform quantization for different media data set.
#    For example, the quantization methods for "pages indexed by search engines" shall be different from
#    the "number of followers on social media, such as, Facebook, Twitter, etc".

import math

#input: index, normalized value, typical value shall be around 1, but it can any decimal number from 0 to a large number
#output: a decimal number by applying non-uniform quantization
#        if input value is less than 0.001 or 0, output will be 0. This function will not return negative value
def non_uniform_quantization(index):

    if (index == 0):
        return 0

    # logarithmic quantizaton method: 20*log10(x*1000) = 20*log10(x) + 60
    # __FIX_ME_IMPORTANT__, Shall we add +60 or +40, ?
    quantized = 20*math.log(index, 10) + 60

    # If quantized is less than 0, which means normalized count is less than 0.001,
    # we set to ZERO
    if(quantized < 0):
        quantized = 0

    return quantized

# Input: a two dimensional array which hold normalized data of collected count.
# Output: a two dimensional array which hold quantized normalized data.
def calculate_normalized_index_with_quantization(index_arr):
    index_arr_quantized = []

    for index_list in index_arr:
        index_list = []
        for index in (index_list):

            quantized = non_uniform_quantization(index)
            index_list.append(quantized)

        index_arr_quantized.append(index_list)

    return index_arr_quantized

# calculate composite index with weighted factors for quantized index.
# Input: index_arr, a two dimension array of quantized normalized index, typically, it is non-uniform quantized
#        wf_list,, a one dimension array which contains the weight factor
# output: a one dimension array of composite_index_list
#
# NOTE: __FIX_THIS__
# At this moment, this function is just a copy of calculate_composite_index(...) in calculate_index.py
# This is debatable. Why ?
#
# Because if we use "logarithmic quantization", then the weighted average will be equal to the
# the geometric average, not arithmetic average. Is this really what we want ?
# Will geometric average of different media index is a better measurement of overall marketing influence ?
#
def calculate_composite_index_with_quantization(wf_list, index_arr):

    composite_index_list = [] # composite indexes

    for index_list in index_arr:
        composite_index = 0
        for index, wf in zip(index_list, wf_list):

            # weighted average
            composite_index += index * wf

        composite_index_list.append(composite_index)

    return composite_index_list