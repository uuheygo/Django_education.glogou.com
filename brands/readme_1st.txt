Last Modified Date: 7/03/2015
Last Modified by: _BL_

1. First time creation of brands app.
The brands app is a copy of schools app.

2. At this moment, we copy everything from schools directory to brands
directory, then just rename file names and variable names recursively.

School --> Brand
Schools --> Brands
school --> brand

3. Also a few table names in models.py are renamed.
For example:
GoogleSite  --> br_GoogleSite
BaiduNewsCh --> br_BaiduNewsCh

and a few more. (Compare brands\models.py vs schools\models.py) can find
all the difference.

4. The url for brands is something like:
127.0.0.1:8000/brands

5. To alter database, we had done:
   python manage.py makemigrations brands
   python manage.py sqlmigrate brands 0001   # NOTE 0001 is part of name of file generated in previous step.
   python manage.py migrate

   Above steps are explained in
   https://docs.djangoproject.com/en/1.7/intro/tutorial01/

   Because, in Django 1.7, we do not need do 'syncdb'
