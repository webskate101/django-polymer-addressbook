from django.contrib import admin

from addressbook import models


admin.site.register(models.Organization)
admin.site.register(models.Person)
