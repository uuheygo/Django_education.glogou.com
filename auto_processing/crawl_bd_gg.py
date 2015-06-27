# google blocking period is about 90 min


import mechanize
from time import sleep
import random
import unicodedata
import re
import sys
import codecs
import datetime
import time
from bs4 import BeautifulSoup
import string
import urllib2

def get_bd_index_all_mechanize(file_name):
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    f_error = open('errors_' + st, 'w')
    f_success = open('success_' + st, 'w')
    f_success.write('ID\tgg_index_common\tgg_hk\tgg_new\tgg_site\tbd_index_chinese\t'
                    +'bd_index_common\tbd_news_chinese\tbd_news_common\tbd_site\n')
    
    all_schools = []
    with codecs.open(file_name, 'r', 'utf-8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_schools.append(line)
    #print all_schools
    
    count =0
    # default includes all 650 schools, need to change range for testing purposes
    for school in all_schools[0:]:
        sleep(random.random() * 2)
        
        while True:
            
            nums = []
            #print school, nums
            try:
                ############################## gg
                # school names inside quotes
                if len(school) > 4:
                    target_en = "\"" + school[2] + "\" " + school[4]
                else:
                    target_en = "\"" + school[2] + "\""
                
                #target_ch = "\"" + school[3] + "\""
                site = 'site:' + school[1]
                #print target_en, site
                
                # gg search
                # en                
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com"
                search_box='q'
                
                br.open(url)
                #htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # gg hk
                # en
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com.hk"
                search_box='q'
                
                br.open(url)
                #htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                
                # gg news
                # en
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://news.google.com"
                search_box='q'
                
                br.open(url)
                #htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                
                # gg site
                site = 'site:' + school[1]
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com"
                search_box='q'
                
                br.open(url)
                #htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = site
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                ############################################### baidu
                # school name has not quotes
                if len(school) > 4:
                    target_en = school[2] + " " + school[4]
                else:
                    target_en = school[2]
                target_ch = school[3]
                target_en = string.replace(target_en, ' ', '%20')
                target_ch = string.replace(target_ch, ' ', '%20')
                #print target_ch, target_en, site
                
                while True:
                    nums_bd = []
                    try:
                        # baidu search
                        # ch
                        url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                            +target_ch
                        url = url.encode('utf8')
                        response = urllib2.urlopen(url, timeout = 10)
                        response_html = response.read()
                        soup = BeautifulSoup(response_html)
                        #bs_html = soup.body.prettify(encoding='utf-8')
                        target = soup.find('div', {'class': 'nums'})
                        all_txt = target.text
                        str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                        nums_en_index = re.findall(r'\d+', str_txt)
                        nums_bd.append(''.join(nums_en_index))
                        
                        # baidu search
                        # en
                        url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                            + target_en
                        response = urllib2.urlopen(url, timeout = 30)
                        response_html = response.read()
                        soup = BeautifulSoup(response_html)
                        #bs_html = soup.body.prettify(encoding='utf-8')
                        target = soup.find('div', {'class': 'nums'})
                        all_txt = target.text
                        str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                        nums_en_index = re.findall(r'\d+', str_txt)
                        nums_bd.append(''.join(nums_en_index))
                        
                        # baidu news
                        # ch
                        url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word='+target_ch
                        url = url.encode('utf8')
                        response = urllib2.urlopen(url, timeout = 30)
                        response_html = response.read()
                        soup = BeautifulSoup(response_html)
                        #bs_html = soup.body.prettify(encoding='utf-8')
                        target = soup.find('span', {'class': 'nums'})
                        all_txt = target.text
                        str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                        nums_en_index = re.findall(r'\d+', str_txt)
                        nums_bd.append(''.join(nums_en_index))
                        
                        
                        # baidu news
                        # en
                        url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word='+target_en
                        response = urllib2.urlopen(url, timeout = 30)
                        response_html = response.read()
                        soup = BeautifulSoup(response_html)
                        #bs_html = soup.body.prettify(encoding='utf-8')
                        target = soup.find('span', {'class': 'nums'})
                        all_txt = target.text
                        str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                        nums_en_index = re.findall(r'\d+', str_txt)
                        nums_bd.append(''.join(nums_en_index))
                        
                        # baidu site
                        url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                            + site
                        response = urllib2.urlopen(url, timeout = 30)
                        response_html = response.read()
                        soup = BeautifulSoup(response_html)
                        #bs_html = soup.body.prettify(encoding='utf-8')
                        target = soup.find('div', {'class': 'nums'})
                        all_txt = target.text
                        str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                        nums_en_index = re.findall(r'\d+', str_txt)
                        nums_bd.append(''.join(nums_en_index))
                        
                        nums += nums_bd
                        one_line = school[0] + '\t' + '\t'.join(nums)
                        f_success.write(one_line + '\n')
                        f_success.flush()
                        break
                        
                    except Exception:
                        #print sys.exc_info()[:2]
                        pass
                
                #print 'count =', count, '&&&\t', one_line + '\n'
                count += 1
                
                #if count % 10 == 0: # sleep 10 min every 10 runs 
                    #sleep(600)
                break
                
            except Exception:
                #print sys.exc_info()[:2]
                #print 'count =', count, ' &&&' + '\t'.join(school) + '\n'
                count += 1
                #if count % 10 == 0: # sleep 10 min every 10 runs 
                sleep(600) # sleep 10 min if failed
                f_error.write(school[0] + '\t' + school[2] + '\n')
                f_error.flush()
                pass
    f_error.close()
    f_success.close()
    return f_success.name
    
def crawl_search_counts(filename):
    return get_bd_index_all_mechanize(filename)
