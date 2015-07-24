import MySQLdb

#  At this moment, following individual index tables are supported.
#
# 'baidu_index_ch',
# 'baidu_index_en',
# 'baidu_news_ch',
# 'baidu_news_en',
# 'baidu_site',
# 'google_index_en',
# 'google_index_hk',
# 'google_news',
# 'google_site',
# 'yahoojap_index_en',
# 'yahoojap_index_jp'
#
# And one composite index table
# 'composite_index'

# import normalized index to the table, it will fill three column, school, my_index, my_date,
# it will leave my_index_re column empty
def import_normalized_index(table_name, list_index, date, x):

    # list_index is a list of [id, index] entries
    # where id is for school
    for entry in list_index:
        # Note, the following will receive a Warning: Data truncated for column 'my_index' because entry[0] which is the index,
        # has extra decimals
        insert_statement = "INSERT INTO %s (school, my_index, my_date) VALUES (%s, %s, '%s')" % (table_name, entry[0], entry[1], date)
        print insert_statement
        x.execute(insert_statement)

# Update an existing row of data with renormalized index. It will find the row with the same school and my_date.
def update_with_renormalized_index(table_name, list_index, date, x):

    # list_index is a list of [id, re_index] entries
    # where id is for school
    for entry in list_index:
        # Note, the following will receive a Warning: Data truncated for column 'my_index' because entry[0] which is the index,
        # has extra decimals
        update_statement ="UPDATE %s SET my_index_re = %s WHERE school = %s AND my_date = \'%s\'" % (table_name, entry[1], entry[0], date)
        print update_statement
        x.execute(update_statement)

# simple data integrity check, to verify that the following files all have same number of rows
def data_integrity_check(file_composite, file_indexes, file_composite_re, file_indexes_re):

    # the following four numbers shall be the same
    file_indexes_line_cnt = 0
    file_indexes_re_line_cnt = 0
    file_composite_line_cnt = 0
    file_composite_re_line_cnt = 0

    # the following two numbers shall be same
    file_indexes_sum = 0
    file_indexes_re_sum = 0

    # the following two numbers shall be same
    file_composite_sum = 0
    file_composite_re_sum = 0

    with open(file_indexes, 'r') as f_input:
        for line in f_input.readlines():
            file_indexes_line_cnt += 1
            index_for_school = line.strip().split('\t')
            file_indexes_sum += len(index_for_school)

    with open(file_indexes_re, 'r') as f_input:
        for line in f_input.readlines():
            file_indexes_re_line_cnt += 1
            index_for_school = line.strip().split('\t')
            file_indexes_re_sum += len(index_for_school)

    with open(file_composite, 'r') as f_input:
        for line in f_input.readlines():
            file_composite_line_cnt += 1
            index_for_school = line.strip().split('\t')
            file_composite_sum += len(index_for_school)

    with open(file_composite_re, 'r') as f_input:
        for line in f_input.readlines():
            file_composite_re_line_cnt += 1
            index_for_school = line.strip().split('\t')
            file_composite_re_sum += len(index_for_school)

    # the following four numbers shall be same
    assert(file_indexes_line_cnt == file_indexes_re_line_cnt)
    assert(file_indexes_line_cnt == file_composite_line_cnt)
    assert(file_indexes_line_cnt == file_composite_re_line_cnt)

    # the following two numbers shall be same
    assert(file_indexes_sum == file_indexes_re_sum)

    # the following two numbers shall be same
    assert(file_composite_sum == file_composite_re_sum)

# This function import the following index to database
#
# normalized index
# normalized composite index
# re-normalized index
# re-normalized composite index
#
# The function 1st write normalized index and composite index to the data,
# then it will update the row of the data with re-normalized data.
# Even though this will cause extra database access, but it makes code easier to maintain in future

def import_to_db(host_ip, file_composite, file_indexes, file_composite_re, file_indexes_re, date):

    # check the integrity of the data
    data_integrity_check(file_composite, file_indexes, file_composite_re, file_indexes_re)

    conn = MySQLdb.connect(host = host_ip,
                       user = 'mediaWatch',
                       passwd = 'Morefruit2013',
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
    x = conn.cursor()

    print host_ip, 'start importing to db...'

    # 1st step: import normalized index to the database
    with open(file_indexes, 'r') as f_input:

        #list_index will be 9 list of [id, index]
        # input file has 10 cols including id and 9 indexes
        list_index = [] # 9 lists of [id, index] entries
        for i in range(9):
            list_index.append([])
        for line in f_input.readlines():
            index_for_school = line.strip().split('\t')
            for i in range(9):
                list_index[i].append([index_for_school[0], index_for_school[i + 1]])

        import_normalized_index('google_index_en', list_index[0], date, x)
        import_normalized_index('google_index_hk', list_index[1], date, x)
        import_normalized_index('google_news', list_index[2], date, x)
        import_normalized_index('google_site', list_index[3], date, x)
        import_normalized_index('baidu_index_ch', list_index[4], date, x)
        import_normalized_index('baidu_index_en', list_index[5], date, x)
        import_normalized_index('baidu_news_ch', list_index[6], date, x)
        import_normalized_index('baidu_news_en', list_index[7], date, x)
        import_normalized_index('baidu_site', list_index[8], date, x)
        conn.commit()

    # 2nd step: import normalized composite index to the database
    with open(file_composite, 'r') as f_input:
        list_index = [] # a list of [id, index] entries
        for line in f_input.readlines():
            entry = line.strip().split('\t')
            list_index.append([entry[0], entry[1]])

        import_normalized_index('composite_index', list_index, date, x)
        conn.commit()

    # 3rd step: update row with re-normalized data
    with open(file_indexes_re, 'r') as f_input:

        #list_index will be 9 list of [id, re_index]
        # input file has 10 cols including id and 9 re_indexes
        list_index = [] # 9 lists of [id, re_index] entries
        for i in range(9):
            list_index.append([])
        for line in f_input.readlines():
            index_for_school = line.strip().split('\t')
            for i in range(9):
                list_index[i].append([index_for_school[0], index_for_school[i + 1]])

        # update the existing row of data with re-normalized index
        update_with_renormalized_index('google_index_en', list_index[0], date, x)
        update_with_renormalized_index('google_index_hk', list_index[1], date, x)
        update_with_renormalized_index('google_news', list_index[2], date, x)
        update_with_renormalized_index('google_site', list_index[3], date, x)
        update_with_renormalized_index('baidu_index_ch', list_index[4], date, x)
        update_with_renormalized_index('baidu_index_en', list_index[5], date, x)
        update_with_renormalized_index('baidu_news_ch', list_index[6], date, x)
        update_with_renormalized_index('baidu_news_en', list_index[7], date, x)
        update_with_renormalized_index('baidu_site', list_index[8], date, x)
        conn.commit()

    # 4th step: import renormalized composite index to the database
    with open(file_composite_re, 'r') as f_input:

        list_index = [] # a list of [id, index] entries
        for line in f_input.readlines():
            entry = line.strip().split('\t')
            list_index.append([entry[0], entry[1]])

        update_with_renormalized_index('composite_index', list_index, date, x)
        conn.commit()

    print host_ip, 'done importing to db...'

#         do_import = raw_input('Do you want to commit import to database? y/n: ')
#         if do_import.lower() == 'y':
#             conn.commit()
#             print 'Data import successful'
#         else:
#             print 'Abort import'
        
