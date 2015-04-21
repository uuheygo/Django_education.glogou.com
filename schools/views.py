from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
import json

from utils.get_media_indexes import get_latest_indexes_for_school_view

from schools.models import School, SchoolInforYearly, SchoolsComparisonId, \
    BaiduIndexCh, BaiduIndexEn, BaiduNewsEn,\
    BaiduNewsCh, BaiduSite, GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp

latest_year = SchoolInforYearly.objects.aggregate(Max('year'))['year__max']

# render schools.html for all or selected schools
def list_view(requet, state = 'all', rank_range = 'all', page = '1'):
    # get all schools: id, rank, name, state, cost, population
    all_schools = SchoolInforYearly.objects.filter(year=latest_year).values('school__id', 'overall_rank', 
                                                           'school__name', 'school__state_full',
                                                           'annual_cost', 'student_population')

    # filter by state and rank
    result_set = None
    if state == 'all' and rank_range == 'all':
        result_set = all_schools
    elif state == 'all' and rank_range != 'all':
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_schools.filter(overall_rank__lte=end, overall_rank__gte=start)
    elif rank_range == 'all':
        result_set = all_schools.filter(school__state_short=state)
    else:
        start, end = [int(elem) for elem in rank_range.split('-')]
        result_set = all_schools.filter(overall_rank__lte=end, overall_rank__gte=start, \
                                        school__state_full=state)
    
    # paginator the result set 50/page
    paginator = Paginator(result_set, 50)
    try:
        one_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        one_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        one_page = paginator.page(paginator.num_pages)
    
    return render_to_response('schools/schools.html', {'one_page': one_page})


def school_view(request, school_id = '0'):
    school_id = int(school_id)
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)
    result_set = get_latest_indexes_for_school_view(school) # all latest indexes
    latest_date = BaiduIndexCh.objects.aggregate(Max('date'))['date__max']
    comparison_list = school.school_to_compare.all()
    print len(comparison_list)
    print result_set
    return render(request, 'schools/school_page.html', 
                  {'school': school, 'school_infor': school_infor, 
                   'latest_date': latest_date, 'result_set': result_set,
                   'comparison_list': comparison_list})







