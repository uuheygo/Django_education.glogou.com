/*  __NOTE__BL__, Need to add a columns to a few table. For some reason django database migration tool does not work
So, we have to manually change the table.
For the record, the following is what I had tried to use Django Migration tool
1. change 'False' to 'True' in models.py for each of the table.
2. python manage.py makemigrations
3. python manage migrate

For above step 2 and 3, I also had tried:
4. python manage.py makemigrations schools
5. python manage.py migrate schools

Still does not work.

I also tried to delete profiles from table django_migrations and also delete files from schools\migration
directory, still did not work. Every time, I will get "No migrations to apply".

I had tried this on django 1.7.4
*/

USE mediawatch_lu;
/* Add a column to each table */
ALTER TABLE composite_index ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE baidu_index_ch ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE baidu_index_en ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE baidu_news_ch ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE baidu_news_en ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE baidu_site ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE google_index_en ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE google_index_hk ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE google_news ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE google_site ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE yahoojap_index_en ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;
ALTER TABLE yahoojap_index_jp ADD COLUMN my_index_re DECIMAL(20,7) NULL AFTER my_index;

/* verify the change of column */
show columns from composite_index;
show columns from baidu_index_ch;
show columns from baidu_index_en;
show columns from baidu_news_ch;
show columns from baidu_news_en;
show columns from baidu_site;
show columns from google_index_en;
show columns from google_index_hk;
show columns from google_news;
show columns from baidu_index_ch;
show columns from google_site;
show columns from yahoojap_index_en;
show columns from yahoojap_index_jp;