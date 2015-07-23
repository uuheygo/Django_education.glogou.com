'''
Created on Apr 14, 2015

@author: Lu Peng

What: get a list of school for comparison with a specified school

How: 1. google search the specified school
     2. in the result page, get the schools in the section "People also search for" on the bottom right panel
'''

# SUNY, Buffalo (University at Buffalo): google not returning right page

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
import sys
import io
from selenium.webdriver.support.expected_conditions import presence_of_element_located


browser = webdriver.Firefox()
# create connection to 'mediawatch_lu'
conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediawatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediawatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()



def get_list_of_school_for_comparison(target_schools):
    
    f = io.open('school_failed.txt', 'w', encoding='utf8') # store failed school
    f_compare = io.open('school_list_comparison.txt', 'w', encoding='utf8') # store list of schools for comparison
    
    for target_school in target_schools:
        school_id = int(target_school[0])
        try:
            school_name = unicode(target_school[1], 'UTF-8') # unicode issues
        except:
            school_name = target_school[1]
        #school_name = target_school[1]
        print school_id, repr(school_name)
        
        # find the section "people also search for"
        try:
            # get the the search result page
            browser.get('https://www.google.com/')
            search_box = browser.find_element_by_id('lst-ib')
            print search_box
            search_box.send_keys(school_name + '\n')
            
            # load the search result page and find the link to list of schools for comparison
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "rhs_block")));
            
            link = browser.find_element_by_xpath("//*[contains(text(), 'People also search for')]")
            if not link.is_displayed(): # some school the link is hiden and should click 'show more' first
                link_to_show_more = browser.find_element_by_class_name('_ubf')
                link_to_show_more.click()
                link = browser.find_element_by_xpath("//*[contains(text(), 'People also search for')]")
            
            href = link.get_attribute('href')
            print href
            link.click()
            
            # get the elements with school names from comparison
            school_group = WebDriverWait(browser, 20) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, "klcar"))) \
                .find_elements_by_class_name('klitem');
            
            # put schools in list
            schools = [elem.get_attribute('title') for elem in school_group]
            schools = '|'.join(schools) # '|' delimiter
            
#             x.execute('''insert into schools_comparison (id, school_list)
#                         values (%s, %s)
#                         ''', (school_id, schools))
#             conn.commit()
            
            line = str(school_id) + '\t' + schools
            print line
            print ''
            f_compare.write(line + '\n')
            
        except Exception, err:
            print sys.exc_info()[0]
            print school_name, 'failed'
            print ''
            f.write(str(school_id) + '\t' + school_name + '\n')
            
    f.close()
    f_compare.close()
        

if __name__ == '__main__':
    print 'options:'
    print '0 --- input from database'
    print '1 --- input from file'
    option = raw_input('Your option: ')
     
    target_schools = []
    if option == '0':
        x.execute('select id, name from school_list')
        target_schools = x.fetchall()
        
    elif option == '1':
        file_name = raw_input('Enter the file name: ')
        school_file = open(file_name, 'r')
        for line in school_file:
            if len(line) > 0:
                target_schools.append(line.rstrip().split('\t'))
        school_file.close()
    print target_schools
    
    # find comparison list for each school and write to a file
    get_list_of_school_for_comparison(target_schools)
    
    browser.close()