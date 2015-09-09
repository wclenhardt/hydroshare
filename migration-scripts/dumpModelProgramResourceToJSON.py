import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from hs_model_program.models import ModelProgramResource 

django.setup()
data = serializers.serialize("json", ModelProgramResource.objects.all(), fields=('short_id', 'public', 'comments_count', 'rating_count', 'rating_average', 'rating_sum', 'user', 'creator', 'owners', 'view_users', 'edit_users'))
out = open("modelprogramresource.json", "w")
out.write(data)
out.close()
