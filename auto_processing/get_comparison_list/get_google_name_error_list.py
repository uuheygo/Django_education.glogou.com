import re
import urllib2
from bs4 import BeautifulSoup
import mechanize
from time import sleep

def find_name_error_list(file_name):
#     f_read = open('comparison_list.csv', 'r')
#     regex = re.compile(r'\d+,(.+)')
#     all_schools = []
#     for line in f_read.readlines()[1:]:
#         schools = set(re.findall(regex, line)[0][1:-1].split('|'))
#         all_schools = all_schools + list(set(schools) - set(all_schools))
#     print all_schools # all unique schools in comparison list
#     print len(all_schools)
    
    f = open(file_name, 'r')
#     for line in f.readlines():
#         print all_schools[int(line)-1]
#     assert False
    
    all_schools = []
    for line in f.readlines():
        all_schools.append(line)
    print all_schools
    #assert False
    count = 0
    for school_name in all_schools:
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
            br.form[search_box] = school_name
    
            response = br.submit()
            response_html = response.get_data()
            #print response_html
            soup = BeautifulSoup(response)
            target = soup.find('div', {'id': 'ires'}).find('span', {'class': 'nobr'})
            #print count, target.text
            count += 1
#            bs_html = soup.body.prettify(encoding='utf-8')
            print target.text
        except Exception, Error:
            print count
            pass
    
if __name__ == '__main__':
    file_name = raw_input('Enter the error list file name: ')
    find_name_error_list(file_name)