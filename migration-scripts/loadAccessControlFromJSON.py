# usage: python loadAccessControlFromJSON.py resources.JSON
# where resources.JSON has old resource info including access controls.
# This script read the old resource access control info and ingest
# them into the new access control system
# Author: Hong Yi
import os
import sys
import json

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

django.setup()

from hs_core import hydroshare
from hs_access_control.models import PrivilegeCodes, HSAccessException

# get admin user as requesting user so it has permission to add access control for all resources
r_user = User.objects.get(pk=1)
if not r_user.is_superuser:
    print "pk=1 is not a superuser, exit"
    exit()

with open(sys.argv[1]) as old_res_file:
    for old_res in serializers.deserialize("json", old_res_file):
        res_id = old_res.object.short_id
        owners = old_res.object.owners
        edit_users = old_res.object.edit_users
        view_users = old_res.object.view_users
        print res_id
        print owners
        print edit_users
        print view_users
        try:
           res = hydroshare.utils.get_resource_by_shortkey(res_id, or_404=False)
        except ObjectDoesNotExist:
           print "No resource was found for resource id:%s" % res_id
           continue

        res.raccess.public = old_res.object.public
        res.raccess.save()

        try:
            r_user.uaccess.share_resource_with_user(res, view_users, PrivilegeCodes.VIEW)
        except HSAccessException as exp:
            print exp.message
            exit()

        try:
            r_user.uaccess.share_resource_with_user(res, edit_users, PrivilegeCodes.CHANGE)
        except HSAccessException as exp:
            print exp.message
            exit()

        try:
            r_user.uaccess.share_resource_with_user(res, owners, PrivilegeCodes.OWNER)
        except HSAccessException as exp:
            print exp.message
            exit()