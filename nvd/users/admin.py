from django.contrib import admin

from nvd.users.models import CustomUser

admin.site.register(CustomUser)
