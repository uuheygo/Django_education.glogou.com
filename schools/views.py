from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
import json

from utils.helper_functions import get_latest_indexes_for_school_view, get_result_set, filter_by_keyword, \
    get_race_percentages, get_gg_index, get_bd_index, get_yh_index, get_all_indexes, convert_to_chart_data, \
    get_data_col

from .models import School, SchoolInforYearly, SchoolsComparisonId, \
    BaiduIndexCh, BaiduIndexEn, BaiduNewsEn, BaiduNewsCh, BaiduSite, \
    GoogleIndexEn, GoogleIndexHk, GoogleNews, GoogleSite,\
    YahoojapIndexEn, YahoojapIndexJp, SchoolChName
    
from .forms import ContactForm


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
    print result_set
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

def media_view(request, school_id='0'):
    school_id = int(school_id)
    num_days = '7'
    if request.GET.get('num_days'):
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)
    comparison_list = school.school_to_compare.all()
    
    # ---default media indexes are latest 7 days
    # gg
    gg_by_date = get_gg_index(school_id, num_days)
    # bd
    bd_by_date = get_bd_index(school_id, num_days)
    # yh
    yh_by_date = get_yh_index(school_id, num_days)
    
    return render(request, 'schools/school_media.html', {'school': school, 
                    'school_infor': school_infor, 'comparison_list': comparison_list,
                    'gg': gg_by_date, 'bd': bd_by_date, 'yh': yh_by_date,
                    'num_days': num_days,
                                                        })

# auto-completion list for custom selection of schools for comparison
def custom_selection(request):
    if request.is_ajax():
        text = request.GET.get('term', '').lower()
        result_set = get_result_set('All states', 'All')
        results = filter_by_keyword(result_set, text)
        
        result_list = []
        # format matching schools for autocomplete list
        for school in results:
            school_json = {}
            school_json['label'] = school['school__name']
            school_json['value'] = school['school__id']
            result_list.append(school_json)
        data = json.dumps(result_list)
    else:
        data = 'No match'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# compare media index of selected schools
def compare_view(request, this_id=''):
    #print this_id
    num_days = '7' # default period
    this_school = School.objects.get(id=int(this_id)) # the school to compare
    
    if request.GET.get('num_days'): # custom selected period
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    
    school_ids = []
    for checked in request.GET.keys():
        if checked != 'num_days':
            school_ids.append(request.GET[checked])
    #print school_ids
    # get line chart data
    name_list = [] # store selected school names for lookup
    index_list = [] # store index list of each school, one to one with name_list
    selected_schools = [] # selected schools for comparison
    for school_id in school_ids:
        school_id = int(school_id)
        school_obj = School.objects.get(id=school_id)
        if school_id != int(this_id):
            selected_schools.append(school_obj)
        indexes = get_all_indexes(school_id, num_days)[:-2] # contain all indexes in the period gg, bd, yh
        name_list.append(school_obj.name)
        index_list.append(indexes)
#     print school_dict
#     print school_dict['name_list']
#     print school_dict['United States Military Academy']
    
    index_list = convert_to_chart_data(index_list)
    
    # get column chart data
    data_sets_col = get_data_col(school_ids)
    #print data_sets_col
    return render(request, 'schools/school_compare.html', {'this_school': this_school, 
                    'name_list': name_list, 'index_list': index_list, 'num_days': num_days,
                    'data_sets_col': data_sets_col, 'selected_schools': selected_schools,
                    'latest_date': latest_date,})

def news_view(request, school_id):
    school = School.objects.get(id=school_id)
    school_ch = school.schoolchname.ch_simp
    print school_ch
    comparison_list = school.school_to_compare.all()
    return render(request, 'schools/school_news.html', {'school': school, 'school_ch': school_ch, 'comparison_list': comparison_list})

def report_view(request, school_id):
    return render(request, 'schools/under_construction.html')

# contact form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): # validate form fields
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = ['pengluustc@gmail.com', 'lupengscu@gmail.com']
        
        if cc_myself:
            recipients.append(email)
            
        send_mail(subject, message, email, recipients)
        return HttpResponseRedirect('/schools/thanks/')
    
    form = ContactForm()
    return render(request, 'schools/contact_us.html', {'form': form})
    
    
    
    
    
    
    