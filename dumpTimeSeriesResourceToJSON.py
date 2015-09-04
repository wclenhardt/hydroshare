import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from hs_app_timeseries.models import TimeSeriesResource 

django.setup()
data = serializers.serialize("json", TimeSeriesResource.objects.all(), fields=('short_id', 'public', 'comments_count', 'rating_count', 'rating_average', 'rating_sum', 'user', 'creator', 'owners', 'view_users', 'edit_users'))
out = open("timeseriesresource.json", "w")
out.write(data)
out.close()
