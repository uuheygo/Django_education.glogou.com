from __future__ import unicode_literals

from django.db import models

# Option to show either normalized 'index' or renormalized index value
# This option is mainly used to set alias (property) in model.
# NOTE, NOT all SQL functions can be accessed using this alias (property) method.
# An example of such exception is: aggregate(Max(...)) and aggregate(Avg(...))
g_USE_INDEX_OR_INDEX_RE = 1       # 0, use normalized index, 1, use renormalized index

class Brand(models.Model):
    name = models.CharField(max_length=200)
    brand_url = models.CharField(db_column='url', max_length=200, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state_full = models.CharField(max_length=45)
    state_short = models.CharField(max_length=45, blank=True, null=True)
    logo_url = models.CharField(max_length=200, blank=True, null=True)
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, blank=True, null=True)
    googleplus_url = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.CharField(max_length=200, blank=True, null=True)
    youtube_url = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    forbes_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'brand'



class BrandChName(models.Model):
    brand = models.OneToOneField(Brand, db_column='brand', primary_key=True)
    ch_simp = models.CharField(max_length=200, blank=True, null=True)
    ch_trad = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "Chinese names for %s" % self.brand.name

    class Meta:
        managed = True
        db_table = 'brand_ch_name'


class BrandInforYearly(models.Model):
    brand = models.ForeignKey(Brand, db_column='brand')
    year = models.IntegerField(blank=True, null=True)
    overall_rank = models.IntegerField(blank=True, null=True)
    student_population = models.CharField(max_length=10, blank=True, null=True)
    undergrad_population = models.CharField(max_length=10, blank=True, null=True)
    student_faculty_ratio = models.CharField(max_length=10, blank=True, null=True)
    annual_cost = models.CharField(max_length=10, blank=True, null=True)
    in_state_tuition = models.CharField(max_length=10, blank=True, null=True)
    out_state_tuition = models.CharField(max_length=10, blank=True, null=True)
    financial_aid_percentage = models.CharField(max_length=10, blank=True, null=True)
    admission_percentage = models.CharField(max_length=10, blank=True, null=True)
    sat_range = models.CharField(max_length=50, blank=True, null=True)
    act_range = models.CharField(max_length=50, blank=True, null=True)
    financial_grade = models.CharField(max_length=10, blank=True, null=True)
    enroll_male_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_female_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_americanindiannative_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_asian_pacific_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_black_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_latino_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_white_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_towormoreraces_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_raceunknown_percentage = models.CharField(max_length=10, blank=True, null=True)
    enroll_nonresidentalien_percentage = models.CharField(max_length=10, blank=True, null=True)
    fulltime_percentage = models.CharField(max_length=10, blank=True, null=True)
    parttime_percentage = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return "Yearly information for %s" % self.brand.name

    class Meta:
        managed = True
        db_table = 'brand_infor_yearly'


class BrandsComparisonId(models.Model):
    brand = models.ForeignKey(Brand, db_column='brand', related_name='brand_to_compare')
    brand_compare = models.ForeignKey(Brand, db_column='brand_compare',
                                       related_name='brand_compare_list', blank=True, null=True)

    def __unicode__(self):
        return "brands for comparison for %s" % self.brand.name

    class Meta:
        managed = True
        db_table = 'brands_comparison_id'

class br_CompositeIndex(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # Re-normalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "Composite index for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_composite_index'

class br_BaiduIndexCh(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "baidu index (ch) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_baidu_index_ch'


class br_BaiduIndexEn(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "baidu index (en) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_baidu_index_en'


class br_BaiduNewsCh(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    def __unicode__(self):
        return "baidu news index (ch) for %s" % self.brand.name

    class Meta:
        managed = True
        db_table = 'br_baidu_news_ch'


class br_BaiduNewsEn(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "baidu news index (en) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_baidu_news_en'


class br_BaiduSite(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "baidu site index for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_baidu_site'


class br_GoogleIndexEn(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "google index (en) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_google_index_en'


class br_GoogleIndexHk(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "google index (hk) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_google_index_hk'


class br_GoogleNews(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "google news index for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_google_news'


class br_GoogleSite(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "google site index for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_google_site'



class br_YahoojapIndexEn(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "yahoo japan index (en) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_yahoojap_index_en'


class br_YahoojapIndexJp(models.Model):
    brand = models.ForeignKey('Brand', db_column='brand')
    index_no = models.DecimalField(db_column='my_index', max_digits=20, decimal_places=7, blank=True, null=True)

    # renormalized index
    index_re = models.DecimalField(db_column='my_index_re', max_digits=20, decimal_places=7, blank=True, null=True)

    date = models.DateField(db_column='my_date', blank=True, null=True)

    def __unicode__(self):
        return "yahoo japan index (jp) for %s" % self.brand.name

    def _get_index(self):
        if(g_USE_INDEX_OR_INDEX_RE == 0):
            return self.index_no
        else:
            return self.index_re

    # create a property field to get index
    index = property(_get_index)

    class Meta:
        managed = True
        db_table = 'br_yahoojap_index_jp'
