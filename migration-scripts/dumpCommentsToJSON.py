import os

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hydroshare.settings")

import django
from django.core import serializers
#from mezzanine.generic.models import Rating, ThreadedComment
from django.contrib.comments.models import Comment

django.setup()
data = serializers.serialize("json", Comment.objects.all(), indent=4)
out = open("comments.json", "w")

out.write(data)
out.close()
