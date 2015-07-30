#!/usr/bin/python

'''
Created on May 17, 2015
@author: lu

Note 1: This program collects index information according to a list.
At this moment, the list is saved in a file, f_schools = ''school_info.csv'.
This can be changed to other list, so that this program can collect data for other list.

Note 2: The collected data will be saved to text files 1st, then, they will be processed. Normalized index
        (and renormalized index) will be saved to databases.

Note 3: At this moment, this program runs on data collection server, so it will import indexes to three
        different server, glogou production server, glogou backup server and local server.

Note 4: To test this code on person computer, if you do not want to run complete list, one can
        search __HARD_CODING_TESTING_PURPOSE__ in the following and make necessary changes.
'''

import sys
import os
os.chdir("/home/dev/crawling_lu/auto_processing")           # __CHANGE__THIS if run on person computer
f_schools = 'school_info.csv'

#f_schools = 'school_info_short.csv'                                # __HARD_CODING_TESTING_PURPOSE__

from crawl_bd_gg import crawl_search_counts
from calculate_index import calculate_indexes
from import_db import import_to_db
from renormalization import update_db_with_renormlized_index

print 'starting to crawl: %s'%(f_schools)
# return a file name which contains the "raw, un-processed "crawled results.
# the name of the file which contains the crawled results.
# The name file contains time stamp, in the following way: 'success_2015_06_04_09_00_03'
# The error was log in 'error_2015_06_04_09_00_03'
try:
    f_counts = crawl_search_counts(f_schools)
except:
    print 'crawl has error for %s'%(f_schools)

# Sometimes, crawling is not complete, only data has only crawled for some schools, not all schools.
# but following step can still continue.

# f_counts = 'success_2015_07_23_16_19_23'                          # __HARD_CODING_TESTING_PURPOSE__
# f_counts = 'success_2015_07_27_23_44_39'                       # __HARD_CODING_TESTING_PURPOSE__

print 'starting to calculate index: %s'%(f_counts)
# return four file names,
#         a file name of normalized index,
#         a file name of composite index,
#         a file name of renormalized index,
#         a file name of renormalized composite index calculated with simple algorithm,
#
# the name of the file contains the time stamps
# For example:
#         the file name for normalized index will be: indexes_2015_07_09_09_00_02
#         the file name for composite index will be: composite_index_2015_07_09_09_00_02
#         the file name for renormalized index will be: indexes_re_2015_07_09_09_00_02
#         the file name for renormlized composite index will be: composite_re_index_2015_07_09_09_00_02
f_indexes, f_composite_indexes, f_indexes_re, f_composite_indexes_re = calculate_indexes(f_counts)

print 'starting to write to database'

#f_indexes = 'indexes_2015_06_04_09_00_03'
#f_composite_indexes = 'composite_index_2015_06_04_09_00_03'
date = '-'.join(f_indexes.split('_')[1:4])
print '++++++++++' + date + '+++++++++++'
print ''
print 'index files: ' + f_indexes, f_composite_indexes, f_indexes_re, f_composite_indexes_re
print ''

# import data to glogou_production_server
try:
    import_to_db('www.glogou.com', f_composite_indexes, f_indexes, f_composite_indexes_re, f_indexes_re, date)

    print date, 'www.glogou.com task successful'
except Exception:
    print sys.exc_info(), 'www.glogou.com failed'
print ''

# import data to localhost
try:
    import_to_db('localhost', f_composite_indexes, f_indexes,  f_composite_indexes_re,  f_indexes_re,  date) # localhost

    print date, 'localhost task successful'
except Exception:
    print sys.exc_info(), 'localhost failed'
print ''

# import data to glogou_backup_server
try:
    import_to_db('www.glogou.us', f_composite_indexes, f_indexes,  f_composite_indexes_re,  f_indexes_re, date)

    print date, 'www.glogou.us task successful'
except Exception:
    print sys.exc_info(), 'www.glogou.us failed'
print ''

print '++++++++++' + date + '+++++++++++'

