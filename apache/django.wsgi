import os
import sys

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/dev/Workspace/mediaWatch_lu/mediaWatch_lu')
sys.path.append('/home/dev/Workspace/mediaWatch_lu/mediaWatch_lu/mediaWatch_lu')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mediaWatch_lu.settings'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

with open('/home/dev/Workspace/mediaWatch_lu/mediaWatch_lu/apache/out.txt','a') as writer:
    writer.write('sys path is :\n')
    for l in sys.path:
        writer.write(l+'\n')

    writer.write('latest result is here\n')
writer.close()


