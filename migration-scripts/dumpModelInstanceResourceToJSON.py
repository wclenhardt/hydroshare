import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from hs_modelinstance.models import ModelInstanceResource 

django.setup()
data = serializers.serialize("json", ModelInstanceResource.objects.all(), fields=('short_id', 'public', 'comments_count', 'rating_count', 'rating_average', 'rating_sum', 'user', 'creator', 'owners', 'view_users', 'edit_users'), indent=4)
out = open("modelinstanceresource.json", "w")
out.write(data)
out.close()
