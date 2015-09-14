# usage: python loadThreadedCommentsFromJSON.py threaded_comments.JSON 
# where threaded_comments.JSON is generated from dumpThreadedCommentsToJSON
# Author: Hong Yi
import os
import sys
import json

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from django.contrib.comments.models import Comment
from mezzanine.generic.models import ThreadedComment

django.setup()
with open(sys.argv[1]) as json_file:
    for obj in serializers.deserialize("json", json_file):
        obj.save()

