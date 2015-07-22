import MySQLdb

# 'baidu_index_ch','baidu_index_en', 'baidu_news_ch', 'baidu_news_en', 
#              'baidu_site', 'google_index_en', 'google_index_hk', 'google_news', 
#              'google_site', 'yahoojap_index_en', 'yahoojap_index_jp'

def import_google_index_en(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("INSERT INTO google_index_en (school, my_index, my_date) VALUES (%s, %s, '%s')" 
                  % (entry[0], entry[1], date))
        
def import_google_index_hk(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_index_hk (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))
        
def import_google_news(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_news (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))
        
def import_google_site(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_site (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))
        
def import_baidu_index_ch(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_index_ch (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))

def import_baidu_index_en(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_index_en (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))

def import_baidu_news_ch(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_news_ch (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))

def import_baidu_news_en(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_news_en (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))

def import_baidu_site(list_index, date, x):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_site (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))

def import_to_db(host_ip, file_composite, file_indexes, date):
    conn = MySQLdb.connect(host = host_ip,
                       user = 'mediaWatch',
                       passwd = 'Morefruit2013',
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
    x = conn.cursor()

    print host_ip, 'start importing to db...'
    with open(file_indexes, 'r') as f_input:
        # input file has 10 cols including id and 9 indexes
        list_index = [] # 9 lists of [id, index] entries
        for i in range(9):
            list_index.append([])
        for line in f_input.readlines():
            index_for_school = line.strip().split('\t')
            for i in range(9):
                list_index[i].append([index_for_school[0], index_for_school[i + 1]])
        # date = raw_input('Enter the date (eg, 2015-04-08): ')
        
        import_google_index_en(list_index[0], date, x)
        import_google_index_hk(list_index[1], date, x)
        import_google_news(list_index[2], date, x)
        import_google_site(list_index[3], date, x)
        import_baidu_index_ch(list_index[4], date, x)
        import_baidu_index_en(list_index[5], date, x)
        import_baidu_news_ch(list_index[6], date, x)
        import_baidu_news_en(list_index[7], date, x)
        import_baidu_site(list_index[8], date, x)
        conn.commit()
       
    with open(file_composite, 'r') as f_input:
        for line in f_input.readlines():
            entry = line.strip().split('\t')
            x.execute("insert into composite_index (school, my_index, my_date) VALUES ('%s', '%s', '%s')"
                  % (entry[0], entry[1], date))
        conn.commit() 
    print host_ip, 'done importing to db...'
#         do_import = raw_input('Do you want to commit import to database? y/n: ')
#         if do_import.lower() == 'y':
#             conn.commit()
#             print 'Data import successful'
#         else:
#             print 'Abort import'
        
