from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
import json

from utils.helper_functions import get_latest_indexes_for_school_view, get_result_set, filter_by_keyword, \
    get_race_percentages

from schools.models import School, SchoolInforYearly, SchoolsComparisonId, \
    BaiduIndexCh, BaiduIndexEn, BaiduNewsEn, BaiduNewsCh, BaiduSite, \
    GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp

latest_year = SchoolInforYearly.objects.aggregate(Max('year'))['year__max']
latest_date = BaiduIndexCh.objects.aggregate(Max('date'))['date__max']

# render schools.html for all or selected schools
def list_view(request, state = 'All states', rank_range = 'All', page = '1', keyword=''):
    if request.GET.get('state'):
        state = request.GET.get('state')
    if request.GET.get('rank_range'):
        rank_range = request.GET.get('rank_range')
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
    #print state, rank_range, keyword
    
    # filter by state and rank
    result_set = get_result_set(state, rank_range)
    
    # filter by keywords
    if len(keyword) > 1:
        result_set = filter_by_keyword(result_set, keyword)
    
    # paginator the result set 50/page
    paginator = Paginator(result_set, 100)
    try:
        one_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        one_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        one_page = paginator.page(paginator.num_pages)
    
    if request.is_ajax(): # render only the table for filtering
        return render_to_response('schools/school_table.html', {'one_page': one_page, 
                        'page_range': paginator.page_range}, context_instance=RequestContext(request))
    return render_to_response('schools/schools.html', {'one_page': one_page, 
                        'page_range': paginator.page_range, 'state': state, 'rank_range': rank_range})


def school_view(request, school_id = '0'):
    school_id = int(school_id)
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)
    result_set = get_latest_indexes_for_school_view(school) # all latest indexes
    
    comparison_list = school.school_to_compare.all()
    return render(request, 'schools/school_page.html', 
                  {'school': school, 'school_infor': school_infor, 
                   'latest_date': latest_date, 'result_set': result_set,
                   'comparison_list': comparison_list})

def info_view(request, school_id = '0'):
    school_id = int(school_id)
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)[0]
    comparison_list = school.school_to_compare.all()
    
    #financial aid
    financial_yes = -1
    financial_no = -1
    if school_infor.financial_aid_percentage is not None:
        financial_yes = int(school_infor.financial_aid_percentage[:-1])
        financial_no = 100 - financial_yes
        
    #admission
    admission_yes = -1
    admission_no = -1
    if school_infor.admission_percentage is not None:
        admission_yes = int(school_infor.admission_percentage[:-1])
        admission_no = 100 - admission_yes
        
    #gender enrollment
    male = -1
    female = -1
    if school_infor.admission_percentage is not None:
        male = int(school_infor.enroll_male_percentage[:-1])
        female = int(school_infor.enroll_female_percentage[:-1])
    
    #Enrollment by Race
    a_i_n, a_p, black, latino, white, unknown, n_r= -1, -1, -1, -1, -1, -1, -1
    race_percentages = get_race_percentages(school_infor)
    
    # attendance
    full_time, part_time = -1, -1
    if school_infor.fulltime_percentage is not None:
        full_time = int(school_infor.fulltime_percentage[:-1])
        part_time = 100 - full_time
    
    return render(request, 'schools/school_info.html', {'school': school, 
                    'school_infor': school_infor, 'comparison_list': comparison_list,
                    'financial_yes': financial_yes, 'financial_no': financial_no,
                    'admission_yes': admission_yes, 'admission_no': admission_no,
                    'male': male, 'female': female, 'race': race_percentages,
                    'full_time': full_time, 'part_time': part_time,
                    })

def media_view(request, school_id='0', num_days = 7):
    school_id = int(school_id)
    
    if not request.is_ajax():
        school = School.objects.get(id=school_id)
        school_infor = school.schoolinforyearly_set.filter(year=latest_year)
        comparison_list = school.school_to_compare.all()
    
    
    # ---default media indexes are latest 7 days
    # gg
    gg = [None] * 4
    gg[0] = GoogleIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg index en
    gg[1] = GoogleIndexHk.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg index hk
    gg[2] = GoogleNews.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg news
    gg[3] = GoogleSite.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # gg site
    
    # bd
    bd = [None] * 5
    bd[0] = BaiduIndexCh.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd index ch
    bd[1] = BaiduIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd index en
    bd[2] = BaiduNewsCh.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd news ch
    bd[3] = BaiduNewsEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd news en
    bd[4] = BaiduSite.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # bd site
    
    # yh
    yh = [None] * 2
    yh[0] = YahoojapIndexEn.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # yh index en
    yh[1] = YahoojapIndexJp.objects.filter(school=int(school_id)).order_by('-date')[:num_days] # yh index jp
    
    # ajax call to use custom media index period
    if request.is_ajax():
        return render(request, 'schools/index_charts.html', {
                    'gg': gg, 'bd': bd, 'yh': yh,
                    })
    
    return render(request, 'schools/school_media.html', {'school': school, 
                    'school_infor': school_infor, 'comparison_list': comparison_list,
                    'gg': gg, 'bd': bd, 'yh': yh,
                                                        })





