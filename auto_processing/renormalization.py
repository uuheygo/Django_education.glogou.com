# NOTE_1: To run the script of this file, the index tables in the database shall already have my_index_re columns.
#        This maybe done with django migration tool. If the tool does not work, then try to run database_change.sql
#
# NOTE_2: renormalization is a method used in physics, particularly in quantum field theory and statistical mechanics.
# In this file, renormalization means that we apply non-uniform quantization to the normalized data. This process can
# be considered as "re-normalization".
#
# NOTE_3: Following the spirit of renormalization methods in physics, the "non-uniform" quantization methods we use
# can be considered as a special type of "regularization".
#
#  NOTE_4, the methods we calculte  composite index after "re-normalization" need further investigation (7/1/2015)
#
from  data_quantization import non_uniform_quantization
import MySQLdb

# Update the database with renormalized index.
# NOTE: the table composite_index may need special handling.
def update_db_with_renormlized_index():

    host_ip = 'localhost'

    conn = MySQLdb.connect(host = host_ip,
                       user = 'mediaWatch',
                       passwd = 'Morefruit2013',
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)

    update_index_table_with_renormalized_index(conn, 'baidu_index_ch')
    update_index_table_with_renormalized_index(conn, 'baidu_index_en')
    update_index_table_with_renormalized_index(conn, 'baidu_news_ch')
    update_index_table_with_renormalized_index(conn, 'baidu_news_en')
    update_index_table_with_renormalized_index(conn, 'baidu_site')
    update_index_table_with_renormalized_index(conn, 'google_index_en')
    update_index_table_with_renormalized_index(conn, 'google_index_hk')
    update_index_table_with_renormalized_index(conn, 'google_news')
    update_index_table_with_renormalized_index(conn, 'google_site')
    update_index_table_with_renormalized_index(conn, 'yahoojap_index_en')
    update_index_table_with_renormalized_index(conn, 'yahoojap_index_jp')

    ## __FXI_ME__, renormalize table composite_index need special handling, but
    # we do it in this way at this moment just for quick testing purpose..
    update_index_table_with_renormalized_index(conn, 'composite_index')

# Update one index table with renormalized index
# __FIX_ME__, this function update each record with one SQL statement, 
# this must not be right. We shall be able to update entire column with one sql statement.
# Since this function is excuated offline, it is OK to be slow at this moment.
def update_index_table_with_renormalized_index(conn, table_name):

    x = conn.cursor()

    retrieve_index_st = 'select my_index, id from %s'%(table_name)
    x.execute(retrieve_index_st)
    results = x.fetchall()

    cnt = 0
    for row in results:

        my_index = row[0]
        id = row[1]

        my_index_re = non_uniform_quantization(my_index)
        update_statement = 'update %s set my_index_re = %20.7f where id = %d'%(table_name, my_index_re, id)
        print update_statement

        try:
            x.execute(update_statement)
        except MySQLdb.Error, e:
            print "query failed"
            print e

        # __FIX_ME__, It was said that the SQL statement used in above is NOT safe, prone to
        # SQL injection attack, the following will be safer, somehow, I could not get it work, not sure why.
        #ret = x.execute("""update %s set my_index_re = %20.7f where id = %d""", (table_name, float(my_index_re), id))

        cnt += 1

    # Commit the database change
    try:
        conn.commit()
    except MySQLdb.Error, e:
        print "commit failed"
        print e

    print '\n====== %s, Total row changed: %d'%(table_name, cnt)

### ============================================================================================
# main script for offline updating the existing table with renormalized index.
update_db_with_renormlized_index()