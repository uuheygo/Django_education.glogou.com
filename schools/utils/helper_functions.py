from django.db.models import Max
import json
import re
from schools.models import School, SchoolInforYearly, BaiduIndexCh, BaiduIndexEn, BaiduNewsEn,\
    BaiduNewsCh, BaiduSite, GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp
    
latest_year = SchoolInforYearly.objects.aggregate(Max('year'))['year__max']

def get_result_set(state, rank_range):
    # get all schools: id, rank, name, state, cost, population
    all_schools = SchoolInforYearly.objects.filter(year=latest_year).values('school__id', 'overall_rank', 
                                                           'school__name', 'school__state_short',
                                                           'annual_cost', 'student_population').order_by('overall_rank')
                                                           
    if state == 'All states' and rank_range == 'All':
        result_set = all_schools
    elif state == 'All states' and rank_range != 'All':
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_schools.filter(overall_rank__lte=end, overall_rank__gte=start)
    elif rank_range == 'All':
        result_set = all_schools.filter(school__state_short=state)
    else:
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_schools.filter(overall_rank__lte=end, overall_rank__gte=start, \
                                        school__state_short=state)
    return result_set

def filter_by_keyword(result_set, keyword):
    results = []
    remove_list = ['University', 'of', 'College', 'Institute', 'State'] # words to ignore
    for school in result_set:
        school_keywords = re.split("[, ]", school['school__name']) # split the keyword using ',' and ' '
        for word in remove_list: # remove meaningless words defined in remove_list
            try:
                school_keywords.remove(word)
            except:
                pass
            
            # select schools whose keywords start with the input text
        for word in school_keywords:
            if word.lower().startswith(keyword):
                results.append(school)
    return results
        
def get_latest_indexes_for_school_view(school):
    result_set = [None] * 12
    latest_date = BaiduIndexCh.objects.aggregate(Max('date'))['date__max']
    latest_date = latest_date.strftime('%Y-%m-%d') # convert to xxxx-xx-xx format string
    result_set[0] = ['Indexes on Major Search Engines', 'Index of ' + school.name, 'Max Index of All Schools']
    result_set[1] = ['baidu_index_ch', float(school.baiduindexch_set.latest('date').index), 
                     float(BaiduIndexCh.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[2] = ['baidu_index_en', float(school.baiduindexen_set.latest('date').index), 
                     float(BaiduIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[3] = ['baidu_news_ch', float(school.baidunewsch_set.latest('date').index), 
                     float(BaiduNewsCh.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[4] = ['baidu_news_en', float(school.baidunewsen_set.latest('date').index), 
                     float(BaiduNewsEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[5] = ['baidu_site', float(school.baidusite_set.latest('date').index), 
                     float(BaiduSite.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[6] = ['google_index_en', float(school.googleindexen_set.latest('date').index), 
                     float(GoogleIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[7] = ['google_index_hk', float(school.googleindexhk_set.latest('date').index), 
                     float(GoogleIndexHk.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[8] = ['google_news', float(school.googlenews_set.latest('date').index), 
                     float(GoogleNews.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[9] = ['google_site', float(school.googlesite_set.latest('date').index), 
                     float(GoogleSite.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[10] = ['yahoojap_index_en', float(school.yahoojapindexen_set.latest('date').index), 
                     float(YahoojapIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    result_set[11] = ['yahoojap_index_jp', float(school.yahoojapindexjp_set.latest('date').index), 
                     float(YahoojapIndexJp.objects.filter(date=latest_date).aggregate(Max('index'))['index__max'])]
    return json.dumps(result_set)

def get_race_percentages(school_infor):
    race_per = [-1]*8
    if school_infor.enroll_americanindiannative_percentage is not None:
        race_per[0] = int(school_infor.enroll_americanindiannative_percentage[:-1])
    if school_infor.enroll_asian_pacific_percentage is not None:
        race_per[1] = int(school_infor.enroll_asian_pacific_percentage[:-1])
    if school_infor.enroll_black_percentage is not None:
        race_per[2] = int(school_infor.enroll_black_percentage[:-1])
    if school_infor.enroll_latino_percentage is not None:
        race_per[3] = int(school_infor.enroll_latino_percentage[:-1])
    if school_infor.enroll_white_percentage is not None:
        race_per[4] = int(school_infor.enroll_white_percentage[:-1])
    if school_infor.enroll_towormoreraces_percentage is not None:
        race_per[5] = int(school_infor.enroll_towormoreraces_percentage[:-1])
    if school_infor.enroll_raceunknown_percentage is not None:
        race_per[6] = int(school_infor.enroll_raceunknown_percentage[:-1])
    if school_infor.enroll_nonresidentalien_percentage is not None:
        race_per[7] = int(school_infor.enroll_nonresidentalien_percentage[:-1])
    return race_per