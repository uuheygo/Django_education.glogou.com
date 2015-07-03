Last Modifed: 7/3/2015

1. This project will run as a separate Django project, it is not on the same project as SSP and Media planning.
   On Linux server, we need to configure httpd.conf and wsgi
   
2. There is a background data crawling project related to this project.

The source code for the  data crawling project is mediaWatch_lu_auto_processing,
it runs on a server, media-watching.com, and there is a crontab which controls 
the task.

3. This project will requires Django 1.7 or later

4. On our existing linux server, either www.glogou.com or www.glogou.us, need to set virtual environment,
   go to: /home/dev/Workspace/mediaWatch_lu/env
   source bin/activate
