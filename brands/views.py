from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from utils.helper_functions import get_brand_name, get_brand_id
import json

from utils.helper_functions import get_latest_indexes_for_brand_view, get_result_set, filter_by_keyword, \
    get_race_percentages, get_gg_index, get_bd_index, get_yh_index, get_all_indexes, convert_to_chart_data, \
    get_data_col, get_index, get_index_data_col, convert_to_chart_data_index, get_index_report, get_pie_data,\
    get_composite_index, get_brand_name

from .models import Brand, BrandInforYearly, BrandsComparisonId, \
    br_BaiduIndexCh, br_BaiduIndexEn, br_BaiduNewsEn, br_BaiduNewsCh, br_BaiduSite, \
    br_GoogleIndexEn, br_GoogleIndexHk, br_GoogleNews, br_GoogleSite,\
    br_YahoojapIndexEn, br_YahoojapIndexJp, BrandChName
    
from .forms import ContactForm


latest_year = BrandInforYearly.objects.aggregate(Max('year'))['year__max']
latest_date = br_BaiduIndexCh.objects.aggregate(Max('date'))['date__max']

# render brands.html for all or selected brands
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
        return render_to_response('brands/brand_table.html', {'one_page': one_page,
                        'page_range': paginator.page_range}, context_instance=RequestContext(request))
    return render_to_response('brands/brands.html', {'one_page': one_page,
                        'page_range': paginator.page_range, 'state': state, 'rank_range': rank_range})


def brand_view(request, brand_id = '0'):
    brand_id = int(brand_id)
    brand = Brand.objects.get(id=brand_id)
    brand_infor = brand.brandinforyearly_set.filter(year=latest_year)
    result_set = get_latest_indexes_for_brand_view(brand_id) # all latest indexes
    print result_set
    comparison_list = brand.brand_to_compare.all()
    return render(request, 'brands/brand_page.html',
                  {'brand': brand, 'brand_infor': brand_infor,
                   'latest_date': latest_date, 'result_set': result_set,
                   'comparison_list': comparison_list})

def info_view(request, brand_id = '0'):
    brand_id = int(brand_id)
    brand = Brand.objects.get(id=brand_id)
    brand_infor = brand.brandinforyearly_set.filter(year=latest_year)[0]
    comparison_list = brand.brand_to_compare.all()
    
    financial_yes, financial_no, admission_yes, admission_no, male, female, race_percentages, full_time, part_time = \
        get_pie_data(brand_infor)
#     #financial aid
#     financial_yes = -1
#     financial_no = -1
#     if brand_infor.financial_aid_percentage is not None:
#         financial_yes = int(brand_infor.financial_aid_percentage[:-1])
#         financial_no = 100 - financial_yes
#         
#     #admission
#     admission_yes = -1
#     admission_no = -1
#     if brand_infor.admission_percentage is not None:
#         admission_yes = int(brand_infor.admission_percentage[:-1])
#         admission_no = 100 - admission_yes
#         
#     #gender enrollment
#     male = -1
#     female = -1
#     if brand_infor.admission_percentage is not None:
#         male = int(brand_infor.enroll_male_percentage[:-1])
#         female = int(brand_infor.enroll_female_percentage[:-1])
#     
#     #Enrollment by Race
#     #a_i_n, a_p, black, latino, white, unknown, n_r= -1, -1, -1, -1, -1, -1, -1
#     race_percentages = get_race_percentages(brand_infor)
#     
#     # attendance
#     full_time, part_time = -1, -1
#     if brand_infor.fulltime_percentage is not None:
#         full_time = int(brand_infor.fulltime_percentage[:-1])
#         part_time = 100 - full_time
    
    return render(request, 'brands/brand_info.html', {'brand': brand,
                    'brand_infor': brand_infor, 'comparison_list': comparison_list,
                    'financial_yes': financial_yes, 'financial_no': financial_no,
                    'admission_yes': admission_yes, 'admission_no': admission_no,
                    'male': male, 'female': female, 'race': race_percentages,
                    'full_time': full_time, 'part_time': part_time,
                    })

def media_view(request, brand_id='0'):
    brand_id = int(brand_id)
    num_days = '30'
    index_category = 'general'
    if request.GET.get('num_days'):
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ########### place holder for other categories
    if index_category != 'general':
        return render(request, 'brands/under_construction.html')
    
    brand = Brand.objects.get(id=brand_id)
    brand_infor = brand.brandinforyearly_set.filter(year=latest_year)
    comparison_list = brand.brand_to_compare.all()
    
    # ---default media indexes are latest 30 days
    composite_by_date = get_composite_index(brand_id, num_days, index_category)
    # gg
    gg_by_date = get_gg_index(brand_id, num_days, index_category)
    # bd
    bd_by_date = get_bd_index(brand_id, num_days, index_category)
    # yh
    #yh_by_date = get_yh_index(brand_id, num_days, index_category)
    
    return render(request, 'brands/brand_media.html', {'brand': brand, 'index_category':index_category,
                    'brand_infor': brand_infor, 'comparison_list': comparison_list,
                    'gg': gg_by_date, 'bd': bd_by_date, #'yh': yh_by_date,
                    'num_days': num_days, 'composite': composite_by_date,
                                                        })

# auto-completion list for custom selection of brands for comparison
def custom_selection(request):
    if request.is_ajax():
        text = request.GET.get('term', '').lower()
        result_set = get_result_set('All states', 'All')
        results = filter_by_keyword(result_set, text)
        
        result_list = []
        # format matching brands for autocomplete list
        for brand in results:
            brand_json = {}
            brand_json['label'] = brand['brand__name']
            brand_json['value'] = brand['brand__id']
            result_list.append(brand_json)
        data = json.dumps(result_list)
    else:
        data = 'No match'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


# compare media index of selected brands
def compare_view(request, this_id=''):
    this_brand = Brand.objects.get(id = int(this_id))
    num_days = '30' # default period
    index_name = 'br_composite_index'
    index_category = 'general'

    index_dict = {'bd_index_en':'Baidu Page Index (EN)', 'bd_index_ch':'Baidu Page Index (CH)',
                  'bd_news_en':'Baidu News Index (EN)', 'bd_news_ch':'Baidu News Index (CH)',
                  'bd_site':'Baidu Site Index', 'gg_index_en':'Google Page Index (EN)',
                  'gg_index_hk':'Google Page Index (HK)', 'gg_news_en':'Google News Index (EN)',
                  'gg_site':'Google Site Index', 'br_composite_index':'Composite Index'}


    if request.GET.get('num_days'): # custom selected period
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_name'):
        index_name = request.GET.get('index_name')
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ##### place holde for other index category
    if index_category != 'general':
        return render(request, 'brands/under_construction.html')

    brand_names = []
    for checked in request.GET.keys():
        if checked != 'num_days' and checked != 'index_name' and checked != 'index_category':
            brand_names.append(request.GET[checked])
    brand_ids = []
    for brand_name in brand_names :
        brand_ids.append(int(get_brand_id(brand_name)))


    # get line chart data
    name_list = [] # store selected brand names for lookup
    index_list = [] # store index list of each brand, one to one with name_list
    selected_brands = [] # selected brands for comparison
    for brand_name in brand_names:
        brand_name = str(brand_name)
        brand_obj = Brand.objects.get(name =brand_name)
        if brand_obj.id != int(this_id) :
            selected_brands.append(brand_obj)
        indexes = get_index(brand_obj.id, index_name, num_days, index_category)
        name_list.append(brand_obj.name)
        index_list.append(indexes)
#     print brand_dict
#     print brand_dict['name_list']
#     print brand_dict['United States Military Academy']
    
    #index_list = convert_to_chart_data(index_list)
    # get column chart data
    #data_sets_col = get_data_col(brand_ids)
    data_sets_col = get_index_data_col(brand_ids, index_name, index_category)
    index_list = convert_to_chart_data_index(index_list)
    #print data_sets_col
    return render(request,'brands/brand_compare.html', {'this_brand': this_brand,'index_category':index_category,
                    'name_list': name_list, 'index_list': index_list, 'num_days': num_days,
                    'data_sets_col': data_sets_col, 'selected_brands': selected_brands,
                    'latest_date': latest_date, 'index_name': index_dict[index_name],})

def news_view(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand_ch = brand.brandchname.ch_simp
    # print brand_ch
    comparison_list = brand.brand_to_compare.all()
    return render(request, 'brands/brand_news.html', {'brand': brand, 'brand_ch': brand_ch, 'comparison_list': comparison_list})

def report_view(request, brand_id):
    num_days = '30' # default period
    index_category = 'general' # default category
    if request.GET.get('num_days'): # custom selected period
        num_days = request.GET.get('num_days')
    num_days = int(num_days)
    if request.GET.get('index_category'):
        index_category = request.GET.get('index_category')
    
    ########### place holder for other categories
    if index_category != 'general':
        return render(request, 'brands/under_construction.html')
    
    brand_id = int(brand_id)
    brand = Brand.objects.get(id=brand_id)
    brand_infor = brand.brandinforyearly_set.filter(year=latest_year)[0]
    
    result_set, composite_by_date, gg_by_date, bd_by_date = get_index_report(brand_id, num_days, index_category)
    financial_yes, financial_no, admission_yes, admission_no, male, female, race_percentages, full_time, part_time = \
        get_pie_data(brand_infor)
#     # all latest indexes
#     result_set = get_latest_indexes_for_brand_view(brand)
#     # gg
#     gg_by_date = get_gg_index(brand_id, num_days)
#     # bd
#     bd_by_date = get_bd_index(brand_id, num_days)
    return render(request, 'brands/brand_report.html',
                  {'brand': brand, 'brand_infor': brand_infor, 'index_category': index_category,
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
        return HttpResponseRedirect('/brands/thanks/')
    
    form = ContactForm()
    return render(request, 'brands/contact_us.html', {'form': form})
    
    
    
    
    
    
    