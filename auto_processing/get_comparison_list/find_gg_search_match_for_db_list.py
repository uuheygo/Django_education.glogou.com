'''
Created on Apr 18, 2015

@author: Lu Peng

What: After getting the list of schools for comparison from google, 
relate each school to the id in db (school name may be different).

How: 1. search school on google and from the first entry get the url
     2. match result from both table to get the id
'''
import re
import urllib2
from bs4 import BeautifulSoup
import mechanize
from time import sleep
import MySQLdb

from _mysql_exceptions import Error
# create connection to 'mediawatch_lu'
conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

# search result is id = 'rso', 'li' s are result entry
# find 'a' in first 'li', 'data-href' is the url
def match_id():
    # from the comparison list get all unique schools and save in file
    x.execute('select id, name from school')
    all_schools = x.fetchall()
    print all_schools # all unique schools in comparison list
    print len(all_schools)
#    assert False
#     # print out the failed school names
#     f_error = open('error_list.txt', 'r')
#     for line in f_error.readlines():
#         print all_schools[int(line)-1]
#     assert False
    
    # search google for url of each school
    br = mechanize.Browser()
    br.set_handle_robots(False)     # ignore robots
    br.set_handle_refresh(False)    # can sometimes hang without this
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
    url = "http://www.google.com"
    search_box='q'
    
    #f_write = open('gg_search_match_db_list.txt', 'w')
    #f_exception = open('error_list.txt', 'w')
    count = 0
    
    for school in all_schools:
    #for school in ['Mentor graphics']:
        try:
            br = mechanize.Browser()
            br.set_handle_robots(False)     # ignore robots
            br.set_handle_refresh(False)    # can sometimes hang without this
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
            url = "http://www.google.com"
            search_box='q'
            
            br.open(url)
            htmlFile = br.response()
            br.select_form(nr=0)
            br.form[search_box] = school[1]
    
            response = br.submit()
            response_html = response.get_data()
            print response_html
            #print response_html
            soup = BeautifulSoup(response)
            target = soup.find('div', {'id': 'ires'}).find('span', {'class': 'nobr'})
            print count, target.text
            count += 1
            bs_html = soup.body.prettify(encoding='utf-8')
            #print bs_html
#             f_write.write(str(school[0]) + '\t' + school[1] + '\t' + target.text + '\n')
#             f_write.flush()
#             if count % 50 == 0:
#                 sleep(5)
        except Exception, Error:
            #print Exception, Error
            print count, school[0], school[1]
            pass
            
    #f_write.close()
    #f_exception.close()
if __name__ == '__main__':
    match_id()








