import os
import sys

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django

django.setup()

content_path_list = []

for(dirpath, dirnames, filenames) in os.walk(sys.argv[1]):
    for dirname in dirnames:
        if dirname != 'bags':
            content_path_list.append(os.path.join(sys.argv[1], dirname))
    break

# print content_path_list

from hs_core.serialization import create_resource_from_bag
for content_path in content_path_list:
    try:
        create_resource_from_bag(content_path)
    except Exception as ex:
        print ex.message
        continue