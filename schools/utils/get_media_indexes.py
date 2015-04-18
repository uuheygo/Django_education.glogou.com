from django.db.models import Max
import json
from schools.models import School, SchoolInforYearly, BaiduIndexCh, BaiduIndexEn, BaiduNewsEn,\
    BaiduNewsCh, BaiduSite, GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp

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