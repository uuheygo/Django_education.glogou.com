from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from utils.helper_functions import get_school_name, get_school_id
import json

from utils.helper_functions import get_latest_indexes_for_school_view, get_result_set, filter_by_keyword, \
    get_race_percentages, get_gg_index, get_bd_index, get_yh_index, get_all_indexes, convert_to_chart_data, \
    get_data_col, get_index, get_index_data_col, convert_to_chart_data_index, get_index_report, get_pie_data,\
    get_composite_index, get_school_name

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
    result_set = get_latest_indexes_for_school_view(school_id) # all latest indexes
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
    
    financial_yes, financial_no, admission_yes, admission_no, male, female, race_percentages, full_time, part_time = \
        get_pie_data(school_infor)
#     #financial aid
#     financial_yes = -1
#     financial_no = -1
#     if school_infor.financial_aid_percentage is not None:
#         financial_yes = int(school_infor.financial_aid_percentage[:-1])
#         financial_no = 100 - financial_yes
#         
#     #admission
#     admission_yes = -1
#     admission_no = -1
#     if school_infor.admission_percentage is not None:
#         admission_yes = int(school_infor.admission_percentage[:-1])
#         admission_no = 100 - admission_yes
#         
#     #gender enrollment
#     male = -1
#     female = -1
#     if school_infor.admission_percentage is not None:
#         male = int(school_infor.enroll_male_percentage[:-1])
#         female = int(school_infor.enroll_female_percentage[:-1])
#     
#     #Enrollment by Race
#     #a_i_n, a_p, black, latino, white, unknown, n_r= -1, -1, -1, -1, -1, -1, -1
#     race_percentages = get_race_percentages(school_infor)
#     
#     # attendance
#     full_time, part_time = -1, -1
#     if school_infor.fulltime_percentage is not None:
#         full_time = int(school_infor.fulltime_percentage[:-1])
#         part_time = 100 - full_time
    
    return render(request, 'schools/school_info.html', {'school': school, 
                    'school_infor': school_infor, 'comparison_list': comparison_list,
                    'financial_yes': financial_yes, 'financial_no': financial_no,
                    'admission_yes': admission_yes, 'admission_no': admission_no,
                    'male': male, 'female': female, 'race': race_percentages,
                    'full_time': full_time, 'part_time': part_time,
                    })

def media_view(request, school_id='0'):
    school_id = int(school_id)
    num_days = '30'
    index_category = 'general'
    if request.GET.get('num_days'):
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ########### place holder for other categories
    if index_category != 'general':
        return render(request, 'schools/under_construction.html')
    
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)
    comparison_list = school.school_to_compare.all()
    
    # ---default media indexes are latest 30 days
    composite_by_date = get_composite_index(school_id, num_days, index_category)
    # gg
    gg_by_date = get_gg_index(school_id, num_days, index_category)
    # bd
    bd_by_date = get_bd_index(school_id, num_days, index_category)
    # yh
    #yh_by_date = get_yh_index(school_id, num_days, index_category)
    
    return render(request, 'schools/school_media.html', {'school': school, 'index_category':index_category,
                    'school_infor': school_infor, 'comparison_list': comparison_list,
                    'gg': gg_by_date, 'bd': bd_by_date, #'yh': yh_by_date,
                    'num_days': num_days, 'composite': composite_by_date,
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
    this_school = School.objects.get(id = int(this_id))
    num_days = '30' # default period
    index_name = 'composite_index'
    index_category = 'general'

    index_dict = {'bd_index_en':'Baidu Page Index (EN)', 'bd_index_ch':'Baidu Page Index (CH)',
                  'bd_news_en':'Baidu News Index (EN)', 'bd_news_ch':'Baidu News Index (CH)',
                  'bd_site':'Baidu Site Index', 'gg_index_en':'Google Page Index (EN)',
                  'gg_index_hk':'Google Page Index (HK)', 'gg_news_en':'Google News Index (EN)',
                  'gg_site':'Google Site Index', 'composite_index':'Composite Index'}


    if request.GET.get('num_days'): # custom selected period
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_name'):
        index_name = request.GET.get('index_name')
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ##### place holde for other index category
    if index_category != 'general':
        return render(request, 'schools/under_construction.html')

    school_names = []
    for checked in request.GET.keys():
        if checked != 'num_days' and checked != 'index_name' and checked != 'index_category':
            school_names.append(request.GET[checked])
    school_ids = []
    for school_name in school_names :
        school_ids.append(int(get_school_id(school_name)))


    # get line chart data
    name_list = [] # store selected school names for lookup
    index_list = [] # store index list of each school, one to one with name_list
    selected_schools = [] # selected schools for comparison
    for school_name in school_names:
        school_name = str(school_name)
        school_obj = School.objects.get(name =school_name)
        if school_obj.id != int(this_id) :
            selected_schools.append(school_obj)
        indexes = get_index(school_obj.id, index_name, num_days, index_category)
        name_list.append(school_obj.name)
        index_list.append(indexes)
#     print school_dict
#     print school_dict['name_list']
#     print school_dict['United States Military Academy']
    
    #index_list = convert_to_chart_data(index_list)
    # get column chart data
    #data_sets_col = get_data_col(school_ids)
    data_sets_col = get_index_data_col(school_ids, index_name, index_category)
    index_list = convert_to_chart_data_index(index_list)
    #print data_sets_col
    return render(request,'schools/school_compare.html', {'this_school': this_school,'index_category':index_category,
                    'name_list': name_list, 'index_list': index_list, 'num_days': num_days,
                    'data_sets_col': data_sets_col, 'selected_schools': selected_schools,
                    'latest_date': latest_date, 'index_name': index_dict[index_name],})

def news_view(request, school_id):
    school = School.objects.get(id=school_id)
    school_ch = school.schoolchname.ch_simp
    # print school_ch
    comparison_list = school.school_to_compare.all()
    return render(request, 'schools/school_news.html', {'school': school, 'school_ch': school_ch, 'comparison_list': comparison_list})

def report_view(request, school_id):
    num_days = '30' # default period
    index_category = 'general' # default category
    if request.GET.get('num_days'): # custom selected period
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ########### place holder for other categories
    if index_category != 'general':
        return render(request, 'schools/under_construction.html')
    
    school_id = int(school_id)
    school = School.objects.get(id=school_id)
    school_infor = school.schoolinforyearly_set.filter(year=latest_year)[0]
    
    result_set, composite_by_date, gg_by_date, bd_by_date = get_index_report(school_id, num_days, index_category)
    financial_yes, financial_no, admission_yes, admission_no, male, female, race_percentages, full_time, part_time = \
        get_pie_data(school_infor)
#     # all latest indexes
#     result_set = get_latest_indexes_for_school_view(school) 
#     # gg
#     gg_by_date = get_gg_index(school_id, num_days)
#     # bd
#     bd_by_date = get_bd_index(school_id, num_days)
    return render(request, 'schools/school_report.html',
                  {'school': school, 'school_infor': school_infor, 'index_category': index_category,
                   'latest_date': latest_date, 'result_set': result_set, 'composite': composite_by_date,
                   'gg': gg_by_date, 'bd': bd_by_date, 'num_days': num_days,
                   'financial_yes': financial_yes, 'financial_no': financial_no,
                    'admission_yes': admission_yes, 'admission_no': admission_no,
                    'male': male, 'female': female, 'race': race_percentages,
                    'full_time': full_time, 'part_time': part_time,})

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
    
def college_recruiting_view(request):
   return render(request, 'schools/college_recruiting.html',{})

def alumni_engagement_view(request):
   return render(request, 'schools/alumni_engagement.html',{})


    
    
    
    
    