from django.db.models import Max, Avg
import json
import re
from schools.models import School, SchoolInforYearly, BaiduIndexCh, BaiduIndexEn, BaiduNewsEn,\
    BaiduNewsCh, BaiduSite, GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp, CompositeIndex
    
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
    return result_set # not a dict of School objs but of selected fields of School objs

def filter_by_keyword(result_set, keyword):
    results = []
#     remove_list = ['University', 'of', 'College', 'Institute', 'State'] # words to ignore
    for school in result_set:
#         school_keywords = re.split("[, ]", school['school__name']) # split the keyword using ',' and ' '
#         for word in remove_list: # remove meaningless words defined in remove_list
#             try:
#                 school_keywords.remove(word)
#             except:
#                 pass
#             
#             # select schools whose keywords start with the input text
#         for word in school_keywords:
#             if word.lower().startswith(keyword):
#                 results.append(school)
        if keyword.lower() in school['school__name'].lower():
            #print school['school__name']
            results.append(school)
    #print results
    return results
        
def get_latest_indexes_for_school_view(school):
    result_set = [None] * 12
    latest_date = BaiduIndexCh.objects.aggregate(Max('date'))['date__max']
    latest_date = latest_date.strftime('%Y-%m-%d') # convert to xxxx-xx-xx format string
    result_set[0] = ['Indexes on Major Search Engines', 
                     'Index of ' + school.name, 
                     'Max Index of All Schools',
                     'Average Index of All Schools']
    result_set[1] = ['baidu_index_ch', 
                     float(school.baiduindexch_set.latest('date').index), 
                     float(BaiduIndexCh.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(BaiduIndexCh.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[2] = ['baidu_index_en', 
                     float(school.baiduindexen_set.latest('date').index), 
                     float(BaiduIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(BaiduIndexEn.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[3] = ['baidu_news_ch', 
                     float(school.baidunewsch_set.latest('date').index), 
                     float(BaiduNewsCh.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(BaiduNewsCh.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[4] = ['baidu_news_en', 
                     float(school.baidunewsen_set.latest('date').index), 
                     float(BaiduNewsEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(BaiduNewsEn.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[5] = ['baidu_site', 
                     float(school.baidusite_set.latest('date').index), 
                     float(BaiduSite.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(BaiduSite.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[6] = ['google_index_en', 
                     float(school.googleindexen_set.latest('date').index), 
                     float(GoogleIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(GoogleIndexEn.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[7] = ['google_index_hk', 
                     float(school.googleindexhk_set.latest('date').index), 
                     float(GoogleIndexHk.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(GoogleIndexHk.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[8] = ['google_news', 
                     float(school.googlenews_set.latest('date').index), 
                     float(GoogleNews.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(GoogleNews.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[9] = ['google_site', 
                     float(school.googlesite_set.latest('date').index), 
                     float(GoogleSite.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(GoogleSite.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[10] = ['yahoojap_index_en', 
                     float(school.yahoojapindexen_set.latest('date').index), 
                     float(YahoojapIndexEn.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(YahoojapIndexEn.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    result_set[11] = ['yahoojap_index_jp', 
                     float(school.yahoojapindexjp_set.latest('date').index), 
                     float(YahoojapIndexJp.objects.filter(date=latest_date).aggregate(Max('index'))['index__max']),
                     float(YahoojapIndexJp.objects.filter(date=latest_date).aggregate(Avg('index'))['index__avg'])]
    return json.dumps(result_set[:-2])

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

# get google index for school in the period of last num_days days
def get_gg_index(school_id, num_days):
    gg = [None] * 4
    gg[0] = GoogleIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg index en
    gg[1] = GoogleIndexHk.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg index hk
    gg[2] = GoogleNews.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg news
    gg[3] = GoogleSite.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg site
    return [[a, b, c, d] for a, b, c, d in zip(gg[0], gg[1], gg[2], gg[3])]
    
# get baidu index for school in the period of last num_days days
def get_bd_index(school_id, num_days):
    bd = [None] * 5
    bd[0] = BaiduIndexCh.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd index ch
    bd[1] = BaiduIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd index en
    bd[2] = BaiduNewsCh.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd news ch
    bd[3] = BaiduNewsEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd news en
    bd[4] = BaiduSite.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd site
    return [[a, b, c, d, e] for a, b, c, d, e in zip(bd[0], bd[1], bd[2], bd[3], bd[4])]
        
# get yahoo index for school in the period of last num_days days
def get_yh_index(school_id, num_days):
    yh = [None] * 2
    yh[0] = YahoojapIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # yh index en
    yh[1] = YahoojapIndexJp.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # yh index jp
    return [[a, b] for a, b in zip(yh[0], yh[1])]
    
# get all indexes of selected period for a School
def get_all_indexes(school_id, num_days):
    indexes = [None] * 11
    indexes[0] = GoogleIndexEn.objects.filter(school=school_id).order_by('-date')[:num_days] # gg index en
    indexes[1] = GoogleIndexHk.objects.filter(school=school_id).order_by('-date')[:num_days] # gg index hk
    indexes[2] = GoogleNews.objects.filter(school=school_id).order_by('-date')[:num_days] # gg news
    indexes[3] = GoogleSite.objects.filter(school=school_id).order_by('-date')[:num_days] # gg site
    indexes[4] = BaiduIndexCh.objects.filter(school=school_id).order_by('-date')[:num_days] # bd index ch
    indexes[5] = BaiduIndexEn.objects.filter(school=school_id).order_by('-date')[:num_days] # bd index en
    indexes[6] = BaiduNewsCh.objects.filter(school=school_id).order_by('-date')[:num_days] # bd news ch
    indexes[7] = BaiduNewsEn.objects.filter(school=school_id).order_by('-date')[:num_days] # bd news en
    indexes[8] = BaiduSite.objects.filter(school=school_id).order_by('-date')[:num_days] # bd site
    indexes[9] = YahoojapIndexEn.objects.filter(school=school_id).order_by('-date')[:num_days] # yh index en
    indexes[10] = YahoojapIndexJp.objects.filter(school=school_id).order_by('-date')[:num_days] # yh index jp
    return indexes

# get specific index of selected period for a School 
def get_index(school_id, index_name, num_days):
    if index_name == 'composite_index':
        return CompositeIndex.objects.filter(school=school_id).order_by('-date')[:num_days] # bd index en
    if index_name == 'bd_index_en' :
        return BaiduIndexEn.objects.filter(school=school_id).order_by('-date')[:num_days] # bd index en
    if index_name == 'bd_index_ch' :
        return BaiduIndexCh.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'bd_news_en' :
        return BaiduNewsEn.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'bd_news_ch' :
        return BaiduNewsCh.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'bd_site' :
        return BaiduSite.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'gg_index_en' :
        return GoogleIndexEn.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'gg_index_hk' :
        return GoogleIndexHk.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'gg_news_en' :
        return GoogleNews.objects.filter(school=school_id).order_by('-date')[:num_days]
    if index_name == 'gg_site' :
        return GoogleSite.objects.filter(school=school_id).order_by('-date')[:num_days]
    
# convert list per school to list per chart
def convert_to_chart_data(list_per_school):
    list_for_chart = []
    for i in range(0, len(list_per_school[0])):
        temp_list = []
        for j in range(0, len(list_per_school)):
            temp_list.append(list_per_school[j][i])
        list_for_chart.append(temp_list)

    list_per_chart = []
    for one_list in list_for_chart:
        list_for_day = []
        for i in range(0, len(one_list[0])):
            list_per_day = []
            for j in range(0, len(one_list)):
                list_per_day.append(one_list[j][i])
            list_for_day.append(list_per_day)
        list_per_chart.append(list_for_day)
    
#     for elem in list_per_chart:
#         print elem
            
    return list_per_chart

def convert_to_chart_data_index(list_per_school):
    list_per_day = []
    for i in range(len(list_per_school[0])):
        one_list = []
        for j in range(len(list_per_school)):
            one_list.append(list_per_school[j][i])
        list_per_day.append(one_list)
    return list_per_day
def get_data_col(school_ids):
    schools = []
    for id in school_ids: # get all indexes of a school
        id = int(id)
        schools.append(get_all_indexes(id, 1)[:-2])

    # group indexes by src for a list of schools
    data_sets = []
    for i in range(len(schools[0])):
        one_set = []
        one_set.append(['School', 'Index'])
        for j in range(len(schools)):
            print schools[j][i][0].school.name
            one_set.append([schools[j][i][0].school.name.encode('ascii','ignore') + '', float(schools[j][i][0].index)])
        print one_set
        data_sets.append(one_set)
    #print data_sets
    return data_sets
        
def get_index_data_col(school_ids, index_name):
    data_set = []
    data_set.append(['School', 'Index'])
    for id in school_ids:
        school_id = int(id)
        #print float(get_index(school_id, index_name, 1)[0].index)
        data_set.append([School.objects.get(id=school_id).name.encode('ascii','ignore'), 
                         float(get_index(school_id, index_name, 1)[0].index)])
    return data_set