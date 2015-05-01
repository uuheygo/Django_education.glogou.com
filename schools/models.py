# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class School(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state_full = models.CharField(max_length=45)
    state_short = models.CharField(max_length=45, blank=True, null=True)
    logo_url = models.CharField(max_length=200, blank=True, null=True)
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    twitter_url = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    forbes_url = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        managed = False
        db_table = 'school'
        


class SchoolChName(models.Model):
    school = models.OneToOneField(School, db_column='school', primary_key=True)
    ch_simp = models.CharField(max_length=200, blank=True, null=True)
    ch_trad = models.CharField(max_length=200, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return "Chinese names for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'school_ch_name'


class SchoolInforYearly(models.Model):
    school = models.ForeignKey(School, db_column='school')
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
        return "Yearly information for %s" % self.school.name
        
    class Meta:
        managed = False
        db_table = 'school_infor_yearly'


class SchoolsComparisonId(models.Model):
    school = models.ForeignKey(School, db_column='school', related_name='school_to_compare')
    school_compare = models.ForeignKey(School, db_column='school_compare', 
                                       related_name='school_compare_list', blank=True, null=True)
    
    def __unicode__(self):
        return "schools for comparison for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'schools_comparison_id'


class BaiduIndexCh(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "baidu index (ch) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'baidu_index_ch'


class BaiduIndexEn(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "baidu index (en) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'baidu_index_en'


class BaiduNewsCh(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "baidu news index (ch) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'baidu_news_ch'


class BaiduNewsEn(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "baidu news index (en) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'baidu_news_en'


class BaiduSite(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "baidu site index for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'baidu_site'


class GoogleIndexEn(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "google index (en) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'google_index_en'
    

class GoogleIndexHk(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "google index (hk) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'google_index_hk'


class GoogleNews(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "google news index for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'google_news'


class GoogleSite(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "google site index for %s" % self.school.name

    class Meta:
        managed = False
        db_table = 'google_site'



class YahoojapIndexEn(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "yahoo japan index (en) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'yahoojap_index_en'


class YahoojapIndexJp(models.Model):
    school = models.ForeignKey('School', db_column='school')
    index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "yahoo japan index (jp) for %s" % self.school.name
    
    class Meta:
        managed = False
        db_table = 'yahoojap_index_jp'
