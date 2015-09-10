import os

os.environ.setdefault("PYTHONPATH", '/home/docker/hydroshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hydroshare.settings'

import django
from django.utils import six
from django.core.serializers.json import Serializer
from django.contrib.comments.models import Comment
from mezzanine.generic.models import ThreadedComment

class MySerializer(Serializer):
    def serialize(self, queryset, **options):
        """
        Serialize a queryset.
        """
        self.options = options

        self.stream = options.pop("stream", six.StringIO())
        self.selected_fields = options.pop("fields", None)
        self.use_natural_foreign_keys = options.pop('use_natural_foreign_keys', False)
        self.use_natural_primary_keys = options.pop('use_natural_primary_keys', False)

        self.start_serialization()
        self.first = True
        for count, obj in enumerate(queryset, start=1):
            self.start_object(obj)
            # Use the concrete parent class' _meta instead of the object's _meta
            # This is to avoid local_fields problems for proxy models. Refs #17717.
            concrete_model = obj._meta.concrete_model
            for field in concrete_model._meta.fields:
                if field.serialize:
                    if hasattr(field, 'remote_field') and field.remote_field is None:
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    else:
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            self.handle_fk_field(obj, field)
            for field in concrete_model._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)
            self.end_object(obj)
            if self.first:
                self.first = False
        self.end_serialization()
        return self.getvalue()

django.setup()
myserializer = MySerializer()
#all_objs = list(ThreadedComment.objects.all())+list(Comment.objects.all())
all_objs = list(ThreadedComment.objects.all())
data = myserializer.serialize(all_objs, indent=4)
out = open("threaded_comments.json", "w")

out.write(data)
out.close()
