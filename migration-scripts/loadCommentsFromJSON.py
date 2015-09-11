# usage: python loadCommentsFromJSON.py comments.JSON resources.JSON new_resources.JSON
# where resources.JSON is used to find mapping from object_pk to short_id and
# new_resources.JSON is used to find mapping from short_id to object_pk for new resources
import os
import sys
import json

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers

django.setup()

id_to_short_id = {}
with open(sys.argv[2]) as old_res_file:
    for old_res in serializers.deserialize("json", old_res_file):
        id_to_short_id[str(old_res.object.pk)] = old_res.object.short_id

short_id_to_id = {}
with open(sys.argv[3]) as new_res_file:
    for new_res in serializers.deserialize("json", new_res_file):
        short_id_to_id[new_res.object.short_id] = str(new_res.object.pk)

with open(sys.argv[1]) as json_file:
    for comment in serializers.deserialize("json", json_file):
        short_id = id_to_short_id[comment.object.object_pk]
        comment.object.object_pk = short_id_to_id[short_id]
        comment.save()

