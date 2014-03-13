import register.models
from django.contrib import admin

admin.site.register(register.models.LDAP)
admin.site.register(register.models.mail)
admin.site.register(register.models.admins)
admin.site.register(register.models.request)
admin.site.register(register.models.service)



