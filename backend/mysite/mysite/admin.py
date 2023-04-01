from django.contrib import admin
from import_export import resources


from ..api.users import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ('email',
                            'username',
                            'first_name',
                            'last_name',
                            'password')
