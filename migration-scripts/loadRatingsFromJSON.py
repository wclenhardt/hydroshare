# usage: python loadRatingsFromJSON.py rating.JSON resources.JSON new_resources.JSON
# where resources.JSON is used to find mapping from object_pk to short_id and
# new_resources.JSON is used to find mapping from short_id to object_pk for new resources
# Author: Hong Yi
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
    # cannot use django serializers.deserialize("json", old_res_file) since the new resource model
    # has changed which will result in "no field" errors while loading old resource data into new
    # resource model; instead, directly read json data to get resource id to short_id mapping instead
    res_data = json.loads(old_res_file.read())
    for item in res_data:
        res_id = item["pk"]
        res_short_id = item["fields"]["short_id"]
        id_to_short_id[res_id] = res_short_id
    old_res_file.close()

short_id_to_id = {}
with open(sys.argv[3]) as new_res_file:
    for new_res in serializers.deserialize("json", new_res_file):
        short_id_to_id[new_res.object.short_id] = new_res.object.pk
    new_res_file.close()

with open(sys.argv[1]) as json_file:
    for rating in serializers.deserialize("json", json_file):
        try:
            short_id = id_to_short_id[rating.object.object_pk]
            rating.object.object_pk = short_id_to_id[short_id]
            rating.save()
        except KeyError as ex:
            print ex.message
            continue
    json_file.close()
