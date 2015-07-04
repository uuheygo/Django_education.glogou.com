from django.db.models import Max, Avg
import json
import re
from brands.models import Brand, BrandInforYearly, br_BaiduIndexCh, br_BaiduIndexEn, br_BaiduNewsEn,\
    br_BaiduNewsCh, br_BaiduSite, br_GoogleIndexEn, br_GoogleIndexHk, br_GoogleNews, br_GoogleSite,\
    br_YahoojapIndexEn, br_YahoojapIndexJp, br_CompositeIndex, g_USE_INDEX_OR_INDEX_RE

latest_year = BrandInforYearly.objects.aggregate(Max('year'))['year__max']

def get_result_set(state, rank_range):
    # get all brands: id, rank, name, state, cost, population
    all_brands = BrandInforYearly.objects.filter(year=latest_year).values('brand__id', 'overall_rank',
                                                           'brand__name', 'brand__state_short',
                                                           'annual_cost', 'student_population').order_by('overall_rank')

    if state == 'All states' and rank_range == 'All':
        result_set = all_brands
    elif state == 'All states' and rank_range != 'All':
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_brands.filter(overall_rank__lte=end, overall_rank__gte=start)
    elif rank_range == 'All':
        result_set = all_brands.filter(brand__state_short=state)
    else:
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_brands.filter(overall_rank__lte=end, overall_rank__gte=start, \
                                        brand__state_short=state)
    return result_set # not a dict of Brand objs but of selected fields of Brand objs

def filter_by_keyword(result_set, keyword):
    results = []
#     remove_list = ['University', 'of', 'College', 'Institute', 'State'] # words to ignore
    for brand in result_set:
#         brand_keywords = re.split("[, ]", brand['brand__name']) # split the keyword using ',' and ' '
#         for word in remove_list: # remove meaningless words defined in remove_list
#             try:
#                 brand_keywords.remove(word)
#             except:
#                 pass
#             
#             # select brands whose keywords start with the input text
#         for word in brand_keywords:
#             if word.lower().startswith(keyword):
#                 results.append(brand)
        if keyword.lower() in brand['brand__name'].lower():
            #print brand['brand__name']
            results.append(brand)
    #print results
    return results
        
def get_latest_indexes_for_brand_view(brand_id, index_category='general'):
    brand = Brand.objects.get(id=brand_id)
    result_set = [None] * 10
    if index_category == 'general':
        latest_date = br_BaiduIndexCh.objects.aggregate(Max('date'))['date__max']
        latest_date = latest_date.strftime('%Y-%m-%d') # convert to xxxx-xx-xx format string
        result_set[0] = ['Indexes on Major Search Engines', 
                         'Index of ' + brand.name,
                         'Max Index of All Brands',
                         'Average Index of All Brands']


        # This is needed because aggregate(Max(...)) and aggregate(Avg(...)) can NOT access through alias
        # property '.index'. For those, We have to access database column directly.
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            index_choice = 'index_no'
            index_choice_max = 'index_no__max'
            index_choice_avg = 'index_no__avg'
        else:
            index_choice = 'index_re'
            index_choice_max = 'index_re__max'
            index_choice_avg = 'index_re__avg'

        # Intentionally leave the following  code here for future debugging purpose
        # Because this piece of code often choke
        tmp1 = br_BaiduIndexCh.objects.filter(date=latest_date)
        tmp2 = tmp1.aggregate(Max(index_choice))
        tmp3 = tmp2[index_choice_max]
        tmp4 = float(tmp3)

        result_set[1] = ['br_baidu_index_ch',
                         float(brand.baiduindexch_set.latest('date').index),
                         # tmp4,   # NOTE, tmp4 is same as the following line
                         float(br_BaiduIndexCh.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_BaiduIndexCh.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[2] = ['br_baidu_index_en',
                         float(brand.baiduindexen_set.latest('date').index),
                         float(br_BaiduIndexEn.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_BaiduIndexEn.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[3] = ['br_baidu_news_ch',
                         float(brand.baidunewsch_set.latest('date').index),
                         float(br_BaiduNewsCh.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_BaiduNewsCh.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[4] = ['br_baidu_news_en',
                         float(brand.baidunewsen_set.latest('date').index),
                         float(br_BaiduNewsEn.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_BaiduNewsEn.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[5] = ['br_baidu_site',
                         float(brand.baidusite_set.latest('date').index),
                         float(br_BaiduSite.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_BaiduSite.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[6] = ['br_google_index_en',
                         float(brand.googleindexen_set.latest('date').index),
                         float(br_GoogleIndexEn.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_GoogleIndexEn.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[7] = ['br_google_index_hk',
                         float(brand.googleindexhk_set.latest('date').index),
                         float(br_GoogleIndexHk.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_GoogleIndexHk.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[8] = ['br_google_news',
                         float(brand.googlenews_set.latest('date').index),
                         float(br_GoogleNews.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_GoogleNews.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
        result_set[9] = ['br_google_site',
                         float(brand.googlesite_set.latest('date').index),
                         float(br_GoogleSite.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
                         float(br_GoogleSite.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
    #     result_set[10] = ['br_yahoojap_index_en',
    #                      float(brand.yahoojapindexen_set.latest('date').index),
    #                      float(br_YahoojapIndexEn.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
    #                      float(br_YahoojapIndexEn.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
    #     result_set[11] = ['br_yahoojap_index_jp',
    #                      float(brand.yahoojapindexjp_set.latest('date').index),
    #                      float(br_YahoojapIndexJp.objects.filter(date=latest_date).aggregate(Max(index_choice))[index_choice_max]),
    #                      float(br_YahoojapIndexJp.objects.filter(date=latest_date).aggregate(Avg(index_choice))[index_choice_avg])]
    return json.dumps(result_set)

def get_race_percentages(brand_infor):
    race_per = [-1]*8
    if brand_infor.enroll_americanindiannative_percentage is not None:
        race_per[0] = int(brand_infor.enroll_americanindiannative_percentage[:-1])
    if brand_infor.enroll_asian_pacific_percentage is not None:
        race_per[1] = int(brand_infor.enroll_asian_pacific_percentage[:-1])
    if brand_infor.enroll_black_percentage is not None:
        race_per[2] = int(brand_infor.enroll_black_percentage[:-1])
    if brand_infor.enroll_latino_percentage is not None:
        race_per[3] = int(brand_infor.enroll_latino_percentage[:-1])
    if brand_infor.enroll_white_percentage is not None:
        race_per[4] = int(brand_infor.enroll_white_percentage[:-1])
    if brand_infor.enroll_towormoreraces_percentage is not None:
        race_per[5] = int(brand_infor.enroll_towormoreraces_percentage[:-1])
    if brand_infor.enroll_raceunknown_percentage is not None:
        race_per[6] = int(brand_infor.enroll_raceunknown_percentage[:-1])
    if brand_infor.enroll_nonresidentalien_percentage is not None:
        race_per[7] = int(brand_infor.enroll_nonresidentalien_percentage[:-1])
    return race_per

# get composite index for brand in the period of last num_days days
def get_composite_index(brand_id, num_days, index_category):
    composite = None
    if index_category == 'general':
        composite = br_CompositeIndex.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days]
    return composite

# get google index for brand in the period of last num_days days
def get_gg_index(brand_id, num_days, index_category):
    gg = [None] * 4
    if index_category == 'general':
        gg[0] = br_GoogleIndexEn.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # gg index en
        gg[1] = br_GoogleIndexHk.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # gg index hk
        gg[2] = br_GoogleNews.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # gg news
        gg[3] = br_GoogleSite.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # gg site
    return [[a, b, c, d] for a, b, c, d in zip(gg[0], gg[1], gg[2], gg[3])]
    
# get baidu index for brand in the period of last num_days days
def get_bd_index(brand_id, num_days, index_category):
    bd = [None] * 5
    if index_category == 'general':
        bd[0] = br_BaiduIndexCh.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # bd index ch
        bd[1] = br_BaiduIndexEn.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # bd index en
        bd[2] = br_BaiduNewsCh.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # bd news ch
        bd[3] = br_BaiduNewsEn.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # bd news en
        bd[4] = br_BaiduSite.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # bd site
    return [[a, b, c, d, e] for a, b, c, d, e in zip(bd[0], bd[1], bd[2], bd[3], bd[4])]
        
# get yahoo index for brand in the period of last num_days days
def get_yh_index(brand_id, num_days):
    yh = [None] * 2
    yh[0] = br_YahoojapIndexEn.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # yh index en
    yh[1] = br_YahoojapIndexJp.objects.filter(brand=int(brand_id)).order_by('-date')[:num_days] # yh index jp
    return [[a, b] for a, b in zip(yh[0], yh[1])]
    
# get all indexes of selected period for a Brand
def get_all_indexes(brand_id, num_days):
    indexes = [None] * 11
    indexes[0] = br_GoogleIndexEn.objects.filter(brand=brand_id).order_by('-date')[:num_days] # gg index en
    indexes[1] = br_GoogleIndexHk.objects.filter(brand=brand_id).order_by('-date')[:num_days] # gg index hk
    indexes[2] = br_GoogleNews.objects.filter(brand=brand_id).order_by('-date')[:num_days] # gg news
    indexes[3] = br_GoogleSite.objects.filter(brand=brand_id).order_by('-date')[:num_days] # gg site
    indexes[4] = br_BaiduIndexCh.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd index ch
    indexes[5] = br_BaiduIndexEn.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd index en
    indexes[6] = br_BaiduNewsCh.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd news ch
    indexes[7] = br_BaiduNewsEn.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd news en
    indexes[8] = br_BaiduSite.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd site
#     indexes[9] = br_YahoojapIndexEn.objects.filter(brand=brand_id).order_by('-date')[:num_days] # yh index en
#     indexes[10] = br_YahoojapIndexJp.objects.filter(brand=brand_id).order_by('-date')[:num_days] # yh index jp
    return indexes

# get specific index of selected period for a Brand
def get_index(brand_id, index_name, num_days, index_category):
    if index_category == 'general':
        if index_name == 'br_composite_index':
            return br_CompositeIndex.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd index en
        if index_name == 'bd_index_en' :
            return br_BaiduIndexEn.objects.filter(brand=brand_id).order_by('-date')[:num_days] # bd index en
        if index_name == 'bd_index_ch' :
            return br_BaiduIndexCh.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'bd_news_en' :
            return br_BaiduNewsEn.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'bd_news_ch' :
            return br_BaiduNewsCh.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'bd_site' :
            return br_BaiduSite.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'gg_index_en' :
            return br_GoogleIndexEn.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'gg_index_hk' :
            return br_GoogleIndexHk.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'gg_news_en' :
            return br_GoogleNews.objects.filter(brand=brand_id).order_by('-date')[:num_days]
        if index_name == 'gg_site' :
            return br_GoogleSite.objects.filter(brand=brand_id).order_by('-date')[:num_days]
    
# convert list per brand to list per chart
def convert_to_chart_data(list_per_brand):
    list_for_chart = []
    for i in range(0, len(list_per_brand[0])):
        temp_list = []
        for j in range(0, len(list_per_brand)):
            temp_list.append(list_per_brand[j][i])
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

def convert_to_chart_data_index(list_per_brand):
    list_per_day = []
    for i in range(len(list_per_brand[0])):
        one_list = []
        for j in range(len(list_per_brand)):
            one_list.append(list_per_brand[j][i])
        list_per_day.append(one_list)
    return list_per_day
def get_data_col(brand_ids):
    brands = []
    for id in brand_ids: # get all indexes of a brand
        id = int(id)
        brands.append(get_all_indexes(id, 1)[:-2])

    # group indexes by src for a list of brands
    data_sets = []
    for i in range(len(brands[0])):
        one_set = []
        one_set.append(['Brand', 'Index'])
        for j in range(len(brands)):
            print brands[j][i][0].brand.name
            one_set.append([brands[j][i][0].brand.name.encode('ascii','ignore') + '', float(brands[j][i][0].index)])
        print one_set
        data_sets.append(one_set)
    #print data_sets
    return data_sets
        
def get_index_data_col(brand_ids, index_name, index_category):
    data_set = []
    data_set.append(['Brand', 'Index'])
    if index_category == 'general':
        for id in brand_ids:
            brand_id = int(id)
            #print float(get_index(brand_id, index_name, 1)[0].index)
            data_set.append([Brand.objects.get(id=brand_id).name.encode('ascii','ignore'),
                             float(get_index(brand_id, index_name, 1, index_category)[0].index)])
    return data_set

def get_index_report(brand_id, num_days, index_category):
    result_set = get_latest_indexes_for_brand_view(brand_id, index_category)
    # composite
    composite_by_date = get_composite_index(brand_id, num_days, index_category)
    # gg
    gg_by_date = get_gg_index(brand_id, num_days, index_category)
    # bd
    bd_by_date = get_bd_index(brand_id, num_days, index_category)
    return result_set, composite_by_date, gg_by_date, bd_by_date

def get_pie_data(brand_infor):
    #financial aid
    financial_yes = -1
    financial_no = -1
    if brand_infor.financial_aid_percentage is not None:
        financial_yes = int(brand_infor.financial_aid_percentage[:-1])
        financial_no = 100 - financial_yes
        
    #admission
    admission_yes = -1
    admission_no = -1
    if brand_infor.admission_percentage is not None:
        admission_yes = int(brand_infor.admission_percentage[:-1])
        admission_no = 100 - admission_yes
        
    #gender enrollment
    male = -1
    female = -1
    if brand_infor.admission_percentage is not None:
        male = int(brand_infor.enroll_male_percentage[:-1])
        female = int(brand_infor.enroll_female_percentage[:-1])
    
    #Enrollment by Race
    #a_i_n, a_p, black, latino, white, unknown, n_r= -1, -1, -1, -1, -1, -1, -1
    race_percentages = get_race_percentages(brand_infor)
    
    # attendance
    full_time, part_time = -1, -1
    if brand_infor.fulltime_percentage is not None:
        full_time = int(brand_infor.fulltime_percentage[:-1])
        part_time = 100 - full_time
    
    return financial_yes, financial_no, admission_yes, admission_no, male, female, race_percentages, full_time, part_time

def get_brand_name(brand_id):
    brand = Brand.objects.get(id=brand_id)
    return brand.name

def get_brand_id(brand_name):
    brand = Brand.objects.get(name = brand_name)
    return brand.id

