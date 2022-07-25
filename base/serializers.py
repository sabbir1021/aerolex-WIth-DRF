from django.contrib.auth import get_user_model
from rest_framework.serializers import SerializerMethodField, ModelSerializer

User = get_user_model()


class ReadWriteSerializerMethodField(SerializerMethodField):
    """
    Default SerializerMethodField in drf is read only.
    This method field class supports both read and write
    """

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        self.read_only = False
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {f'{self.field_name}_id': data}


