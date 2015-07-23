import MySQLdb

# create connection to 'mediawatch_lu'
conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

with open('search_result_comparison_list.csv', 'r') as f:
    count = 0
    for line in f.readlines():
        count += 1
        print count, line
        pair = line.strip().split('\t')
        x.execute('insert into list_phone (name, phone) values(%s, %s)', (pair[0], pair[1]))
conn.commit()