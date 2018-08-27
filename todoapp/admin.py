from django.contrib import admin

from .models import Profile,Todo,Group,Thread

admin.site.register(Profile)
admin.site.register(Todo)
admin.site.register(Group)
admin.site.register(Thread)
