import os

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from mezzanine.generic.models import Rating, ThreadedComment

django.setup()
data = serializers.serialize("json", list(ThreadedComment.objects.all())+list(Rating.objects.all()), indent=4)
out = open("threaded_comments_rating.json", "w")

out.write(data)
out.close()
