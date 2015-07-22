## _BY_BL_
## Date: 11-13-2014
## Last Modify Date: 2-5-2015
## use numpy and matplotlib.pyplot to do data analysis

import string
import sys
import time
import codecs
import copy
import math
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np
import pprint

def read_data(in_file_name):

    try:
        in_f = codecs.open(in_file_name, 'r', 'utf-8')
    except:
        print 'file read error'
        sys.exit(0)

    cnt = 0

    bd_index_eng_list = []
    bd_news_eng_list = []
    gg_index_eng_list =  []

    for line in in_f:

        # Try to handle each line
        try:

            columns = string.split(line, '\t')

            print '=======before ===='
            print columns
            print '=======after ====='

            bd_index_eng = columns[1]
            bd_news_eng = columns[3]
            gg_index_eng = columns[5]

            bd_index_eng_list.append(float(bd_index_eng))
            bd_news_eng_list.append(float(bd_news_eng))
            gg_index_eng_list.append(float(gg_index_eng))

        except:
            error_str = 'cnt %d, columns %s'%(cnt, columns)
            print error_str
            continue

    in_f.close()

    return bd_index_eng_list,  bd_news_eng_list, gg_index_eng_list

# read media weight factor file and return  media_weight_factor 2D dict and also the size of 2D dict
# return
# d_arr, two dict, the real values are from column 1, row 1; column 0 and row 0 do not hold real value
# d_arr_rows, number of row, include row 0
# d_arr_cols, number of column, include column 0
def read_media_weight_factor(media_weight_factor_file):
    try:
        media_weight_factor_f = codecs.open(media_weight_factor_file, 'r', 'utf-8')
    except:
        print 'file read error: %s'%(media_weight_factor_file)
        sys.exit(0)

    # read media_weight_factor as two dimensional array using a dict
    # We do it by read the media_weight_factor_file twice.
    # 1st time just to get the size of two dimensions
    number_of_row = 0
    for line in media_weight_factor_f:
        columns = string.split(line, '\t')

        number_of_row = number_of_row + 1
        number_of_columns = len(columns)

    # first column and 1st row do not hold real value of media_weight_factor matrix
    # because those are just comments
    d_arr_rows = number_of_row
    d_arr_cols = number_of_columns

    # create a  2D-array using a dictionary with index tuples
    # as keys, initialize with zero. Column 0 and row 0 do NOT hold any real value a
    d_arr = {(x,y):0 for x in range(d_arr_rows) for y in range(d_arr_cols)}

    # read the again and fill up the matrix
    media_weight_factor_f.seek(0, 0)
    number_of_row = 0

    for line in media_weight_factor_f:

        # skip the 1st line, because it is a comment line
        if(number_of_row == 0):
            number_of_row = number_of_row + 1
            continue

        temp = line.rstrip()
        columns = string.split(temp, '\t')

        print columns
        number_of_columns = len(columns)

        # start from 2nd column, because 1st column is NOT an number
        for j in range(1, number_of_columns):
            d_arr[number_of_row, j]= float(columns[j])

        number_of_row = number_of_row + 1


    # We ue pprint to print out dict, the simple print will not print dict in right format
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(d_arr)

    return d_arr, d_arr_rows, d_arr_cols

# calculate media index with weight factor, weighted average of factor
# At this moment, this function is not flexible, because it takes fixed input. If we add one or input, then
# this function need to re-write. This is not a good design, but let's us it for now.
# return:
#   china_media_index,
#   asia_media_index,
#   japan_media_index
def calculate_media_index_with_weight(d_arr, bd_index_common, bd_index_chinese, bd_news_common, bd_news_chinese, gg_index_common, gg_new, gg_hk, gg_site, bd_site, yj_index_eng):

    china_media_index = bd_index_common*d_arr[1, 1] + \
                        bd_index_chinese*d_arr[1, 2] + \
                        bd_news_common*d_arr[1, 3] + \
                        bd_news_chinese*d_arr[1, 4] +\
                        gg_index_common*d_arr[1, 5] + \
                        gg_new*d_arr[1, 6] + \
                        gg_hk*d_arr[1, 7]  + \
                        gg_site*d_arr[1, 8] + \
                        bd_site*d_arr[1, 9] + \
                        yj_index_eng*d_arr[1, 10]

    if(china_media_index > 1000):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d_arr)

    asia_media_index = 0

    asia_media_index =  bd_index_common*d_arr[2, 1] + \
                        bd_index_chinese*d_arr[2, 2] + \
                        bd_news_common*d_arr[2, 3] + \
                        bd_news_chinese*d_arr[2, 4] +\
                        gg_index_common*d_arr[2, 5] + \
                        gg_new*d_arr[2, 6] + \
                        gg_hk*d_arr[2, 7] + \
                        gg_site*d_arr[2, 8] + \
                        bd_site*d_arr[2, 9] + \
                        yj_index_eng*d_arr[2, 10]


    if(asia_media_index > 1000):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d_arr)

    japan_media_index = bd_index_common*d_arr[3, 1] + \
                        bd_index_chinese*d_arr[3, 2] + \
                        bd_news_common*d_arr[3, 3] + \
                        bd_news_chinese*d_arr[3, 4] +\
                        gg_index_common*d_arr[3, 5] + \
                        gg_new*d_arr[3, 6] + \
                        gg_hk*d_arr[3, 7] + \
                        gg_site*d_arr[3, 8] + \
                        bd_site*d_arr[3, 9] + \
                        yj_index_eng*d_arr[3, 10]


    if(japan_media_index > 1000):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(d_arr)

    return china_media_index, asia_media_index, japan_media_index

# For each column, we will exclude the largest data and smallest data,
# then we use the rest data to find out the industry average
#
def process_raw_data(in_file_name, out_file_name, media_weight_factor_file):

    try:
        in_f = codecs.open(in_file_name, 'r', 'utf-8')
    except:
        print 'file read error: %s'%(in_file_name)
        sys.exit(0)

    try:
        out_f = codecs.open(out_file_name, 'w', 'utf-8')
    except:
        print 'file creation error: %s'%(out_file_name)
        sys.exit(0)

    english_phrase_list = []
    chinese_phrase_list = []
    bd_index_eng_list = []
    bd_index_chinese_list = []
    bd_news_eng_list = []
    bd_news_chinese_list = []
    gg_index_eng_list = []
    gg_news_list = []
    gg_hk_list = []
    gg_site_list = []
    bd_site_list =[]
    yj_index_eng_list = []

    # read input file and put content column by column into lists
    cnt = 0
    for line in in_f:

        # Try to handle each line
        try:

            columns = string.split(line, '\t')

            print '=======before ===='
            print columns
            print '=======after ====='

            # first line is menu line, will not do any processing
            if (cnt == 0):
                cnt = cnt + 1
                continue

            # put each column into an list
            english_phrase = columns[0]
            chinese_phrase = columns[1]
            bd_index_eng = columns[2]
            bd_index_chinese = columns[3]
            bd_news_eng = columns[4]
            bd_news_chinese = columns[5]
            gg_index_eng = columns[6]
            gg_news = columns[7]
            gg_hk = columns[8]
            gg_site = columns[9]
            bd_site = columns[10]
            yj_index_eng = columns[11]

            english_phrase_list.append(english_phrase)
            chinese_phrase_list.append(chinese_phrase)
            bd_index_eng_list.append(float(bd_index_eng))
            bd_index_chinese_list.append(float(bd_index_chinese))
            bd_news_eng_list.append(float(bd_news_eng))
            bd_news_chinese_list.append(float(bd_news_chinese))
            gg_index_eng_list.append(float(gg_index_eng))
            gg_news_list.append(float(gg_news))
            gg_hk_list.append(float(gg_hk))
            gg_site_list.append(float(gg_site))
            bd_site_list.append(float(bd_site))
            yj_index_eng_list.append(float(yj_index_eng))

        except:
            error_str = 'cnt %d, columns %s'%(cnt, columns)
            print error_str
            continue

    in_f.close()

    # normalize each list with industry average
    bd_index_eng_average_no_extreme, bd_index_eng_normalized_list = normalize_and_get_average_exclude_extreme(bd_index_eng_list)
    bd_index_chinese_average_no_extreme, bd_index_chinese_normalized_list = normalize_and_get_average_exclude_extreme(bd_index_chinese_list)
    bd_news_eng_average_no_extreme, bd_news_eng_normalized_list = normalize_and_get_average_exclude_extreme(bd_news_eng_list)
    bd_news_chinese_average_no_extreme, bd_news_chinese_normalized_list = normalize_and_get_average_exclude_extreme(bd_news_chinese_list)
    gg_index_eng_average_no_extreme, gg_index_eng_normalized_list = normalize_and_get_average_exclude_extreme(gg_index_eng_list)
    gg_news_average_no_extreme, gg_news_normalized_list = normalize_and_get_average_exclude_extreme(gg_news_list)
    gg_hk_average_no_extreme, gg_hk_normalized_list = normalize_and_get_average_exclude_extreme(gg_hk_list)
    gg_site_average_no_extreme, gg_site_normalized_list = normalize_and_get_average_exclude_extreme(gg_site_list)
    bd_site_average_no_extreme, bd_site_normalized_list = normalize_and_get_average_exclude_extreme(bd_site_list)
    yj_index_eng_average_no_extreme, yj_index_eng_normalized_list = normalize_and_get_average_exclude_extreme(yj_index_eng_list)

    number_of_entries = len(bd_index_eng_normalized_list)
    assert(number_of_entries == len(english_phrase_list))
    assert(number_of_entries == len(chinese_phrase_list))
    assert(number_of_entries == len(bd_index_chinese_normalized_list))
    assert(number_of_entries == len(bd_news_eng_normalized_list))
    assert(number_of_entries == len(bd_news_chinese_normalized_list))
    assert(number_of_entries == len(gg_index_eng_normalized_list))
    assert(number_of_entries == len(gg_news_normalized_list))
    assert(number_of_entries == len(gg_hk_normalized_list))
    assert(number_of_entries == len(gg_site_normalized_list))
    assert(number_of_entries == len(bd_site_normalized_list))
    assert(number_of_entries == len(yj_index_eng_normalized_list))

    # Read the media weight factor, we will need those to calculate media index
    d_arr, d_arr_rows, d_arr_cols = read_media_weight_factor(media_weight_factor_file)

    # At this moment, we know there are only three type of media index,
    # if we want the program to be more flexible, we shall define 'd_arr_rows - 1' type of media_index_list
    china_media_index_list=[]
    japan_media_index_list=[]
    asia_media_index_list=[]

    # print menu bar first
    out_str = u'%s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s\t %s\t %s\n'%('english_phrase',
                'chinese_phrase',
                'bd_index_common',
                'bd_index_chinese',
                'bd_news_common',
                'bd_news_chinese',
                'gg_index_common',
                'gg_new',
                'gg_hk',
                'gg_site',
                'bd_site',
                'yj_index_eng',
                'china_media_index',
                'asia_media_index',
                'japan_media_index')

    out_f.write(out_str)
    out_f.flush()

    # cumulate the sum so to calculate average
    china_media_index_sum = 0
    asia_media_index_sum = 0
    japan_media_index_sum = 0

    for i in range(0, number_of_entries):

        english_phrase = english_phrase_list[i]
        chinese_phrase = chinese_phrase_list[i]
        bd_index_common = bd_index_eng_normalized_list[i]
        bd_index_chinese = bd_index_chinese_normalized_list[i]
        bd_news_common = bd_news_eng_normalized_list[i]
        bd_news_chinese = bd_news_chinese_normalized_list[i]
        gg_index_common = gg_index_eng_normalized_list[i]
        gg_new = gg_news_normalized_list[i]
        gg_hk = gg_hk_normalized_list[i]
        gg_site = gg_site_normalized_list[i]
        bd_site = bd_site_normalized_list[i]
        yj_index_eng = yj_index_eng_normalized_list[i]

        # calculate media index with weight factors
        china_media_index, asia_media_index, japan_media_index = calculate_media_index_with_weight(d_arr, bd_index_common, bd_index_chinese, bd_news_common, bd_news_chinese, gg_index_common, gg_new, gg_hk, gg_site, bd_site, yj_index_eng)

        # record media index to the list
        china_media_index_list.append(china_media_index)
        asia_media_index_list.append(asia_media_index)
        japan_media_index_list.append(japan_media_index)

        # cumulate the sum so to calculate average
        china_media_index_sum  = china_media_index_sum + china_media_index
        asia_media_index_sum  = asia_media_index_sum + asia_media_index
        japan_media_index_sum  = japan_media_index_sum + japan_media_index

        out_str = u'%s \t %s \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f\n'%(english_phrase,
                    chinese_phrase,
                    bd_index_common,
                    bd_index_chinese,
                    bd_news_common,
                    bd_news_chinese,
                    gg_index_common,
                    gg_new,
                    gg_hk,
                    gg_site,
                    bd_site,
                    yj_index_eng,
                    china_media_index,
                    asia_media_index,
                    japan_media_index)

        print out_str

        out_f.write(out_str)
        out_f.flush()

        cnt = cnt + 1
        print 'cnt %d china_media_index_sum %f\n'%(cnt, china_media_index_sum)
        print 'cnt %d asia_media_index_sum %f\n'%(cnt, asia_media_index_sum)
        print 'cnt %d japan_media_index_sum %f\n'%(cnt, japan_media_index_sum)

    # Media Index Average
    china_media_index_ave = china_media_index_sum/number_of_entries
    asia_media_index_ave = asia_media_index_sum/number_of_entries
    japan_media_index_ave = japan_media_index_sum/number_of_entries

    # Put average of every component to the file
    out_str = u'\n'
    out_f.write(out_str)

    out_str = u'%s \t %s \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f \t %f\n'%('Average ',
            'Value ',
            bd_index_eng_average_no_extreme,
            bd_index_chinese_average_no_extreme,
            bd_news_eng_average_no_extreme,
            bd_news_chinese_average_no_extreme,
            gg_index_eng_average_no_extreme,
            gg_news_average_no_extreme,
            gg_hk_average_no_extreme,
            gg_site_average_no_extreme,
            bd_site_average_no_extreme,
            yj_index_eng_average_no_extreme,
            china_media_index_ave,
            asia_media_index_ave,
            japan_media_index_ave)


    out_f.write(out_str)
    out_f.flush()
    out_f.close()

    print out_str
    print 'COMPLETE Normalization'

    #return media index ave and list
    return china_media_index_ave, asia_media_index_ave, japan_media_index_ave, china_media_index_list, japan_media_index_list, asia_media_index_list

# For a list, we will find out the largest number, smallest number. Those numbers are consider 'abnormal',
# then we will calculate average for the rest of the number.
# return:
# average_no_extreme, 
# normalized_list
def normalize_and_get_average_exclude_extreme(input_list):

    number_of_entry = len(input_list)

    copy_list = list(input_list)
    copy_list.sort()
    min = copy_list[0]
    max = copy_list[number_of_entry -1]

    # find average exclude max and min term,
    # maybe we can use numpy built-in function for calculating average, but it is simple to write this function
    # ourselves
    sum = 0.0

    # This loop start from 1, and end at (number_of_entry - 1), it will skip two numbers at ends
    for i in range(1, number_of_entry - 1):
        sum = sum + copy_list[i]

    # we need to divide 'number_of_entry - 2' because we exclude min, max
    average_no_extreme = sum/(number_of_entry - 2)

    # At this moment, there is no reason that average is 0, because all numbers are positive
    # average zero means that every term is ZERO
    if(average_no_extreme == 0):
        print 'WARNING: average_no_extreme is ZERO'

    # normalize the list by average
    normalized_list = []

    # if average_no_extreme is ZERO, we will not normalize anything, just copy the input_list to output
    if(average_no_extreme == 0):
        normalized_list = list(input_list)
        return average_no_extreme, normalized_list

    # maybe we can use numpy built-in function to normalize the list,, but it is simple to write this function
    # ourselves
    for i in range(0, number_of_entry):

        normalized_tmp = float(input_list[i]/average_no_extreme)
        normalized_list.append(normalized_tmp)

        # after normalization, normalized value shall be not completely out of range
        # the value can be small or ZERO, but can NOT be too large
        assert(normalized_tmp <1000)

    return average_no_extreme, normalized_list

# plot three index on the same plot
def plot_index_distribution(index_1_list,  index_2_list, index_3_list, xlabel_str, category_and_product_str):

    index_1_list = np.array(index_1_list)
    index_2_list = np.array(index_2_list)
    index_3_list = np.array(index_3_list)

    index_1_len = len(index_1_list)
    index_2_len = len(index_2_list)
    index_3_len = len(index_3_list)
    assert(index_1_len == index_2_len)
    assert(index_1_len == index_3_len)

    x_array =range(0, index_1_len)

    title_str = 'Asia Marketing Comparing: %s' % (category_and_product_str)

    fig = plt.figure()
    p1, = plt.plot(x_array, index_1_list, '-bo')
    plt.ion()
    plt.ylabel('Media Index')
    plt.grid(True)
    p2, =  plt.plot(x_array, index_2_list, '-g^')
    p3, =  plt.plot(x_array, index_3_list, '-rs')
    plt.legend([p1, p2, p3], ["China Media Index", "Asia Media Index", "Japan Media Index"])
    plt.xlabel(xlabel_str)
    plt.title(title_str)
    plt.show()
    plt.draw()
    image_file_name='%s.png'%(category_and_product_str)
    fig.savefig(image_file_name, dpi=fig.dpi)

    tmp = 100

# plot index distribution
def plot_correlation_of_index(index_1_list,  index_2_list, index_3_list):

    plt.figure()
    pa, = plt.plot(index_1_list, index_2_list, linestyle='None', marker="*")
    plt.title('Correlation of China Marketing vs. Asia Marketing ')
    plt.ylabel('Media Index')
    plt.grid(True)
    plt.draw()

    plt.show()

    tmp = 100

# plot media index distribution
def plot_media_index_distribution( media_index_list, xlabel_str, category_and_product_str ):

    media_index_list = np.array( media_index_list)
    print media_index_list

    media_index_len = len(media_index_list)

    x_array =range(0, media_index_len)

    title_str = 'China Marketing Media Comparing: %s' % (category_and_product_str)
    plt.figure()
    p1, = plt.plot( x_array, media_index_list, 'bo-')
    #plt.ion()
    plt.ylabel('Media Index')
    plt.xlabel(xlabel_str)
    plt.grid(True)
    plt.legend([p1], ['China Media Index'])
    plt.title(title_str)
    plt.draw()

    tmp = 100

def EDA_vendor_Asia_media_comparing():

    # media_weighted_factor_file
    media_weight_factor_file = 'media_weighted_factor_utf8.txt'

    # Testing for EDA vendors
    # in_file_name ='eda_companies_out_pcb_utf8.txt'
    in_file_name ='output/eda_companies/eda_companies_out_pcb_v2_utf8.txt'
    out_file_name ='output/eda_companies/eda_companies_out_pcb_v2_normalized_utf8.txt'

    china_media_index_ave, asia_media_index_ave, japan_media_index_ave, china_media_index_list, japan_media_index_list, asia_media_index_list = process_raw_data(in_file_name, out_file_name, media_weight_factor_file)

    xlable_str = 'Vendor Index, 0: Mentor, 1, Cadence, 2: Synopsys, 3: PDF, 4: Altium, 5: Zuken, 6: ASM'
    category_and_product_str = 'PCB Product for EDA Vendors'
    plot_media_index_distribution( china_media_index_list, xlable_str, category_and_product_str)
    plot_index_distribution(china_media_index_list,  asia_media_index_list, japan_media_index_list, xlable_str, category_and_product_str)

def CSU_MBA_Program_Asia_Media_index_comparing():

    # media_weighted_factor_file
    media_weight_factor_file = 'media_weighted_factor_utf8.txt'

    # Testing for California State Univ MBA
    in_file_name ='output/csu/csu_school_out_mba_utf8.txt'
    out_file_name ='output/csu/csu_school_out_mba_normalized_utf8.txt'

    china_media_index_ave, asia_media_index_ave, japan_media_index_ave, china_media_index_list, japan_media_index_list, asia_media_index_list = process_raw_data(in_file_name, out_file_name, media_weight_factor_file)

    xlable_str = '0:CSUM, 1:Calpoly, 2:Ponoma, 3:CSUB, 4:CSUCI, 5:Chico, 6:CSUDH, 7:East Bay\n \
                8:Fresno, 9:CSUMB, 10:CSULB, 11:LA, 12: CSUMB, 13: CSUN, 14:CSUS, 15: CSUSB, 16:CSUSM, 17:CSUStan, 18:Humboldt, \n \
                19:SDSU, 20:SFSU, 21:SJSU, 22:Sonoma'

    category_and_product_str = 'California State Univ MBA Program'

    plot_media_index_distribution( china_media_index_list, xlable_str, category_and_product_str)
    plot_index_distribution(china_media_index_list,  asia_media_index_list, japan_media_index_list, xlable_str, category_and_product_str)

def Travel_Destination_Asia_Media_index_comparing():

    # media_weighted_factor_file
    media_weight_factor_file = 'media_weighted_factor_utf8.txt'

    # Testing for California State Univ MBA
    in_file_name ='output/travel_destination/travel_destination_out_travel_utf8.txt'
    out_file_name ='output/travel_destination/travel_destination_out_travel_normalized_utf8.txt'

    china_media_index_ave, asia_media_index_ave, japan_media_index_ave, china_media_index_list, japan_media_index_list, asia_media_index_list = process_raw_data(in_file_name, out_file_name, media_weight_factor_file)

    xlable_str = '0:Hawaii, 1:CA, 2:Phuket, 3:Maldives, 4:Jeju-do, 5:Bali, 6:Washington DC, 7:NY, 8:LA, 9:USA'

    category_and_product_str = 'Destination Travel'

    plot_media_index_distribution( china_media_index_list, xlable_str, category_and_product_str)
    plot_index_distribution(china_media_index_list,  asia_media_index_list, japan_media_index_list, xlable_str, category_and_product_str)

def earphone_vendor_Asia_Media_index_comparing():

    # media_weighted_factor_file
    media_weight_factor_file = 'media_weighted_factor_utf8.txt'

    # Testing for California State Univ MBA
    in_file_name ='output/earphone/earphone_vendors_out_earphone_utf8.txt'
    out_file_name ='output/earphone/earphone_vendors_out_earphone_normalized_utf8.txt'

    china_media_index_ave, asia_media_index_ave, japan_media_index_ave, china_media_index_list, japan_media_index_list, asia_media_index_list = process_raw_data(in_file_name, out_file_name, media_weight_factor_file)

    xlable_str = '0:Beats, 1:Audio-Technica, 2:Sennheiser, 3:Bose'

    category_and_product_str = 'Ear Phone Vendor'

    plot_media_index_distribution( china_media_index_list, xlable_str, category_and_product_str)
    plot_index_distribution(china_media_index_list,  asia_media_index_list, japan_media_index_list, xlable_str, category_and_product_str)


if __name__=='__main__':

    EDA_vendor_Asia_media_comparing()

    #CSU_MBA_Program_Asia_Media_index_comparing()

    #Travel_Destination_Asia_Media_index_comparing()

    #earphone_vendor_Asia_Media_index_comparing()

    plt.show()

    tmp = 100